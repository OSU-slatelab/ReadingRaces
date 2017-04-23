import pocketsphinx_wrapper
import string
import subprocess
import re
import os
import math
import sys

def build_mispellings(n_best):
    filename = 'n_best.tmp'
    with open(filename, 'w') as f:
        f.write('\n'.join(n_best))

    command = ['phonetisaurus-g2pfst']
    command.append('--model=resources/cmu_inv.fst')
    command.append('--wordlist=' + filename)
    command.append('--gsep=" "')

    FNULL = open(os.devnull, 'w')
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=FNULL)
    mispellings = []

    for line in iter(p.stdout.readline, ''):
        print(line)
        mispellings.append(re.split('\t', line)[0].strip().replace(' ', ''))

    retval = p.wait()
    if 0 != retval:
        print 'error'

    os.remove(filename)
    return mispellings

def unique(n_best, scores):
    seen = set()
    return [x for x in zip(n_best, scores) if not (x[0] in seen or seen.add(x[0]))]

def clean(word_list):
    return [word.replace('SIL', '').replace('+SPN+','').strip() for word in word_list]

def transform(scores):
    scores = [1.0/x for x in scores]
    score_sum = sum(scores)
    scores = [x/score_sum for x in scores]
    scores = [math.log(x, 1.001) for x in scores]
    return scores

class GraphemeModel(object):
    def build_command(self, word, n):
        command = ['phonetisaurus-g2pfst']
        command.append('--model=resources/cmu.fst')
        command.append('--word=' + word)
        command.append('--nbest=' + str(n))
        return command

    def predict(self, word, n):
        command = self.build_command(word, n)
        FNULL = open(os.devnull, 'w')
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=FNULL)
        n_best = []
        scores = []

        for line in iter(p.stdout.readline, ''):
            if re.match('^' + word, line):
                values = re.split('\t', line)
                n_best.append(values[2].strip())
                scores.append(float(values[1]))

        retval = p.wait()
        if 0 != retval:
            print 'error'
            return None

        r = unique(n_best, transform(scores))
        return r

class AcousticModel(object):

    def get_jsgf_name(self, word):
        return 'tmp/' + word.translate(None, string.replace(string.punctuation, '-', '')) + '.jsgf'

    def convert(self, scores):
        x = min(scores)
        weights = []
        for score in scores:
            weights.append(x/score)
        return weights

    def wild(self, scores):
        x = min(scores)
        weights = []
        for score in scores:
            if score == x:
                weights.append(1000000.0)
            else:
                weights.append(0.001)
        return weights

    def build_jsgf(self, word, rules):
        rules = [x for x in rules if x[0] != '']
        #print rules
        filename = self.get_jsgf_name(word)

        with open(filename, 'w') as f:
            f.write("#JSGF V1.0;\n")
            f.write("grammar " + word.translate(None, string.replace(string.punctuation, '-', '')) + ";\n")
            ruleNames = ["<rule" + str(i+1) + ">" for i in range(0,len(rules))]
            scores = [x[1] for x in rules]
            #print scores
            #weights = self.convert(scores)
            weights = self.wild(scores)
            #print weights
            start = ["/" + str(weight) + "/ " + name for (weight, name) in zip(weights, ruleNames)]
            f.write("public <start> = " + " | ".join(start) + ";\n")
            #f.write("public <start> = " + " | ".join(ruleNames) + ";\n")
            for (ruleName, rule) in zip(ruleNames, rules):
                #print ruleName, rule[0]
                f.write(ruleName + " = " + rule[0] + ";\n")

        return filename

    def predict(self, audio_path, n, word=None, rules=None):
        if word and rules:
            jsgf_path = self.build_jsgf(word, rules)
            ps = pocketsphinx_wrapper.PocketSphinxWrapper(n, audio_path, jsgf_path)
            #print 'Full predicted'
            os.remove(jsgf_path)
            hypotheses = ps.getList()
            scores = ps.getScores()
            t = unique(clean(hypotheses), scores)
            #print 'Full returning'
            return t
        else:
            ps = pocketsphinx_wrapper.PocketSphinxWrapper(n, audio_path, "")
            hypotheses = ps.getList()
            scores = ps.getScores()
            #print 'Acoustic predicted'
            t = unique(clean(hypotheses), scores)
            #print 'Acoustic returning'
            return t
