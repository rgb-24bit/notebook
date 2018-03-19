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


def get_sub_dir(parent_dir):
    """ Get subdirectory."""
    for sub_dir in os.listdir(parent_dir):
        sub_dir = os.path.join(parent_dir, sub_dir)
        if os.path.isdir(sub_dir):
            yield sub_dir


def get_sub_file(parent_dir):
    """ Get subfile."""
    for sub_file in os.listdir(parent_dir):
        sub_file = os.path.join(parent_dir, sub_file)
        if os.path.isfile(sub_file):
            yield sub_file


def is_ignore_dir(dir_path):
    """ Determine if the folder is ignored."""
    ignore_dir = ('.git', 'inbox', '_style', 'trash')

    if os.path.split(dir_path)[-1] in ignore_dir:
        return True

    for sub_file in get_sub_file(dir_path):
        if not is_ignore_file(sub_file):
            break
    else:
        return True  # No valid subfile exists

    return False


def is_ignore_file(file_path):
    """ Determine if the file is ignored."""
    file_type = os.path.splitext(file_path)[-1]
    file_name = os.path.split(file_path)[-1]
    return file_type != '.org' or file_name == 'README.org'


def get_file_title(file_path):
    """ Get file title."""
    with io.open(file_path, 'r', encoding='utf-8') as fp:
        pattern = r'#\+TITLE:.+'

        match = re.search(pattern, fp.read())
        if match:
            title = match.group(0).split(':')[-1]
            return title.strip()

        return os.path.split(file_path)[-1]


def generate_content(parent_dir, fp, digree=0):
    format = '- [[file:{path}][{name}]]\n'

    for sub_dir in get_sub_dir(parent_dir):
        if is_ignore_dir(sub_dir):
            continue

        content = digree * '  ' + '- *' + os.path.basename(sub_dir) + '*\n'
        fp.write(content)

        generate_content(sub_dir, fp, digree + 1)

    for sub_file in get_sub_file(parent_dir):
        if is_ignore_file(sub_file):
            continue

        content = digree * '  ' + format.format(path=sub_file, name=get_file_title(sub_file))
        fp.write(content)


def generate_file(parent_dir, file_name):
    with io.open(file_name, 'w', encoding='utf-8') as fp:
        fp.write('#+TITLE: Table of Contents\n\n')
        generate_content(parent_dir, fp, 0)


if __name__ == '__main__':
    generate_file('.', 'README.org')
