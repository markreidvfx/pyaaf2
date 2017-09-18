from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def sandbox():
    dirname = os.path.join(base, 'results')
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    return dirname

def get_test_file(name):
    return os.path.join(sandbox(), name)

def test_files_dir():
    return os.path.join(base, 'test_files')

def test_file_01():
    return os.path.join(test_files_dir(), "test_file_01.aaf")

def test_empty_file():
    return os.path.join(test_files_dir(), "empty.aaf")
