import glob
import re
import sys
from result import Result, ResultsContainer, ResultSummary

results_dir = 'results/old'
models = {'acoustic': "output_acoustic-*.txt", 'full': "output_full-*.txt", 'grapheme': "output_grapheme-*.txt"}

results = ResultsContainer()

def parse(line):
    row = re.split('\t', line)
    if len(row) < 3:
        print line
        sys.exit()
    return row[0].strip(), row[1].strip(), row[2].strip()

for model in models.keys():
    for f in glob.glob(results_dir + models[model]):
        with open(f, 'r') as f_in:
            for line in f_in:
                word, pronunciation, prediction = parse(line)
                results.add(word, pronunciation, model, prediction)

results.check()

r = ResultSummary(results.toList())
r.display()
