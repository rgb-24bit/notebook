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


class Storage(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


def glob_dir(dir_name, glob_pattern=list()):
    """ 获取指定目录下符合 glob pattern 的 sub_dir, sub_file."""
    glob_res = Storage(sub_dir=list(), sub_file=list())

    for pattern in glob_pattern:
        for match in glob.glob(os.path.join(dir_name, pattern)):
            if os.path.isdir(match):
                glob_res.sub_dir.append(match)
            else:
                glob_res.sub_file.append(match)

    return glob_res


def get_glob_pattern(dir_name):
    """ 获取该目录的 glob 匹配模式."""
    glob_pattern = list()

    file_name = os.path.join(dir_name, '.generate')
    if os.path.isfile(file_name):
        with io.open(file_name, 'r', encoding='utf-8') as fp:
            for line in fp:
                if not line[0] == '#':
                    glob_pattern.append(line.strip())
    return glob_pattern


def get_file_title(file_name):
    """ 获取文件标题."""
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        pattern = r'#\+TITLE:.+'

        match = re.search(pattern, fp.read())
        if match:
            title = match.group(0).split(':')[-1]
            return title.strip()

        return os.path.split(file_name)[-1]


def generate_content(root_dir, root_glob_pattern, stream, digree=0):
    """ 生成 README.org 的内容"""
    kind_format = '- *{name}*\n'
    link_format = '- [[file:{path}][{name}]]\n'

    glob_pattern = get_glob_pattern(root_dir)
    if not glob_pattern:
        glob_pattern = root_glob_pattern

    glob_res = glob_dir(root_dir, glob_pattern)
    for sub_dir in glob_res.sub_dir:
        # TODO 去除重复 glob 匹配
        if glob_dir(sub_dir, glob_pattern).sub_file:
            kind = digree * '  ' + kind_format.format(
                name = os.path.basename(sub_dir[0:-1])
            )
            stream.write(kind)

            generate_content(sub_dir, glob_pattern, stream, digree + 1)

    for sub_file in glob_res.sub_file:
        link = digree * '  ' + link_format.format(
            path = sub_file,
            name = get_file_title(sub_file)
        )
        stream.write(link)

def generate_file(root_dir, file_name):
    """ 生成 README.org 文件"""
    with io.open(file_name, 'w', encoding='utf-8') as stream:
        stream.write('#+TITLE: Table of Contents\n\n')
        generate_content(root_dir, list(), stream, 0)


if __name__ == '__main__':
    generate_file('.', 'README.org')
