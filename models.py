import pocketsphinx_wrapper
import string
import subprocess
import re
import os

class GraphemeModel(object):
    def build_command(self, word, n):
        command = ['phonetisaurus-g2pfst']
        command.append('--model=cmu.fst')
        command.append('--word=' + word)
        command.append('--nbest=' + str(n))
        return command

    def predict(self, word, n):
        # TODO suppress output from stdout, too cluttered
        command = self.build_command(word, n)
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        rules = []

        for line in iter(p.stdout.readline, ''):
            if re.match('^COMPUTER-GENERATED', line):
                rules.append(re.split("\t", line)[2].strip())

        retval = p.wait()
        if 0 != retval:
            print 'error'
            return None
            # TODO do something

        return rules

class AcousticModel(object):

    def get_jsgf_name(self, word):
        return word.translate(None, string.replace(string.punctuation, '-', '')) + '.jsgf'

    def build_jsgf(self, word, rules):
        filename = self.get_jsgf_name(word)

        with open(filename, 'w') as f:
            f.write("#JSGF V1.0;")
            f.write("grammar " + filename + ";\n")
            ruleNames = ["<rule" + str(i+1) + ">" for i in range(0,len(rules))]
            f.write("public <start> = " + " | ".join(ruleNames) + ";\n")
            for (ruleName, rule) in zip(ruleNames, rules):
                f.write(ruleName + " = " + rule + ";\n")

        return filename

    def predict(self, word, audio_path, n, rules):
        jsgf_path = self.build_jsgf(word, rules)
        ps = pocketsphinx_wrapper.PocketSphinxWrapper(n, audio_path, jsgf_path)
        os.remove(jsgf_path)
        return ps.getList()
