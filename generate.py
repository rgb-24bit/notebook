# -*- coding: utf-8 -*-

"""
Generate README.org
~~~~~~~~~~~~~~~~~~~

1. Only .org files required.
2. Depth does not exceed 2.
"""

from __future__ import unicode_literals

import re, io, os, glob


def get_sub_dir(path):
    for sub_dir in glob.glob(os.path.join(path, '*/')):
        yield os.path.normpath(sub_dir)


def get_sub_file(path):
    for sub_file in glob.glob(os.path.join(path, '*.org')):
        yield os.path.normpath(sub_file)


def get_file_title(path):
    with io.open(path, 'r', encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:.+', fp.read())
        if match:
            title = match.group(0).split(':')[-1]
            return title.strip()
    return os.path.split(path)[-1]


def generate(file_name='README.org'):
    link_format = '- [[file:{path}][{name}]]\n'
    with io.open(file_name, 'w', encoding='utf-8') as fp:
        fp.write('#+TITLE: Note\n\n')

        sep = '\\' if os.name == 'nt' else '/'  # 不同系统下的分隔符
        ignore_dir = ('trash', 'inbox')  # 忽略的文件夹

        # 分类子文件夹
        for sub_dir in get_sub_dir('.'):
            if sub_dir in ignore_dir:
                continue

            fp.write('- *{name}*\n'.format(name=sub_dir))

            # 分类子文件夹的子文件夹
            for sub_sub_dir in get_sub_dir(sub_dir):
                # 剔除无意义的子文件夹
                if len(list(get_sub_file(sub_sub_dir))) == 0:
                    continue

                name = sub_sub_dir.split(sep)[-1]
                fp.write('  - *{name}*\n'.format(name=name))

                # 分类子文件夹的子文件夹的子文件
                for sub_sub_file in get_sub_file(sub_sub_dir):
                    link = link_format.format(
                        path=sub_sub_file,
                        name=get_file_title(sub_sub_file))
                    fp.write('    ' + link)

            # 分类子文件夹的子文件
            for sub_file in get_sub_file(sub_dir):
                link = link_format.format(
                    path=sub_file,
                    name=get_file_title(sub_file))
                fp.write('  ' + link)


if __name__ == '__main__':
    generate()
