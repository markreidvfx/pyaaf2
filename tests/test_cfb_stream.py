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

def small_data(count):
    for i in range(count):
        data = b"some data %d" % i
        yield  data * 10

def large_data(count):
    for i in range(count):
        data = b"some larger data %d" % i
        yield  data * 10000

import unittest
class StreamTests(unittest.TestCase):

    def write_and_test(self, filename, data_list, chunksize=61):
        path = os.path.join(test_dir, filename)

        with io.open(path, 'wb+') as f:
            ss = CompoundFileBinary(f, 'wb+')

            for i, data in enumerate(data_list):
                s = ss.open("/test_stream%d" % i, 'w')
                write_data = data
                while len(write_data):
                    s.write(write_data[:chunksize])
                    write_data = write_data[chunksize:]

                s.seek(0)

                result = s.read()

                assert result == data

                s.close()

            for i, data in enumerate(data_list):
                s = ss.open("/test_stream%d" % i, 'r')
                s.seek(0)
                result = s.read()

                assert result == data

            ss.close()


        with io.open(path, 'rb') as f:

            ss = CompoundFileBinary(f)

            for i, data in enumerate(data_list):
                s = ss.open("/test_stream%d" % i, 'r')

                assert s.dir.byte_size, len(data)

                result = s.read()

                assert result == data

    def write_and_ovewrite(self, filename, data_list1, data_list2, chunksize=61):

        path = os.path.join(test_dir, filename)

        with io.open(path, 'wb+') as f:

            ss = CompoundFileBinary(f, 'wb+')

            for i, data in enumerate(data_list1):
                s = ss.open("/test_stream%d" % i, 'w')
                while len(data):
                    s.write(data[:chunksize])
                    data = data[chunksize:]
                s.close()

            for i, data in enumerate(data_list2):
                s = ss.open("/test_stream%d" % i, 'w')
                while len(data):
                    s.write(data[:chunksize])
                    data = data[chunksize:]
                s.close()

            ss.close()

        with io.open(path, 'rb') as f:

            ss = CompoundFileBinary(f)

            for i, data in enumerate(data_list2):
                s = ss.open("/test_stream%d" % i, 'r')
                assert s.dir.byte_size, len(data)

                result = s.read()
                assert result == data

    def test_mini_stream(self):
        self.write_and_test("mini_stream.aaf", [b"small data\n" * 10])

    def test_multi_mini_stream(self):
        self.write_and_test("mulit_mini_stream.aaf", [b"small1 data\n" * 10, b"small2 data\n" * 10])

    def test_large_stream(self):
        self.write_and_test("large_stream.aaf", [b"large data\n" * 5000])

    def test_large_mini(self):
        self.write_and_test("mini_and_large_stream.aaf", [b"large data\n" * 5000,
                                                          b"small data\n" * 10])
    def test_mini_large(self):
        self.write_and_test("mini_and_large_stream.aaf", [b"small data\n" * 10,
                                                          b"large data\n" * 5000
                                                     ])

    def test_lots_of_small(self):
        self.write_and_test("lots_of_small_streams.aaf", list(small_data(300)))

    def test_lots_of_large(self):
        self.write_and_test("lots_of_large_streams.aaf", list(large_data(100)), chunksize=1024)

    def test_64(self):
        self.write_and_test("64.aaf", list(small_data(4)), chunksize=64)

    def test_4096(self):
        self.write_and_test("4096.aaf", list(large_data(5)), chunksize=4096)


    def test_mix_bag(self):

        s = list(small_data(50))
        l = list(large_data(50))
        d = []
        for x,y in zip(s, l):
            d.append(x)
            d.append(y)

        self.write_and_test("mixed_bag_streams.aaf", d, chunksize=1024)


    def test_overwrite(self):

        data1 = [b"small data\n" * 20,
                 b"large data\n" * 5000]

        data2 = [b"overwrite data\n" * 10,
                 b"overwrite data\n" * 10000]

        self.write_and_ovewrite("mini_and_large_stream.aaf", data1, data2)

    def test_seek(self):
        path = os.path.join(test_dir, "seek_test.aaf")

        f = open(path, 'wb+')
        ss = CompoundFileBinary(f, 'wb+')

        s = ss.open("/seektest", 'w')
        s.seek(100)
        data= b"end of seek"
        s.write(data)
        assert s.tell() == 100 + len(data)
        s.close()

        s = ss.open("/seek_large", 'w')
        seek_size = 1000000
        s.seek(seek_size)
        data= b"end of seek"
        s.write(data)
        assert s.dir.byte_size == seek_size  + len(data)
        s.close()
        ss.close()


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)


    unittest.main()
