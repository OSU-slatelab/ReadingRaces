import re
import sys
import models
import numpy as np
from result import Hypothesis, Result, ResultSummary

def get_min(result_set):
    set_min = 0.0
    for x in result_set:
        if x[1] < set_min:
            set_min = x[1]
    return set_min

def align(grapheme, acoustic):
    output = {}
    min_a = get_min(acoustic)
    min_g = get_min(grapheme)

    for x in acoustic:
        output[x[0]] = [min_g, x[1]]

    for x in grapheme:
        if x[0] in output:
            output[x[0]][0] = x[1]
        else:
            output[x[0]] = [x[1], min_a]
    return [[x, output[x][0], output[x][1]]for x in output.keys()]

class PronunciationPredictor(object):

    def __init__(self, n, am_results=False, gm_results=False, full_results=True, output_n=1):
        self.gm = models.GraphemeModel() # Phonetisaurus wrapper
        self.am = models.AcousticModel() # PocketSphinx wrapper
        self.n = n
        self.am_results = am_results
        self.gm_results = gm_results
        self.full_results = full_results
        self.output_n = output_n
        self.explore = False
        self.gamma = 0.7
        self.gamma_range = []

    def interpolate(self, grapheme, acoustic, gamma):
        hypotheses = align(grapheme, acoustic)
        results = []
        for h in hypotheses:
            score = gamma * h[1] + (1 - gamma) * h[2]
            #print h[0], '\t', h[1], h[2], gamma, score
            results.append([h[0], score])
        return sorted(results, key=lambda x:(-1 * x[1]))

    def predict(self, word, audio_file, pronunciation=''):
        result = Result(word, pronunciation)

        if self.explore:
            grapheme_n_best = self.gm.predict(word, self.n)
            result.add('grapheme', [Hypothesis(x) for x in grapheme_n_best[0:self.output_n]])
            acoustic_n_best = self.am.predict(audio_file, self.n, word, grapheme_n_best)
            result.add('acoustic', [Hypothesis(x) for x in acoustic_n_best[0:self.output_n]])
            for gamma in self.gamma_range:
                full_r = self.interpolate(grapheme_n_best, acoustic_n_best, gamma)
                result.add('gamma' + str(gamma), [Hypothesis(x) for x in full_r[0:self.output_n]])

        else:
            grapheme_n_best = self.gm.predict(word, self.n)
            result.add('grapheme', [Hypothesis(x) for x in grapheme_n_best[0:self.output_n]])
            #print 'Grapheme'

            acoustic_results = self.am.predict(audio_file, self.n)[0:self.output_n]
            result.add('acoustic', [Hypothesis(x) for x in acoustic_results])
            #print 'Acoustic'

            n_best = self.am.predict(audio_file, self.n, word, grapheme_n_best)
            #result.add('full', [Hypothesis(x) for x in n_best[0:self.output_n]])

            full_r = self.interpolate(grapheme_n_best, n_best, self.gamma)
            result.add('full', [Hypothesis(x) for x in full_r[0:self.output_n]])
            #print 'Full'

        return result

def parse(dataFile):
    data = []
    with open(dataFile, 'r') as f:
        for line in f:
            row = re.split('\t', line)
            #print len(row), row[0]
            data.append((row[0].strip(), row[1].strip(), row[2].strip()))
    return data

# For testing
if __name__ == '__main__':
    testFile = sys.argv[1]
    outputName = sys.argv[2]
    n = int(sys.argv[3])
    output_n = int(sys.argv[4])
    error_f = open(outputName + '_errored_words.txt', 'w')
    explore = False
    gamma_range = np.arange(0.1, 0.95, 0.05)
    p = PronunciationPredictor(n, True, True, True, output_n)

    if explore:
        p.explore = True
        p.gamma_range = gamma_range
        model_keys = ['gamma' + str(gamma) for gamma in gamma_range]
        model_keys.extend(['grapheme', 'acoustic'])
    else:
        model_keys = ['grapheme', 'acoustic', 'full']

    outputFiles = {}
    for key in model_keys:
        f = open(outputName + '_' + key + '.txt', 'w')
        outputFiles[key] = f
    
    testData = parse(testFile)

    results = []
    i = 0
    number_of_epochs = 10
    epoch_size = max(1, len(testData) / number_of_epochs)
    print 'Progress updates will come in units of', epoch_size
    for row in testData:
        i += 1
        if i % epoch_size == 0:
            print 'Progress update!\ti:', i, '\t\tword:', row[0]
        #result = p.predict(row[0], row[1], row[2])
        #result.display(outputFiles)
        #results.append(result)
        try:
            result = p.predict(row[0], row[1], row[2])
            #print 'Predicted'
            result.display(outputFiles)
            #print 'Displayed'
            results.append(result)
            #print 'Appended'
        except:
            error_f.write(str(row) + '\n')

    for f in outputFiles.values():
        f.close()

    error_f.close()

    r = ResultSummary(results, model_keys)
    r.display()

    sys.exit(0)
