from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import unittest
from aaf2.file import AAFFile
from aaf2 import properties

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')


def walk(root, space="", func=None):
    indent = "  "

    for p in root.properties():
        if isinstance(p, properties.StrongRefProperty):
            func(space, p.name, p.typedef)
            walk(p.value, space + indent, func)

        if isinstance(p, properties.StrongRefVectorProperty):
            func(space, p.name, p.typedef)
            for obj in p.value:
                func(space + indent, obj)
                walk(obj, space + indent*2, func)
            continue

        if isinstance(p, properties.StrongRefSetProperty):
            func(space, p.name, p.typedef)
            for key, obj in p.items():
                func(space + indent, obj)
                walk(obj, space + indent*2, func)

            continue

        func(space, p.name, p.typedef, p.value)


def procces(*args):
    line = " ".join([str(item) for item in args])


class AAFTests(unittest.TestCase):


    def test_wall_all(self):

        test_file = os.path.join(test_files, "test_file_01.aaf")
        with AAFFile(test_file) as f:
            walk(f.root, '', func=procces)

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
