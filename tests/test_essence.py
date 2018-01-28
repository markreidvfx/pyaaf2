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


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
