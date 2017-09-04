import os
from aaf2.aaf import AAFFile

base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)

    test_file = os.path.join(test_files, "test_file_01.aaf")
    # test_file = os.path.join(test_files, "empty.aaf")
    with AAFFile(test_file) as f:
        pass
        # test = f.read_object("/Header-2/Content-3b03/Mobs-1901{a0}")
        # print test['MobID'].value
        # test = f.read_object("/Header-2/Content-3b03/Mobs-1901{27}/Slots-4403{1}/Segment-4803/Components-1001{0}")
        f.dump()
        # print f.cfb.listdir(test.dir)
