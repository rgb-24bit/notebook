# -*- coding: utf-8 -*-

import os
import pathlib
import re


IGNORE_DIR = 'img', 'assets', 'static'


class FileVisitor(object):
    """Accessing objects that process files during file tree traversal."""

    def pre_visit_directory(self, dirname):
        """Method called before accessing the directory.

        Args:
            dirname: The pathlib.Path object of the directory to be accessed.
        """
        pass

    def post_visit_directory(self, dirname):
        """Method called after accessing the directory.

        Args:
            dirname: The pathlib.Path object of the directory to be accessed.
        """
        pass

    def visit_file(self, filename):
        """Method called when accessing a file.

        Args:
            filename: The pathlib.Path object of the file to be accessed.
        """

    def error_handler(self, error):
        """Method called when an exception occurs during traversal.

        Args:
            error: An instance of the exception that occurred.
        """
        pass


class FileTreeWalker(object):
    """File tree traversal object.

    Args:
        path: The directory to be traversed.
        visitor: Object that implements the FileVisitor interface.
        followlinks: Whether to traverse the symbolic link under the directory,
            the default is False.
    """
    def __init__(self, path, visitor, followlinks=False):
        self.visitor = visitor
        self.walker = os.walk(path, onerror=visitor.error_handler,
                              followlinks=followlinks)

    def walk(self):
        """Traversing the file tree."""
        try:
            dirpath, dirnames, filenames = next(self.walker)

            for dirname in dirnames:
                dirname = pathlib.Path(dirname)
                self.visitor.pre_visit_directory(dirname)
                self.walk()
                self.visitor.post_visit_directory(dirname)

            for filename in filenames:
                self.visitor.visit_file(pathlib.Path(filename))

        except StopIteration:
            pass


def get_note_name(note):
    """Get the name of the note."""
    with open(note, encoding='utf-8') as fp:
        match = re.search(r'#\+TITLE:\s*(.+)', fp.read())
        if match:
            return match.group(1)
    return pathlib.Path(note).stem


class NoteVisitor(FileVisitor):
    """Traversing the processing notes directory."""
    def __init__(self, file_obj, root, ignore_dir=None):
        self._file_obj = file_obj
        self.paths = [root]
        self.ignore_dir = ignore_dir or tuple()
        self.ignore = []  # Ignore directories may be nested

    def pre_visit_directory(self, dirname):
        if dirname.name in self.ignore_dir:
            self.ignore.append(dirname)
            return None

        self._file_obj.writelines([
            '<details><summary><b><i>%s</i></b></summary>\n' % dirname,
            '<ul>\n',
        ])
        self.paths.append(dirname)

    def post_visit_directory(self, dirname):
        if self.ignore:
            self.ignore.pop()
            return None

        self._file_obj.writelines([
            '</ul>\n',
            '</details>\n',
        ])
        self.paths.pop()

    def visit_file(self, filename):
        if self.ignore: return None
        path = pathlib.Path(*self.paths, filename).as_posix()
        name = get_note_name(path)
        self._file_obj.write('<li><a href="%s">%s</a></li>\n' % (path, name))


if __name__ == '__main__':
    with open('README.md', 'w') as fd:
        FileTreeWalker('notebook', NoteVisitor(fd, 'notebook', IGNORE_DIR)).walk()
