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
import shutil
import common
import aaf2
from aaf2 import exceptions

import binascii

def stream_checksum(s):
    crc = 0
    f = s.open('r')
    while True:
        data = f.read(4092)
        if not data:
            break

        crc = binascii.crc32(data, crc) & 0xffffffff

    path = f.dir.path()

    return path, crc


class ImportTests(unittest.TestCase):

    def test_attach(self):
        result_file = common.get_test_file('attach.aaf')
        with aaf2.open(result_file, 'w') as f:

            mob = f.create.MasterMob()
            mob_id = mob.mob_id
            f.content.mobs.append(mob)

            with self.assertRaises(exceptions.AAFAttachError):
                f.content.mobs.append(mob)

            # dettach
            mob = f.content.mobs.pop(mob_id)
            assert mob
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

    def test_reattach(self):
        new_file = os.path.join(common.sandbox(), 'test_reattach.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        mob_ids = []
        original_child_count = 0

        checksums = {}

        with aaf2.open(new_file, 'r+') as f:
            mobs = f.content['Mobs'].value

            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is not None
                    original_child_count += 1

                    for item in streams:
                        path, crc = stream_checksum(item)
                        path = path.replace(m.dir.path(), str(m.mob_id))
                        checksums[path] = crc

            assert original_child_count > len(mobs)

            mob_ids = [m.mob_id for m in mobs]
            f.content['Mobs'].value = []

            child_count = 0
            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is None
                    child_count += 1

            assert child_count == original_child_count

            f.content['Mobs'].value = mobs
            child_count = 0
            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is not None
                    child_count += 1
                    for item in streams:
                        path, crc = stream_checksum(item)
                        path = path.replace(m.dir.path(), str(m.mob_id))
                        assert checksums[path] == crc

            assert child_count == original_child_count

        with aaf2.open(new_file, 'r') as f:
            for mob_id in mob_ids:
                assert f.content.mobs.get(mob_id, None) is not None

            mobs = f.content['Mobs'].value
            child_count = 0
            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is not None
                    child_count += 1

                    for item in streams:
                        path, crc = stream_checksum(item)
                        path = path.replace(m.dir.path(), str(m.mob_id))
                        assert checksums[path] == crc

            assert child_count == original_child_count

    def test_reattach512(self):
        new_file = os.path.join(common.sandbox(), 'test_reattach512.aaf')
        test_file = common.test_file_512()
        shutil.copy(test_file, new_file)

        mob_ids = []
        original_child_count = 0

        with aaf2.open(new_file, 'r+') as f:
            mobs = f.content['Mobs'].value

            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is not None
                    original_child_count += 1

            assert original_child_count > len(mobs)

            mob_ids = [m.mob_id for m in mobs]
            f.content['Mobs'].value = []

            child_count = 0
            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is None
                    child_count += 1

            assert child_count == original_child_count

            f.content['Mobs'].value = mobs
            child_count = 0
            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is not None
                    child_count += 1

            assert child_count == original_child_count

        with aaf2.open(new_file, 'r') as f:
            for mob_id in mob_ids:
                assert f.content.mobs.get(mob_id, None) is not None

            mobs = f.content['Mobs'].value
            child_count = 0
            for m in mobs:
                for item, streams in m.walk_references():
                    assert item.dir is not None
                    child_count += 1

            assert child_count == original_child_count

    def test_mob_id_swap(self):
        new_file = os.path.join(common.sandbox(), 'swap_id.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)
        new_mobid =aaf2.mobid.MobID.new()
        with aaf2.open(new_file, 'rw') as f:
            comp = next(f.content.compositionmobs())
            comp.mob_id = new_mobid

        with aaf2.open(new_file, 'r') as f:
            comp = next(f.content.compositionmobs())
            assert comp.mob_id == new_mobid

    def test_rewrite(self):
        new_file = os.path.join(common.sandbox(), 'test_rewrite.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        prop_count = {}

        with aaf2.open(new_file, 'rw') as f:
            for obj, streams in f.root.walk_references():
                f.manager.add_modified(obj)
                prop_count[obj.dir.path()] = len(list(obj.properties()))

        with aaf2.open(new_file, 'r') as f:
            for obj, streams in f.root.walk_references():
                path = obj.dir.path()
                assert len(list(obj.properties())) == prop_count[path]

    def test_rewrite512(self):
        new_file = os.path.join(common.sandbox(), 'test_rewrite512.aaf')
        test_file = common.test_file_512()
        shutil.copy(test_file, new_file)

        prop_count = {}

        with aaf2.open(new_file, 'rw') as f:
            for obj, streams in f.root.walk_references():
                f.manager.add_modified(obj)
                prop_count[obj.dir.path()] = len(list(obj.properties()))

        with aaf2.open(new_file, 'r') as f:
            for obj, streams in f.root.walk_references():
                path = obj.dir.path()
                assert len(list(obj.properties())) == prop_count[path]

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
