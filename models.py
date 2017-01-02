import n_best
import string

class GraphemeModel(object):

    def predict(self, word):
        return ['']


class AcousticModel(object):

    def build_jsgf(self, word, rules):
        filename = word.translate(None, string.punctuation) + '.jsgf'

        with open(filename, 'w') as f:
            f.write("#JSGF V1.0;")
            f.write("grammar " + filename + ";\n")
            ruleNames = ["<rule" + str(i+1) + ">" for i in range(0,len(rules))]
            f.write("public <start> = " + " | ".join(ruleNames) + ";\n")
            for (ruleName, rule) in zip(ruleNames, rules):
                f.write(ruleName + " = " + rule + ";\n")

        return filename
            

    def predict(self, word, audio_path, n, options):
        jsgf_path = build_jsgf(word, options)
        nb = n_best.NBest(n, audio_path, jsgf_path)
        return nb.getList()
