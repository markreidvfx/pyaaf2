from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2.cfb import CompoundFileBinary

from struct import unpack
import os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    test_file = os.path.join(test_dir, "write_test.aaf")
    f = open(test_file, 'wb+')

    ss = CompoundFileBinary(f)
    # f.flush()

    # ss.read_header()
    # ss.debug_grow = True
    try:
        for i in range(100):
            entry = ss.create_dir_entry("/test%d" % i, 'storage')
            entry = ss.create_dir_entry("/test%d/test" % i, 'storage')
            entry = ss.create_dir_entry("/test%d/test2" % i, 'storage')
            # print ss.next_free_dir_id()

        ss.remove("/test99/test2")
        ss.remove("/test99/test")
        ss.remove("/test99")

        ss.remove("/test97/test")

        ss.rmtree("test87")
    finally:
        ss.close()
        f.close()

    f = open(test_file, 'rb')
    ss = CompoundFileBinary(f)

    for root, storage, streams in ss.walk():
        # print root.path()
        for item in storage:
            print(item.path())

        # for item in streams:
        #     # data = item.data()
        #     # print item
        #     print item.path()
