import subprocess
import shlex
import os

def build_commands(self, word, pronunciation):
    add_entry = '(lex.add.entry \'( "' + word.upper() + '" n (((' + pronunciation + ') 1)) ))'
    say_word = "(SayText \"" + word.upper() + "\")"
    return '(lex.select "cmu")' + add_entry + say_word

def build_command_file(self, word, pronunciation):
    commands = self.build_commands(word, pronuncation)

    f = open(word + '.scm', 'w')
    f.write(commands)
    f.close()


def pronounce(self, word, pronunciation):
    f = self.build_command_file(word, pronunciation)
    args = shlex.split('festival -b ' + f.name)

    p = subprocess.Popen(args, stdout=subprocess.PIPE)

    retval = p.wait()
    os.remove(word + '.scm')
    if 0 != retval:
        print 'error pronouncing word'
        return None
        # TODO handle errors
