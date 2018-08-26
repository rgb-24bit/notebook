# -*- coding: utf-8 -*-

"""
Generate README.org
~~~~~~~~~~~~~~~~~~~

1. Only .org files required.
2. Depth does not exceed 1.
"""

import json
import re

from pathlib import Path


IGNORE = ('.git', 'inbox', 'math', '_style', '__pycache__')


class OrgWrite(object):
    @staticmethod
    def write_list(stream, name, deep=0):
        stream.write('  ' * deep + '- %s ::\n' % name)

    @staticmethod
    def write_link(stream, name, path, deep=0):
        stream.write('  ' * deep + '- [[file:%s][%s]]\n' % (path, name))

    @staticmethod
    def write_title(stream, name):
        stream.write('* ' + name + '\n')


def get_note_dir():
    for fn in Path().iterdir():
        if fn.name in IGNORE or not fn.is_dir():
            continue
        yield fn

def get_note_name(note):
    with open(note, encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:\s*(.+)', fp.read())
        if match:
            return match.group(1)
    return Path(note).stem


def generate_readme(filename):
    with open(filename, 'w+', encoding='utf-8') as stream:
        for note_dir in get_note_dir():
            OrgWrite.write_title(stream, note_dir.name)

            for note in note_dir.glob('**/*.org'):
                OrgWrite.write_link(stream, get_note_name(note), note.as_posix(), 1)


if __name__ == '__main__':
    generate_readme('README.org')
