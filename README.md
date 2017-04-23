# ReadingRaces

This tool is a standalone enhancement to Reading RACES, an oral reading fluency tutor. The tool is a prototype that allows non-technical users to add new content to the program. The system takes an input .txt file containing the story text, normalizes and tokenizes it, and identifies out-of-vocabulary words. Using a combination of a grapheme-based model and an acoustic-based model (phone recognition), an n-best list of possible pronunciations are generated. These hypotheses are labelled with automatically generated sounds-like spellings. The user can identify the correct pronunciation by hearing each one pronounced via speech synthesis.

For more details, see the [full project report](http://day279.github.io/MastersReport.pdf).

## Dependencies:

Phonetisaurus

PocketSphinx

Festival Speech Synthesis System


## Usage:

python addStory.py [--dict dictionary_file] story_file

story_file  Plaintext file containing the story to be parsed for new vocabulary

dictionary_file Phonetic dictionary to use. Default is the included dictionary, dictionary.txt, which is derived from cmudict-0.7b
