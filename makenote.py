# -*- coding: utf-8 -*-

import os
import pathlib
import re


EXCLUDE_DIR = 'image', 'assets', 'static'


def get_note_name(note):
    """Get the name of the note."""
    with open(note, encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:\s*(.+)', fp.readline())
        if match:
            return match.group(1)
    return pathlib.Path(note).stem


def walk(walker):
    """Traverse the specified directory to get the note files in it."""
    try:
        dirpath, subdirs, subfiles = next(walker)

        notes = []

        for subdir in subdirs:
            subnotes = walk(walker)
            if not (subdir in EXCLUDE_DIR or len(subnotes) == 0):
                notes.append({subdir: subnotes})

        for subfile in subfiles:
            if subfile.endswith('.org'):
                notes.append(pathlib.Path(dirpath, subfile).as_posix())

        return notes
    except StopIteration:
        pass


def makecatalog(fd, notes, level=1):
    """Generate file content directory."""
    itemfmt = '  ' * level + '+ [{name}](#{anchor})\n'

    for subnotes in notes:
        if not isinstance(subnotes, dict):
            break
        name = next(iter(subnotes))
        fd.write(itemfmt.format(name=name, anchor=name.lower()))


def makecontent(fd, notes, level=0):
    """Generate file specific content."""
    headfmt = '## {name}\n'
    typefmt = '  ' * level + '+ **{name}**\n'
    itemfmt = '  ' * level + '+ [{name}]({href})\n'

    for subnotes in notes:
        if isinstance(subnotes, dict):
            name = next(iter(subnotes))
            if level == 0:
                fd.write(headfmt.format(name=name))
            else:
                fd.write(typefmt.format(name=name))
            makecontent(fd, subnotes[name], level + 1)
        else:
            fd.write(itemfmt.format(name=get_note_name(subnotes), href=subnotes))


def make(fn, basedir):
    """Generate note index."""
    notes = walk(os.walk(basedir))

    with open(fn, 'w', encoding='utf-8') as fd:
        fd.write('## Table of contents\n')
        makecatalog(fd, notes)
        makecontent(fd, notes)


if __name__ == '__main__':
    make('README.md', 'notebook')
