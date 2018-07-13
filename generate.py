# -*- coding: utf-8 -*-

"""
Generate README.org
~~~~~~~~~~~~~~~~~~~

1. Only .org files required.
2. Depth does not exceed 1.
"""

import re

from pathlib import Path


TITLE = """Note"""

NOTE_DIR = {
    Path('algorithm'): '数据结构与算法',
    Path('c-c++'): 'C & C++',
    Path('python'): 'Python',
    Path('java'): 'Java',
    Path('database'): '数据库',
    Path('front-end'): '前端',
    Path('lang'): '编程语言',
    Path('network'): '网络',
    Path('os'): '操作系统',
    Path('related'): '相关笔记'
}

class OrgWrite(object):
    @staticmethod
    def write_title(stream, title):
        stream.write('#+TITLE: %s\n\n' % title)

    @staticmethod
    def write_list(stream, name, deep=0):
        stream.write('  ' * deep + '- %s ::\n' % name)

    @staticmethod
    def write_link(stream, name, path, deep=0):
        stream.write('  ' * deep + '- [[file:%s][%s]]\n' % (path, name))


def get_note_name(note):
    with open(note, encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:\s*(.+)', fp.read())
        if match:
            return match.group(1)
    return Path(note).stem


def generate_readme(filename):
    with open(filename, 'w+', encoding='utf-8') as stream:
        OrgWrite.write_title(stream, TITLE)

        for directory in NOTE_DIR:
            OrgWrite.write_list(stream, NOTE_DIR.get(directory))

            for note in directory.glob('**/*.org'):
                OrgWrite.write_link(stream, get_note_name(note), note.as_posix(), 1)


if __name__ == '__main__':
    generate_readme('README.org')
