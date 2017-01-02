import tokenizer
import dictionary
import models

class StoryParser(object):

    def __init__(self, args):
        self.file_name = args.story_file
        self.dictionary = dictionary.Dictionary(args.dict)
        self.save = False
        self.gm = models.GraphemeModel() # Phonetisaurus wrapper
        self.am = models.AcousticModel() # PocketSphinx wrapper

    def is_new_vocabulary(self, word):
        return not self.dictionary.contains(word)

    def add_new_word(self, word, pronunciation):
        self.dictionary.insert(word, pronunciation)
        # TODO how frequently to rebuild model after new words?
        # Probably too expensive to do each time, but intermittently?

    def predict(self, word):
        n_best = self.gm.predict(word)
        n = 10
        n_best = self.am.predict(word, audio_path, n, n_best)
        print(word, n_best)
        # TODO refine this process:
        #    add TTS so user can hear pronunciations
        #    allow user to select best to add
        return n_best[0]

    def process(self, word):
        if self.is_new_vocabulary(word):
            print(word)
            pronunciation = self.predict(word)
            self.add_new_word(word, pronunciation)

    def parse(self):
        t = tokenizer.Tokenizer()
        for word in t.get_tokens(self.file_name):
            self.process(word)
        if self.save:
            self.dictionary.save()
        #display = CommandLineDisplay()
        #display.show(results)
        return 0
