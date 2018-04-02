# -*- coding: utf-8 -*-

"""
Generate README.org
~~~~~~~~~~~~~~~~~~~
     __      _
  /\ \ \___ | |_ ___
 /  \/ / _ \| __/ _ \
/ /\  / (_) | ||  __/
\_\ \/ \___/ \__\___|
"""

from __future__ import unicode_literals

import re
import io
import os
import glob


def get_glob_pattern(file_name='./config'):
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        for line in fp:
            if line.strip() and line[0] != '#':
                yield line.strip()


def get_req_file(pattern):
    for f in glob.glob(pattern):
        yield f


def get_file_title(file_name):
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:.+', fp.read())

        if match:
            title = match.group(0).split(':')[-1]
            return title.strip()

        return os.path.split(file_name)[-1]


def generate(file_name='README.org'):
    list_format = '- {name} -- [[file:{path}][{title}]] ::\n'
    with io.open(file_name, 'w', encoding='utf-8') as fp:
        fp.write('#+TITLE: Note\n\n')

        sep = '\\' if os.name == 'nt' else '/'

        for pt in get_glob_pattern():
            for path in get_req_file(pt):
                name = os.path.normpath(path).split(sep)[0]
                title = get_file_title(path)
                fp.write(list_format.format(name=name, path=path, title=title))


if __name__ == '__main__':
    generate()
