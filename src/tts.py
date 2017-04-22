import subprocess
import shlex
import os

def build_commands(word, pronunciation):
    add_entry = '(lex.add.entry \'( "' + word.lower() + '" n (((' + pronunciation.lower() + ') 1)) ))'
    say_word = "(SayText \"" + word.lower() + "\")"
    return '(lex.select "cmu")' + add_entry + say_word

def build_command_file(word, pronunciation):
    commands = build_commands(word, pronunciation)

    f = open('tmp/' + word + '.scm', 'w')
    f.write(commands)
    f.close()

    return f

def pronounce(word, pronunciation):
    f = build_command_file(word, pronunciation)
    args = shlex.split('festival -b ' + f.name)

    p = subprocess.Popen(args, stdout=subprocess.PIPE)

    retval = p.wait()
    #os.remove(word + '.scm')
    if 0 != retval:
        print 'error pronouncing word'
        return None
        # TODO handle errors
