from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
from aaf2.aaf import AAFFile
from aaf2.cfb import CompoundFileBinary
from aaf2.mobid import MobID
base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
test_dir = os.path.join(base, 'results')
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

test_files = os.path.join(base, 'test_files')

import datetime


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)

    # test_file = os.path.join(test_files, "test_file_01.aaf")
    # test_file = os.path.join(test_files, "empty.aaf")
    result_file = os.path.join(test_dir, 'mobs.aaf')
    with AAFFile(result_file, 'w') as f:
        now = datetime.datetime.now()

        for i in range(100):
            mob_id = MobID.new()
            m = f.create.MasterMob()
            m.name = "TestMob%d" %i
            m.id = mob_id
            m['LastModified'].value = now
            m['CreationTime'].value = now
            m['Slots'].value = []

            f.storage['Mobs'].append(m)
            print(m.id)



    f = CompoundFileBinary(open(result_file, 'rb'))
    for root, storage, stream in f.walk():
        print(root.path())
        for s in stream:
            print(s.path())

    with AAFFile(result_file, 'r') as f:

        for root, storage, streams in f.cfb.walk():
            print(root.path())
