#!/usr/bin/env python3
"""SJCheck -- offensive word checker

Usage:
  sjcheck.py check <dir>...

"""
import json
from pathlib import Path
from docopt import docopt
from colorama import Fore, Style
import git


skiplist = ['.git', '.idea']


with open('dictionary.json') as f:
    datafile = json.load(f)


def check_line(line):
    for word, desc in datafile['words'].items():
        if word in line:
            print(f'{Fore.RED}{Style.BRIGHT}' + datafile['categories'][desc['category']]['message'] + f'{Style.RESET_ALL}')


def check_branches(path):
    try:
        repo = git.Repo(path)
        print(f'{Fore.WHITE}{Style.BRIGHT}Checking git branches...{Style.RESET_ALL}')
        for ref in repo.refs:
            print(f'Branch: {ref.name}')
            check_line(ref.name)
    except git.exc.InvalidGitRepositoryError:
        pass


def check_file(name):
    print(f'File: {name}')
    try:
        with open(name) as f:
            for line in f:
                check_line(line)
    except UnicodeDecodeError:
        pass


def check_directory(path):
    print(f'{Fore.WHITE}{Style.BRIGHT}Entering directory: {path}{Style.RESET_ALL}')
    check_branches(path)

    pathlist = Path(path).glob('*')
    for file in pathlist:
        if file.parts[-1] in skiplist:
            print(f'Skipping: {file}')
            continue

        if file.is_file():
            check_file(file)
        if file.is_dir():
            check_directory(file)
    print(f'{Fore.WHITE}{Style.BRIGHT}Leaving directory: {path}{Style.RESET_ALL}')


if __name__ == '__main__':
    arguments = docopt(__doc__, version='SJCheck 1.0')

    if arguments["check"]:
        for path in arguments['<dir>']:
            check_directory(path)


