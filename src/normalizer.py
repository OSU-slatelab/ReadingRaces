import sys
import subprocess
import shlex
import re

nsw_path = '/home/meghan/Documents/nsw/bin/nsw_expand'
domain = 'nantc'

def get_output_file(input_file):
    tmp_dir = 'tmp/'
    input_file = tmp_dir + 'nsw-' + re.split('/', input_file)[-1]
    return input_file

def normalize(input_file):
    output_file = get_output_file(input_file)
    #options = ' '.join([nsw_path, '-domain', domain, input_file, '-output', output_file])
    options = ' '.join([nsw_path, '-domain', domain, input_file, '-output', output_file])
    print options
    p = subprocess.Popen(shlex.split(options), stdout=subprocess.PIPE)

    retval = p.wait()
    if retval != 0:
        print 'Error while recording file'
        return None

    return output_file
