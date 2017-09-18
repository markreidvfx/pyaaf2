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

import unittest

import common
import datetime

class CreatAAFTests(unittest.TestCase):

    def dump(self, path):
        with AAFFile(path, 'r') as f:
            for root, storage, streams in f.cfb.walk():
                print(root.path())

    def test_empty(self):

        result_file = common.get_test_file("empty.aaf")
        with AAFFile(result_file, 'w') as f:
            pass

        self.dump(result_file)

    def test_mobs(self):

        result_file = common.get_test_file('mobs.aaf')
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

                f.content['Mobs'].append(m)

        self.dump(result_file)

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
