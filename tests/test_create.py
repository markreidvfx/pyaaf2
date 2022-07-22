from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
from aaf2.file import AAFFile
from aaf2.cfb import CompoundFileBinary
from aaf2.mobid import MobID
from aaf2 import exceptions
import aaf2

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


        with AAFFile(result_file, 'r') as f:
            assert f.metadict
            assert f.content
            assert f.header['ObjectModelVersion'].value == 1
            assert f.header['Version'].value == {u'major': 1, u'minor': 2}


    def test_empty_512(self):

        result_file = common.get_test_file("empty_512.aaf")
        with AAFFile(result_file, 'w', sector_size=512) as f:
            pass


        with AAFFile(result_file, 'r') as f:
            assert f.metadict
            assert f.content
            assert f.header['ObjectModelVersion'].value == 1
            assert f.header['Version'].value == {u'major': 1, u'minor': 2}

        # self.dump(result_file)

    def test_mobs(self):

        result_file = common.get_test_file('mobs.aaf')

        mobs  = {}
        now = datetime.datetime.now()
        count = 100
        with AAFFile(result_file, 'w') as f:

            for i in range(count):
                mob_id = MobID.new()
                m = f.create.MasterMob()
                m.name = "TestMob%d" %i
                m.mob_id = mob_id
                m['LastModified'].value = now
                m['CreationTime'].value = now
                m['Slots'].value = []

                f.content.mobs.append(m)

                mobs[mob_id] = m.name

        with AAFFile(result_file, 'r') as f:
            # file_mobs = f.content['Mobs'].value

            for mob in f.content.mobs:
                assert mob.mob_id in mobs
                assert mob.name == mobs[mob.mob_id]

            assert len(list(f.content.mobs)) == count


    def test_abstract(self):

        with AAFFile() as f:
            # try and create some abstract classes
            with self.assertRaises(ValueError):
                f.create.Segment()

            with self.assertRaises(ValueError):
                f.create.Component()

            with self.assertRaises(ValueError):
                f.create.PhysicalDescriptor()

    def test_delete_propetry(self):
        result_file = common.get_test_file('delete.aaf')
        with aaf2.open(result_file, 'w') as f:
            m = f.create.MasterMob()
            m['AppCode'].value = 14
            m.usage = 'Usage_LowerLevel'
            f.content.mobs.append(m)

        with aaf2.open(result_file, 'rw') as f:
            mob = list(f.content.mobs)[0]
            assert 'AppCode' in mob
            assert 'UsageCode' in mob

            del mob['AppCode']
            del mob['UsageCode']

            assert 'AppCode' not in mob
            assert 'UsageCode' not in mob

            with self.assertRaises(KeyError):
                del mob['AppCode']



        with aaf2.open(result_file, 'r') as f:
            mob = list(f.content.mobs)[0]
            assert 'AppCode' not in mob
            assert 'UsageCode' not in mob

            with self.assertRaises(KeyError):
                del mob['AppCode']

    def test_bad_timestamp(self):
        result_file = common.get_test_file('bad_timestamp.aaf')
        bad_timestamp = {u'date': {u'month': 0, u'day': 0, u'year': 0},
                         u'time': datetime.time(0, 0)}

        # NOTE: in versions 1.1.0 and 1.0.2 of the AAF SDK it is
        # possible to have datetimes python cannot decode
        # SourceForge Bug ID #1191791
        # https://sourceforge.net/p/aaf/bugs/90/

        with aaf2.open(result_file, 'w') as f:
            f.header['LastModified'].value = bad_timestamp

        with aaf2.open(result_file, 'r') as f:
            assert f.header['LastModified'].value == bad_timestamp

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
