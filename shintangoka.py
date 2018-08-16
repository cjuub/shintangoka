#!/usr/bin/env python3

from argparse import ArgumentParser
from flask import Flask
from pathlib import Path
from typing import List

app = Flask(__name__)

new_words = []
known_words = []


@app.route('/')
def show_commands():
    return 'Welcome to shintangoka!\n\n \
            /known_words - list known words\n \
            /new_words - list new words\n \
            /add_word/<word> - adds word to list of new words\n \
            /flush_new - moves all new words to list of known words\n'


@app.route('/known_words')
def known_words():
    """
    Returns a list of all words considered known.
    """
    return '\n'.join(known_words) + '\n'


@app.route('/new_words')
def new_words():
    """
    Returns a list of all words that are not yet considered known.
    """
    return '\n'.join(new_words) + '\n'


@app.route('/add_word/<string:word>')
def add_word(word: str):
    """
    Adds the specified word to the list of new words.
    """
    if word in known_words:
        return '\'{0}\' is an already known word!\n'.format(word)

    if word not in new_words:
        new_words.append(word)
        _append_word_to_file(new_words_file, word)
    else:
        return '\'{0}\' is already in the list of new words.\n'.format(word)

    return '\'{0}\' was successfully added to the list of new words.\n'.format(word)


@app.route('/flush_new')
def flush_new():
    """
    Moves all words from the new words list to the list of known words.
    """
    global known_words, new_words

    new_words_cnt = len(new_words)

    known_words = known_words + new_words
    _save_file(known_words_file, known_words)
    new_words = []
    _save_file(new_words_file, new_words)

    return 'Moved {0} words into list of known words.\n'.format(new_words_cnt)


def _load_file(file_path: Path) -> List[str]:
    """
    Loads each line from the file and returns it as a list.
    """
    with open(file_path, 'a+') as fp:
        # create file if it does not exist
        pass

    with open(file_path, 'r') as fp:
        return [line.strip() for line in fp]


def _save_file(file_path: Path, word_list: List[str]):
    """
    Saves the list of words to the file, one word per line.
    """
    with open(file_path, 'w+') as fp:
        for word in word_list:
            fp.write(word + '\n')


def _append_word_to_file(file_path: Path, word: str):
    """
    Appends the single word to a new line at the end of the file.
    """
    with open(file_path, 'a+') as fp:
        fp.write(word + '\n')


def main():
    global known_words_file, new_words_file
    global known_words, new_words

    parser = ArgumentParser()
    parser.add_argument('known_words_file')
    parser.add_argument('new_words_file')
    args = parser.parse_args()

    known_words_file = args.known_words_file
    new_words_file = args.new_words_file

    known_words = _load_file(Path(known_words_file))
    new_words = _load_file(Path(new_words_file))

    app.run()


if __name__ == '__main__':
    main()

