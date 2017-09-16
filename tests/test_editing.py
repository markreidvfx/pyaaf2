from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2.cfb import CompoundFileBinary

from struct import unpack
import shutil
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    test_file_orig = os.path.join(test_files, "test_file_01.aaf")
    test_file = os.path.join(test_dir, "test_file_edit.aaf")

    shutil.copy(test_file_orig, test_file)

    f = open(test_file, 'rb+')

    ss = CompoundFileBinary(f)

    ss.rmtree("/MetaDictionary-1")

    ss.rmtree("/Header-2")
    ss.close()

    f = open(test_file, 'rb')
    ss = CompoundFileBinary(f)

    for root, storage, streams in ss.walk():
        print(root.path())
        for item in streams:
            # data = item.data()
            # print item
            print(item.path())
