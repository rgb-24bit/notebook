# -*- coding: utf-8 -*-

"""
generate org
~~~~~~~~~~~~

生成 README.org
"""

from __future__ import unicode_literals

import re
import io
import os


def get_sub_dir(root):
    for sub_dir in os.listdir(root):
        sub_dir = os.path.join(root, sub_dir)
        if os.path.isdir(sub_dir):
            yield sub_dir


def get_sub_file(root):
    for sub_file in os.listdir(root):
        sub_file = os.path.join(root, sub_file)
        if os.path.isfile(sub_file):
            yield sub_file


def is_ignore_dir(path):
    ignore_dir = (
        '.git', 'inbox', '_style',
        'img', 'trash', 'front-end'
    )
    dir_name = os.path.split(path)[-1]
    return dir_name in ignore_dir


def is_ignore_file(path):
    file_type = os.path.splitext(path)[-1]
    file_name = os.path.split(path)[-1]
    return file_type != '.org' or file_name == 'README.org'


def get_title(path):
    with io.open(path, 'r', encoding='utf-8') as fp:
        pattern = r'#\+TITLE:.+'
        match = re.search(pattern, fp.read())

        if match:
            title = match.group(0).split(':')[-1]
            return title.strip()

        return os.path.split(path)[-1]


def generate_content(root, fp, digree=0):
    format = '- [[file:{path}][{name}]]\n'

    for sub_dir in get_sub_dir(root):
        if is_ignore_dir(sub_dir):
            continue

        content = digree * '  ' + '- *' + os.path.basename(sub_dir) + '*\n'
        fp.write(content)

        generate_content(sub_dir, fp, digree + 1)

    for sub_file in get_sub_file(root):
        if is_ignore_file(sub_file):
            continue

        content = digree * '  ' + format.format(path=sub_file, name=get_title(sub_file))
        fp.write(content)


def generate_file(root, file_name):
    with io.open(file_name, 'w', encoding='utf-8') as fp:
        fp.write('#+TITLE: Table of Contents\n\n')
        generate_content(root, fp, 0)



if __name__ == '__main__':
    generate_file('.', 'README.org')
