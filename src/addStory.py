import sys
import argparse
import story_parser
import dictionary

# constants

# exception classes

# interface functions

# classes

# internal functions and classes

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Add a story')
    parser.add_argument('story_file', 
        help='Story file to read and parse')
    parser.add_argument('--dict', nargs='?', default='resources/dictionary.txt', help='Dictionary file to use')

    parser.add_argument('--test', dest='test', action='store_true')
    parser.set_defaults(test=False)

    args = parser.parse_args(argv)

    return args


# TODO add proper logging and error handling throughout
# TODO write unit tests!
# TODO restructure project into package
def main(argv=None):
    args = process_command_line(argv)
    if args.dict != None:
        print('Testing mode: ' + str(args.test))
        parser = story_parser.StoryParser(args)
        return parser.parse()
    else:
        print('missing args.dict')
        return 1

if __name__ == '__main__':
    status = main()
    sys.exit(status)

