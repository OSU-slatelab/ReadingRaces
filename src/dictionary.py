import io
import re

class Dictionary(object):
    def _parse(self, line):
        e = re.split('\t', line.strip())
        word = re.split('\(\d\)', e[0])[0]
        return word, e[1]

    def __init__(self, path):
        self.path = path
        self.entries = {}
        with open(path, 'r') as f:
            for line in f:
                word, pronunciation = self._parse(line)
                self.insert(word, pronunciation)

    def contains(self, word):
        return word in self.entries

    def insert(self, word, pronunciation):
        if word in self.entries:
            self.entries[word].append(pronunciation)
        else:
            self.entries[word] = [pronunciation]

    def save(self):
        with open(self.path, 'w') as f:
            for key in sorted(self.entries):
                f.write(key + '\t' + self.entries[key][0] + '\n')
                for i in range(1, len(self.entries[key])):
                    f.write(key + '(' + str(i) + ')\t' + self.entries[key][i] + '\n')
