# -*- coding: utf-8 -*-

"""
generate htm
~~~~~~~~~~~~

生成 README.html 及 其他笔记的 HTML

Note: 速度......
"""

from __future__ import print_function
from __future__ import unicode_literals

import re
import io
import os


def generate_html(file_name):
    command = 'emacs {} --batch -f org-html-export-to-html --kill'
    os.popen(command.format(file_name)).read()  # .read() 等待命令执行完成
    if os.path.isfile(file_name.relace('.org', '.html~')):
        os.remove(file_name.replace('.org', '.html~'))


def get_all_file(file_name='README.org'):
    pattern = r'file:(.+?\.org)'
    with io.open(file_name, 'r', encoding='utf-8') as fp:
        return re.findall(pattern, fp.read())


def get_readme_html(file_name='README.org'):
    generate_html(file_name)
    with io.open('README.html', 'r+', encoding='utf-8') as fp:
        pattern = r'file:(.+?)\.org'
        repl = r'file\1\.html'
        html = fp.read()
        re.sub(pattern, repl, html)

    with io.open('README.html', 'w', encoding='utf-8') as fp:
        fp.write(html)


if __name__ == '__main__':
    get_readme_html()
    for file_name in get_all_file():
        print(file_name)
        generate_html(file_name)
