from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2.cfb import CompoundFileBinary
import os
import io

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')

import unittest

class CopyTests(unittest.TestCase):
    def test_copy(self):
        src_path = os.path.join(test_files, "test_file_01.aaf")
        dst_path = os.path.join(test_dir, "test_copy.aaf")

        with io.open(src_path, 'rb') as file_a:
            ss_a = CompoundFileBinary(file_a, 'rb')
            with io.open(dst_path, 'wb+') as file_b:
                ss_b = CompoundFileBinary(file_b, 'wb+')

                # copy everything
                for root, storage, streams in ss_a.walk():
                    for item in storage:
                        entry = ss_b.makedir(item.path(), class_id=item.class_id)

                    for item in streams:
                        s_a = ss_a.open(item.path(), 'r')
                        s_b = ss_b.open(item.path(), 'w')
                        s_b.write(s_a.read())

                # check everything exists while file live
                for root, storage, streams in ss_a.walk():

                    assert ss_b.exists(root.path())
                    for item in storage:
                        assert ss_b.exists(item.path())
                        s_b = ss_b.find(item.path())
                        assert s_b.class_id == item.class_id

                    for item in streams:
                        s_a = ss_a.open(item.path(), 'r')
                        s_b = ss_b.open(item.path(), 'r')
                        assert s_a.read() == s_b.read()

                ss_b.close()

            # reopen file and check everything exists
            with io.open(dst_path, 'rb') as f:
                ss_b = CompoundFileBinary(f, 'rb')
                # check everything exists
                for root, storage, streams in ss_a.walk():

                    assert ss_b.exists(root.path())
                    for item in storage:
                        assert ss_b.exists(item.path())
                        s_b = ss_b.find(item.path())
                        assert s_b.class_id == item.class_id

                    for item in streams:
                        s_a = ss_a.open(item.path(), 'r')
                        s_b = ss_b.open(item.path(), 'r')
                        assert s_a.read() == s_b.read()


if __name__ == '__main__':

    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
