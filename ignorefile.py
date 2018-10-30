import fnmatch
import logging
import re
import pathlib

logger = logging.getLogger(__name__)


class IgnoreFile:
    def __init__(self):
        self.matches = []

    def parse(self, file, relative='.'):
        append_relative = (relative != '.')

        for line in file:
            if len(line) == 0:
                # Empty
                continue
            if line.startswith('#'):
                # Comment
                continue

            relative_path = f'{relative}/{line}' if append_relative else line

            file_regex = re.compile(fnmatch.translate(relative_path))
            self.matches.append(file_regex)

    def match(self, filename):
        norm_filename = pathlib.Path(filename).as_posix()
        for match in self.matches:
            if match.match(norm_filename):
                return True
        return False
