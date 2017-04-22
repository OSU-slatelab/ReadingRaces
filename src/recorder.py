import sys
import subprocess
import shlex
import platform

def linux_record(word):
    filename = word + '.wav'
    duration_in_seconds = '4'
    command = 'arecord -t wav -c 1 -r 16000 -d ' + duration_in_seconds + ' -f S16_LE ' + filename 
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

    retval = p.wait()
    if retval != 0:
        print 'Error while recording file'
        # TODO actual error handling

    return filename

def record(word):
    if 'Linux' == platform.system():
        return linux_record(word)
    else:
        print 'At this time, only Linux systems are supported. Sorry!'
        sys.exit()
