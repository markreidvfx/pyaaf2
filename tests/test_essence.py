from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import unittest
import common
import os
import aaf2

class EssenceTests(unittest.TestCase):

    def test_create(self):
        new_file = os.path.join(common.sandbox(), 'create_essence.aaf')
        test_data = b"Essence Data!!"
        mob_id =  aaf2.mobid.MobID()
        mob_id.int = 1

        with aaf2.open(new_file, 'w') as f:
            mob = f.create.SourceMob()
            mob.descriptor = f.create.TapeDescriptor()
            f.content.mobs.append(mob)

            e = f.create.EssenceData()
            e.mob = mob

            f.content.essencedata.append(e)
            stream = e.open("w")
            stream.write(test_data)

            e.mob = mob

            mob.mob_id = mob_id
            e.mob_id = mob_id


        with aaf2.open(new_file, 'r') as f:
            e = next(f.content.essencedata.values())
            assert e.mob_id == mob_id
            stream = e.open("r")
            assert stream.read() == test_data
            mob = e.mob
            assert mob

    def test_write_dettached(self):
        new_file = os.path.join(common.sandbox(), 'essencedata_dettached_write.aaf')
        test_data = b"Essence Data!!"
        mob_id =  aaf2.mobid.MobID()
        mob_id.int = 1

        with aaf2.open(new_file, 'w') as f:
            e = f.create.EssenceData()
            e.mob_id = mob_id
            stream = e.open("w")
            stream.write(test_data)

            f.content.essencedata.append(e)

            stream = e.open('r')
            assert stream.read() == test_data

        with aaf2.open(new_file, 'r') as f:
            e = next(f.content.essencedata.values())
            stream = e.open("r")
            assert stream.read() == test_data

            assert not f.cfb.exists("/tmp")

    def test_write_dettached_clean(self):
        new_file = os.path.join(common.sandbox(), 'essencedata_dettached_clean.aaf')
        test_data = b"Essence Data!!"
        mob_id =  aaf2.mobid.MobID()
        mob_id.int = 1

        with aaf2.open(new_file, 'w') as f:
            e = f.create.EssenceData()
            e.mob_id = mob_id
            stream = e.open("w")
            stream.write(test_data)

        with aaf2.open(new_file, 'r') as f:
            assert not f.cfb.exists("/tmp")

    def test_read_exception(self):

        new_file = os.path.join(common.sandbox(), 'read_exception.aaf')
        test_data = b"Essence Data!!"
        mob_id =  aaf2.mobid.MobID()
        mob_id.int = 1

        with aaf2.open(new_file, 'w') as f:
            e = f.create.EssenceData()
            e.mob_id = mob_id

            with self.assertRaises(aaf2.exceptions.AAFPropertyError):
                stream = e.open('r')

            f.content.essencedata.append(e)

        with aaf2.open(new_file, 'r') as f:
            e = next(f.content.essencedata.values())
            with self.assertRaises(aaf2.exceptions.AAFPropertyError):
                stream = e.open('r')



if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
