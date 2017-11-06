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

            # dettach
            mob = f.content.mobs.pop(mob_id)

            assert len(f.content.mobs) == 0

            f.content.mobs.append(mob)

            slot = mob.create_timeline_slot(25)
            slot.segment = f.create.Sequence()

            comp_paths = []
            for i in range(10):
                filler = f.create.Filler()
                filler['DataDefinition'].value = f.dictionary.lookup_datadef("picture")
                filler['Length'].value = i
                slot.segment['Components'].append(filler)
                comp_paths.append(filler.dir.path())

            assert len(slot.segment['Components']) == 10

            last = slot.segment['Components'].pop(-1)
            assert len(slot.segment['Components']) == 9
            first = slot.segment['Components'].pop(0)
            assert len(slot.segment['Components']) == 8

            for filler in slot.segment['Components']:
                assert filler.dir

            with self.assertRaises(exceptions.AAFAttachError):
                slot.segment['Components'][0] = slot.segment['Components'][1]

            mob = f.content.mobs.pop(mob_id)


            for filler in slot.segment['Components']:
                assert filler.dir is None

            assert slot.dir == None
            assert len(slot.segment['Components']) == 8

            f.content.mobs.append(mob)

            slot.segment['Components'][0] = first

            assert slot.dir


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
