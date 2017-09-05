import os
from aaf2.aaf import AAFFile
from aaf2.cfb import CompoundFileBinary

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)

    # test_file = os.path.join(test_files, "test_file_01.aaf")
    # test_file = os.path.join(test_files, "empty.aaf")
    result_file = os.path.join(test_dir, 'empty.aaf')
    with AAFFile(result_file, 'w') as f:
        print f.create.MasterMob()

    f = CompoundFileBinary(open(result_file, 'rb'))
    for root, storage, stream in f.walk():
        print root.path()
        for s in stream:
            print s.path()

    with AAFFile(result_file, 'r') as f:

        for root, storage, streams in f.cfb.walk():
            print root.path()
