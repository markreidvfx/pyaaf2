from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import subprocess
import unittest
import hashlib
import common
import aaf2
from aaf2 import exceptions

class ImportTests(unittest.TestCase):

    def test_attach(self):
        result_file = common.get_test_file('attach.aaf')
        with aaf2.open(result_file, 'w') as f:

            mob = f.create.MasterMob()
            mob_id = mob.id
            f.content.mobs.append(mob)
            with self.assertRaises(exceptions.AAFAttachError):
                f.content.mobs.append(mob)
            path = mob.dir.path()

            # dettach
            mob = f.content.mobs.pop(mob_id)

            assert len(f.content.mobs) == 0
            assert f.cfb.exists(path) == False

            f.content.mobs.append(mob)

            slot = mob.create_timeline_slot(25)
            slot.segment = f.create.Sequence()
            slot.segment['Components'].value = []

            path = slot.dir.path()

            mob = f.content.mobs.pop(mob_id)

            assert slot.dir == None
            assert f.cfb.exists(path) == False

            f.content.mobs.append(mob)

            assert slot.dir


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
