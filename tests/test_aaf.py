from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import unittest
import aaf2
from aaf2.file import AAFFile
from aaf2 import properties

import common
import shutil

class AAFTests(unittest.TestCase):


    def test_walk_all(self):
        test_file = os.path.join(common.test_files_dir(),"test_file_01.aaf")
        with AAFFile(test_file) as f:
            common.walk_aaf(f.root)

    def test_save_as(self):

        new_file = os.path.join(common.sandbox(), 'save_r+.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        with aaf2.open(new_file, 'r+') as f:
            f.save()


        # should contents compare!
        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
