# ReadingRaces

This project is still in the early stages of development.

This tool is a standalone enhancment to ReadingRaces, an oral reading fluency tutor. The tool predicts pronunciation of new vocabulary found in stories added by the user, using the word spelling and a sample utterance. The project has dependencies on Phonetisaurus, PocketSphinx, and Festival Speech Synthesis System.

Usage:

python addStory.py [--dict dictionary_file] story_file

story_file  Plaintext file containing the story to be parsed for new vocabulary

dictionary_file Phonetic dictionary to use. Default is the included dictionary, dictionary.txt, which is derived from cmudict-0.7b
