import nltk
import io
import re
import string

def read(file_name):
    text = ''
    with open(file_name) as f:
        for line in f:
            text += line.strip()
    return text

def is_punctuation(token):
    return re.search('[A-Za-z0-9]', token) == None

def clean(token):
    return token.strip(string.punctuation).upper()

def tokenize(text):
    t = nltk.tokenize.regexp.WhitespaceTokenizer()
    tokens = []
    for token in t.tokenize(text):
        if not is_punctuation(token):
            tokens.append(clean(token))
    return tokens

class Tokenizer(object):

    def get_tokens(self, file_name):
        text = read(file_name)
        return tokenize(text)
