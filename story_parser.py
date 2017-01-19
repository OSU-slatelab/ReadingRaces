import tokenizer
import dictionary
import models
import recorder
import tts

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

    def get_audio(self, word):
        print 'Beginning acoustic prediction'
        flag = raw_input('If you would like to provide a pre-recorded .wav file, enter the path. If you would like to record the word now, enter \'r\': ')
        if 'r' = flag:
            recorder.record_to_file(word + '.wav')
        else:
            return flag

    def predict(self, word):
        n = 10
        rules = self.gm.predict(word, 10)

        audio_path = self.get_audio(word)

        n_best = self.am.predict(word, audio_path, n, rules)

        # TODO allow user to select best to add
        pronunciation = n_best[0]

        tts.pronounce(word, pronunciation)

        return pronunciation

    def process(self, word):
        if self.is_new_vocabulary(word):
            print 'New word found: ', word
            pronunciation = self.predict(word)
            self.add_new_word(word, pronunciation)

    def parse(self):
        t = tokenizer.Tokenizer()
        for word in t.get_tokens(self.file_name):
            self.process(word)
        if self.save:
            self.dictionary.save()

        # TODO build class for user I/O
        #display = CommandLineDisplay()
        #display.show(results)

        return 0
