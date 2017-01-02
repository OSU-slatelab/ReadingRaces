import sys
import argparse
import story_parser
import dictionary

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Add a story')
    parser.add_argument('story_file', 
        help='Story file to read and parse')
    parser.add_argument('--dict', nargs='?', const='dictionary.txt', help='Dictionary file to use')

    args = parser.parse_args(argv)

    return args


def main(argv=None):
    args = process_command_line(argv)
    parser = story_parser.StoryParser(args)
    return parser.parse()


if __name__ == '__main__':
    status = main()
    sys.exit(status)

