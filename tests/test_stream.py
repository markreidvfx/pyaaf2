from aaf2.cfb import CompoundFileBinary
from StringIO import StringIO

from struct import unpack
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')


def small_data(count):
    for i in range(count):
        data = "some data %d" % i
        yield  data * 10

def large_data(count):
    for i in range(count):
        data = "some larger data %d" % i
        yield  data * 10000

def write_and_test(filename, data_list, chunksize=61):
    path = os.path.join(test_dir, filename)

    f = open(path, 'wb+')

    ss = CompoundFileBinary(f)

    for i, data in enumerate(data_list):
        s = ss.open("/test_stream%d" % i, 'w')
        write_data = data
        while len(write_data):
            s.write(write_data[:chunksize])
            write_data = write_data[chunksize:]

        s.seek(0)

        result = s.read()
        # print result
        # print len(data), len(result)
        assert result == data

        s.close()

    for i, data in enumerate(data_list):
        s = ss.open("/test_stream%d" % i, 'r')
        s.seek(0)
        result = s.read()

        print len(data), len(result)
        assert result == data


    ss.close()
    f.close()

    f = open(path, 'rb')

    ss = CompoundFileBinary(f)

    for i, data in enumerate(data_list):
        s = ss.open("/test_stream%d" % i, 'r')
        # print "FAT"
        # print structured_storage.pretty_sectors(ss.fat)
        # print "MINIFAT"
        # print structured_storage.pretty_sectors(ss.minifat)

        # print ss.minifat
        print s.dir
        print "sector_id =", s.dir.sector_id
        print s.dir.byte_size, len(data)
        assert s.dir.byte_size, len(data)

        result = s.read()
        # result = s.dir.data()
        print len(result), len(data)
        # print result

        assert result == data

def write_and_ovewrite(filename, data_list1, data_list2, chunksize=61):

    path = os.path.join(test_dir, filename)

    f = open(path, 'wb+')

    ss = CompoundFileBinary(f)

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
    f.close()

    f = open(path, 'rb')

    ss = CompoundFileBinary(f)

    for i, data in enumerate(data_list2):
        s = ss.open("/test_stream%d" % i, 'r')
        # print ss.fat
        # print ss.minifat
        print s.dir.byte_size, len(data)
        assert s.dir.byte_size, len(data)
        # result = s.dir.data()

        result = s.read()
        print len(result), len(data)
        # print result
        # print data
        # print result
        assert result == data

def test_mini_stream():
    write_and_test("mini_stream.aaf", ["small data\n" * 10])

def test_multi_mini_stream():
    write_and_test("mulit_mini_stream.aaf", ["small1 data\n" * 10, "small2 data\n" * 10])

def test_large_stream():
    write_and_test("large_stream.aaf", ["large data\n" * 5000])

def test_large_mini():
    write_and_test("mini_and_large_stream.aaf", ["large data\n" * 5000,
                                                 "small data\n" * 10])
def test_mini_large():
    write_and_test("mini_and_large_stream.aaf", ["small data\n" * 10,
                                                 "large data\n" * 5000
                                                 ])

def test_lots_of_small():
    write_and_test("lots_of_small_streams.aaf", list(small_data(900)))

def test_lots_of_large():
    write_and_test("lots_of_large_streams.aaf", list(large_data(100)), chunksize=1024)

def test_64():
    write_and_test("64.aaf", list(small_data(4)), chunksize=64)

def test_4096():
    write_and_test("4096.aaf", list(large_data(5)), chunksize=4096)


def test_mix_bag():

    s = list(small_data(300))
    l = list(large_data(300))
    d = []
    for x,y in zip(s, l):
        d.append(x)
        d.append(y)

    write_and_test("mixed_bag_streams.aaf", d, chunksize=1024)


def test_overwrite():

    data1 = ["small data\n" * 20,
             "large data\n" * 5000]

    data2 = ["overwrite data\n" * 10,
             "overwrite data\n" * 10000]

    write_and_ovewrite("mini_and_large_stream.aaf", data1, data2)

def test_seek():
    path = os.path.join(test_dir, "seek_test.aaf")

    f = open(path, 'wb+')
    ss = CompoundFileBinary(f)

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


def test_stream_read_write():

    test_seek()
    test_mini_stream()
    test_large_stream()
    test_large_mini()
    test_mini_large()
    test_overwrite()
    test_multi_mini_stream()

    test_64()
    test_4096()
    test_mix_bag()
    test_lots_of_small()
    test_lots_of_large()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    test_stream_read_write()
