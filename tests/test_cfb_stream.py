from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
from aaf2.cfb import CompoundFileBinary
import os
import io

import common
import shutil

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

        with io.open(path, 'wb+', buffering=io.DEFAULT_BUFFER_SIZE) as f:
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


        with io.open(path, 'rb', buffering=io.DEFAULT_BUFFER_SIZE) as f:

            ss = CompoundFileBinary(f)

            for i, data in enumerate(data_list):
                s = ss.open("/test_stream%d" % i, 'r')

                assert s.dir.byte_size, len(data)

                result = s.read()

                assert result == data

    def write_and_ovewrite(self, filename, data_list1, data_list2, chunksize=61):

        path = os.path.join(test_dir, filename)

        with io.open(path, 'wb+', buffering=io.DEFAULT_BUFFER_SIZE) as f:

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

        with io.open(path, 'rb',  buffering=io.DEFAULT_BUFFER_SIZE) as f:

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

        with open(path, 'wb+') as f:
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

    def test_move(self):
        path = os.path.join(test_dir, "move_test.aaf")

        src = "/path/to/item"
        dst = "/dest/path/moved_item"

        stream_data = b'move stream data'

        steam_list = [
        "/path/to/item/child1/sub/sub/stream",
        "/path/to/item/stream",
        "/path/to/item2/stream"
        ]

        dir_list = [
        "/path/to/item/child1/sub/sub",
        "/path/to/item/child2",
        "/path/to/item/child3/more_stuff",
        "/path/to/item1/child1",
        "/path/to/item2/child2/sub/sub",
        "/path/to/item2/child2",
        "/dest/path/",
        ]

        result_dirs = [
        "/dest",
        "/dest/path",
        "/dest/path/moved_item",
        "/dest/path/moved_item/child1",
        "/dest/path/moved_item/child1/sub",
        "/dest/path/moved_item/child1/sub/sub",
        "/dest/path/moved_item/child3",
        "/path",
        "/path/to",
        "/path/to/item1",
        "/path/to/item2",
        "/path/to/item2/child2",
        "/path/to/item2/child2/sub",
        ]

        result_streams = [
            "/dest/path/moved_item/child1/sub/sub/stream",
            "/dest/path/moved_item/stream",
            '/dest/path/moved_item/child3/stream'
        ]

        with open(path, 'wb+') as f:
            cfb = CompoundFileBinary(f, 'wb+')
            for p in dir_list:
                cfb.makedirs(p)

            for p in steam_list:
                s = cfb.open(p, 'w')
                s.write(stream_data)

            cfb.move(src, dst)
            with self.assertRaises(ValueError):
                cfb.move('/path/to/item2/stream', '/dest/path/moved_item/child3')

            cfb.move('/path/to/item2/stream', '/dest/path/moved_item/child3/')

            with self.assertRaises(ValueError):
                cfb.move('/path/that/doesnt/exist', '/dest/path/moved_item/')


            with self.assertRaises(ValueError):
                cfb.move('/path/to/item2/child2', '/path/that/doesnt/exist')


            for p in result_dirs:
                assert cfb.exists(p)
                entry = cfb.find(p)
                assert entry.isdir()

            for p in result_streams:
                assert cfb.exists(p)
                entry = cfb.find(p)
                assert entry.isfile()
                assert entry.open('r').read() == stream_data

            cfb.close()

        with open(path, 'rb') as f:
            cfb = CompoundFileBinary(f, 'rb')

            for root, storage_items, streams in cfb.walk():
                pass
                # print(root.path(), streams)

            for p in result_dirs:
                assert cfb.exists(p)
                entry = cfb.find(p)
                assert entry.isdir()

            for p in result_streams:
                assert cfb.exists(p)
                entry = cfb.find(p)
                assert entry.isfile()

                assert entry.open('r').read() == stream_data

    def test_move2(self):
        src_file = common.test_file_01()
        test_file = os.path.join(test_dir, "move2_test.aaf")
        shutil.copy(src_file, test_file)

        dir_list = []
        stream_list = []
        move_root = "/Header-2/Content-3b03"

        with open(test_file, 'rb+') as f:
            cfb = CompoundFileBinary(f, 'rb+')
            for root, storage_items, streams in cfb.walk(move_root):

                for item in storage_items:
                    dir_list.append(item.path())
                for item in streams:
                    stream_list.append(item.path())

            cfb.makedir('/tmp')
            cfb.move(move_root, '/tmp/')

            for item in dir_list:
                assert not cfb.exists(item)
                new_path = item.replace(move_root, '/tmp/Content-3b03')
                assert cfb.exists(new_path)
                assert cfb.find(new_path).isdir()

            for item in stream_list:
                assert not cfb.exists(item)
                new_path = item.replace(move_root, '/tmp/Content-3b03')
                assert cfb.exists(new_path)
                assert cfb.find(new_path).isfile()

            cfb.close()

        with open(test_file, 'rb') as f:
            cfb = CompoundFileBinary(f, 'rb')
            for item in dir_list:
                assert not cfb.exists(item)
                new_path = item.replace(move_root, '/tmp/Content-3b03')
                assert cfb.exists(new_path)
                assert cfb.find(new_path).isdir()

            for item in stream_list:
                assert not cfb.exists(item)
                new_path = item.replace(move_root, '/tmp/Content-3b03')
                assert cfb.exists(new_path)
                assert cfb.find(new_path).isfile()


    def test_rmtree(self):
        src_file = common.test_file_01()
        test_file = os.path.join(test_dir, "rmtree_test.aaf")
        shutil.copy(src_file, test_file)

        remove_list = []
        remove_root = "/Header-2/Content-3b03"

        property_streams = []

        with open(test_file, 'rb+') as f:
            cfb = CompoundFileBinary(f, 'rb+')
            # for root, storage_items, streams in cfb.walk():
            #     for item in streams:
            #         print("!!", item.path())

            for root, storage_items, streams in cfb.walk(remove_root):

                for item in storage_items:
                    remove_list.append(item.path())
                for item in streams:
                    remove_list.append(item.path())

            cfb.rmtree('/Header-2/Content-3b03')

            for item in remove_list:
                assert not cfb.exists(item)

            for root, storage_items, streams in cfb.walk():
                for item in streams:
                    if item.name == 'properties':
                        property_streams.append(item.path())

            for item in property_streams:
                cfb.remove(item)

            for item in property_streams:
                assert not cfb.exists(item)

            cfb.close()

        with open(test_file, 'rb') as f:
            cfb = CompoundFileBinary(f, 'rb')
            for item in remove_list:
                assert not cfb.exists(item)

            for item in property_streams:
                assert not cfb.exists(item)

    def test_trunc_zero(self):
        test_file = os.path.join(test_dir, "trunc_zero_test.aaf")
        with open(test_file, 'wb+') as f:
            cfb = CompoundFileBinary(f, 'wb+')
            s = cfb.open("/zero_trunc", 'w')
            s.write(b'some data')
            s.seek(0)
            s.truncate()
            cfb.close()

        with open(test_file, 'rb') as f:
            cfb = CompoundFileBinary(f, 'rb')
            s = cfb.open("/zero_trunc", 'r')
            assert s.dir.byte_size == 0
            assert s.dir.sector_id is None


    def test_trunc_shrink(self):
        test_file = os.path.join(test_dir, "trunc_shrink_test.aaf")
        with open(test_file, 'wb+') as f:
            cfb = CompoundFileBinary(f, 'w+')
            s = cfb.open("/grow_trunc", 'w')
            data = b"F" * 5000
            s.write(data)
            assert s.is_mini_stream() == False
            s.truncate(256)
            assert s.is_mini_stream() == True
            cfb.close()
        with open(test_file, 'rb') as f:
            cfb = CompoundFileBinary(f, 'rb')
            s = cfb.open("/grow_trunc", 'r')
            data = s.read()
            assert data == b"F" * 256


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)


    unittest.main()
