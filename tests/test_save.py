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
from aaf2.cfb import CompoundFileBinary

class SaveTests(unittest.TestCase):
    def test_save_as(self):

        new_file = os.path.join(common.sandbox(), 'save_as.aaf')
        print(common.test_file_01())
        with aaf2.open(common.test_file_01(), 'r') as f:
            # f.dump()
            f.save(new_file)
            # print(">??")


        # f = io.open(new_file, 'rb')
        #
        # cfb = CompoundFileBinary(f, 'rb')
        # for root, storage, streams in cfb.walk():
        #     print(root.path())
        #

        with aaf2.open(new_file, 'r') as f:
            f.dump()


        # import aaf
        # f = aaf.open(new_file)


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
