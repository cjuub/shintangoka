#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def show_commands():
    return 'Welcome to shintangoka\n'

