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
import os
import re
from ignorefile import IgnoreFile

skiplist = ['.git', '.idea']


with open('dictionary.json') as f:
    datafile = json.load(f)
    patterns = datafile['patterns']
    for pattern in patterns:
        pattern['regex'] = re.compile(pattern['regex'], re.IGNORECASE)


def check_line(line):
    for pattern in patterns:
        if pattern['regex'].match(line):
            category = pattern['categories'][0]

            prefer = ''
            if 'suggest' in pattern:
                prefer = f'Prefer: {Fore.GREEN}{pattern["suggest"]}'

            print(f'{Fore.RED}{Style.BRIGHT}{datafile["categories"][category]["message"]} {prefer}{Style.RESET_ALL}')


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


def check_directory(path, ignorefile):
    print(f'{Fore.WHITE}{Style.BRIGHT}Entering directory: {path}{Style.RESET_ALL}')

    pathlist = Path(path).glob('*')
    for file in pathlist:
        if file.parts[-1] in skiplist or ignorefile.match(file):
            # print(f'Skipping: {file}')
            continue

        if file.is_file():
            check_file(file)
        if file.is_dir():
            check_directory(file, ignorefile)
    print(f'{Fore.WHITE}{Style.BRIGHT}Leaving directory: {path}{Style.RESET_ALL}')


def check_root(path):
    ignorefile = IgnoreFile()
    if os.path.isfile(f'{path}/.sjignore'):
        with open(f'{path}/.sjignore') as f:
            ignorefile.parse(f.read().splitlines(), relative=path)

    check_branches(path)
    check_directory(path, ignorefile)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='SJCheck 1.0')

    if arguments["check"]:
        for path in arguments['<dir>']:
            check_root(path)


