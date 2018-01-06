from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import aaf2
import common
import unittest
import io
import shutil


class SaveTests(unittest.TestCase):
    def test_save_as(self):

        new_file = os.path.join(common.sandbox(), 'save_r+.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        with aaf2.open(new_file, 'r+') as f:
            f.save()


        # should contents compare!
        with aaf2.open(new_file, 'r') as f:
            f.dump()


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
