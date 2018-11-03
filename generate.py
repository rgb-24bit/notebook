# -*- coding: utf-8 -*-

"""
Generate README.org
~~~~~~~~~~~~~~~~~~~

1. Only .org files required.
2. Depth does not exceed 1.
"""

import pathlib
import re


class DetailsWriter(object):
    def __init__(self, fileobj, summary):
        self._fileobj = fileobj
        self._summary = summary

    def __enter__(self):
        line = '#+HTML: <details><summary><b><i>%s</i></b></summary>\n' % self._summary
        self._fileobj.write(line)
        return self

    def __exit__(self, type_, value, trace):
        self._fileobj.write('#+HTML: </details>\n')

    def write(self, path, name):
        self._fileobj.write('- [[file:%s][%s]]\n' % (path, name))


def get_note_dir(notebook):
    """Get the directory containing the notes."""
    for fn in pathlib.Path(notebook).iterdir():
        yield fn


def get_note_name(note):
    """Get the name of the note."""
    with open(note, encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:\s*(.+)', fp.read())
        if match:
            return match.group(1)
    return pathlib.Path(note).stem


def generate(fn):
    """Generate a README document."""
    with open(fn, 'w', encoding='utf-8') as stream:
        for note_dir in get_note_dir('notebook'):
            with DetailsWriter(stream, note_dir.name) as writer:
                for note in note_dir.glob('**/*.org'):
                    writer.write(note.as_posix(), get_note_name(note))


if __name__ == '__main__':
    generate('README.org')
