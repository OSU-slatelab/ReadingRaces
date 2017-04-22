class Hypothesis(object):
    def __init__(self, hypothesis):
        self.value = hypothesis[0]
        self.score = hypothesis[1]

    def getValue(self):
        return self.value

    def getScore(self):
        return self.score

class Result(object):

    def __init__(self, word, pronunciation):
        self.word = word
        self.pronunciation = pronunciation.strip()
        self.model_results = {}

    def add(self, model_type, hypotheses):
        self.model_results[model_type] = hypotheses

    def addValue(self, model_type, hypothesis):
        if model_type not in self.model_results:
            self.model_results[model_type] = [hypothesis]
        else:
            self.model_results[model_type].append(hypothesis)

    def display(self, outputFiles):
        for result_type in self.model_results.keys():
            #print result_type
            for result in self.model_results[result_type]:
                #print result.value, result.score
                outputFiles[result_type].write(self.word + '\t' + self.pronunciation + '\t' + result.getValue() + '\t' + str(result.getScore()) + '\n')

    def get(self, model_type):
        return self.model_results[model_type]

class ResultsContainer(object):
    def __init__(self):
        self.words = {}

    def add(self, word, pronunciation, model, prediction):
        if word not in self.words:
            r = Result(word, pronunciation)
            r.add(model, [prediction])
            self.words[word] = {pronunciation: r}
        elif pronunciation not in self.words[word]:
            r = Result(word, pronunciation)
            r.add(model, [prediction])
            self.words[word][pronunciation] = r
        else:
            self.words[word][pronunciation].addValue(model, prediction)

    def toList(self):
        allResults = []
        for word in self.words.keys():
            for pronunciation in self.words[word].keys():
                allResults.append(self.words[word][pronunciation])
        return allResults

    def check(self):
        for word in self.words.keys():
            for pronunciation in self.words[word].keys():
                r = self.words[word][pronunciation].get('full')
                for p in r:
                   if p not in self.words[word][pronunciation].get('grapheme'):
                       print 'oh no!', word, p
        

class ResultSummary(object):
    def __init__(self, results, model_keys):
        self.total_words = len(results)

        self.model_accuracies = {}
        for key in model_keys:
            self.model_accuracies[key] = 0.0

        if self.total_words == 0:
            print 'ResultSummary empty'
            return

        for result in results:
            for model in result.model_results.keys():
                for mr in result.model_results[model]:
                    if result.pronunciation == mr.getValue():
                        self.model_accuracies[model] += 1.0
                        break

        for model in self.model_accuracies.keys():
            self.model_accuracies[model] /= self.total_words

    def display(self):
        for model, accuracy in self.model_accuracies.iteritems():
            print model, 'whole word accuracy:\t', accuracy
        print "Number of unique words: ", self.total_words
