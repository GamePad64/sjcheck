#!/usr/bin/env python3
"""SJCheck -- offensive word checker

Usage:
  sjcheck.py check <file>...

"""
import json
from docopt import docopt

with open('dictionary.json') as f:
    datafile = json.load(f)

def check_file(name):
    with open(name) as f:
        for line in f:
            for word, desc in datafile['words'].items():
                if word in line:
                    print(datafile['categories'][desc['category']]['message'])


if __name__ == '__main__':
    arguments = docopt(__doc__, version='ЫОСрусл 1.0')

    if arguments["check"]:
        check_file(arguments['<file>'][0])
