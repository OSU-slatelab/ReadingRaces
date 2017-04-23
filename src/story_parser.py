import tokenizer
import pronunciation_predictor
import dictionary
import models
import recorder
import tts
import os
import userinterface
import result
from normalizer import normalize

def build_creative_mispellings(n_best):
    return models.build_mispellings(n_best)

class StoryParser(object):

    def __init__(self, args):
        self.file_name = args.story_file
        self.dictionary = dictionary.Dictionary(args.dict)
        self.save = False
        self.ui = userinterface.CommandLineUI()
        self.predictor = pronunciation_predictor.PronunciationPredictor(10, 10)

    def is_new_vocabulary(self, word):
        return not self.dictionary.contains(word)
        
    def get_audio(self, word):
        flag = self.ui.prompt_audio()

        if 'r' == flag:
            return recorder.record(word)
        else:
            return flag

    def add_new_word(self, word, pronunciation):
        self.dictionary.insert(word, pronunciation)

    def predict(self, word):
        audio_path = self.get_audio(word)
        n_best = [h.getValue() for h in self.predictor.predict(word, audio_path).get('full')]

        creative_mispellings = build_creative_mispellings(n_best)

        done = False
        while not done:
            choice = self.ui.prompt_choice(n_best, creative_mispellings)
            if choice == 's':
                choice = self.ui.get_sounds_like(word)
            tts.pronounce(word, choice)
            
            done = self.ui.get_user_acceptance()

        return choice

    def process(self, word):
        if self.is_new_vocabulary(word):
            self.ui.show_new(word)
            pronunciation = self.predict(word)
            self.add_new_word(word, pronunciation)

    def parse(self):
        t = tokenizer.Tokenizer()
        for word in t.get_tokens(normalize(self.file_name)):
            self.process(word)
        if self.save:
            self.dictionary.save()

        return 0
