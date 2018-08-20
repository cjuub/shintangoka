#!/usr/bin/env python3

from argparse import ArgumentParser
from flask import Flask, request
from pathlib import Path
from typing import List

app = Flask(__name__)

new_words = []
known_words = []


@app.route('/')
def show_commands():
    return 'Welcome to shintangoka!</br>\
            </br>\
            /known_words - list known words</br>\
            /new_words - list new words</br>\
            /add_word - adds word in POST field "word" to list of new words</br>\
            /flush_new - moves all new words to list of known words</br>\
            </br>\
            <form action="/add_word" method="POST">\
                New word:</br>\
                <input type="text" name="word">\
            </form>\n'
            

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


@app.route('/add_word', methods=['POST'])
def add_word():
    """
    Adds the specified word to the list of new words.
    """
    word = request.form['word']

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
    with open(str(file_path), 'a+') as fp:
        # create file if it does not exist
        pass

    with open(str(file_path), 'r', encoding='utf-8') as fp:
        return [line.strip() for line in fp]


def _save_file(file_path: Path, word_list: List[str]):
    """
    Saves the list of words to the file, one word per line.
    """
    with open(str(file_path), 'w+', encoding='utf-8') as fp:
        for word in word_list:
            fp.write(word + '\n')


def _append_word_to_file(file_path: Path, word: str):
    """
    Appends the single word to a new line at the end of the file.
    """
    with open(str(file_path), 'a+', encoding='utf-8') as fp:
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

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=False)


if __name__ == '__main__':
    main()

