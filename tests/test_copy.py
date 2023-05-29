from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import unittest

import aaf2
from aaf2 import properties
import common




class AAFCopyTests(unittest.TestCase):

    def compare_objects(self, a, b, skip_some=False):
        for key in a.keys():
            if a[key].format_name() == "Property":
                if key in ("Description", "Name") and skip_some:
                    continue
                else:
                    self.assertEqual(a[key].data, b[key].data, "key = {}".format(key))
            else:
                pa = a[key]
                pb = b[key]

                if isinstance(pa, (properties.StrongRefSetProperty,
                                   properties.WeakRefArrayProperty)):
                    for key, item_a in pa.items():
                        self.assertTrue(key in pb)
                        item_b = pb[key]
                        self.compare_objects(item_a, item_b, skip_some)

                elif isinstance(pa, properties.StrongRefVectorProperty):
                    for item_a, item_b in zip(pa, pb):
                        self.compare_objects(item_a, item_b, skip_some)
                elif isinstance(pa, (properties.StrongRefProperty,
                                     properties.WeakRefProperty)):
                    self.compare_objects(pa.value, pb.value, skip_some)

                elif isinstance(pa, properties.StreamProperty):
                    read_size = a.root.cfb.sector_size
                    sa = pa.open('r')
                    sb = pb.open('r')
                    byte_size = sa.dir.byte_size
                    self.assertEqual(byte_size, sb.dir.byte_size)
                    while byte_size > 0:
                        da = sa.read(read_size)
                        db = sb.read(read_size)
                        self.assertEqual(da, db)
                        byte_size -= len(da)

    def test_mob_copy(self):
        test_file = os.path.join(common.test_files_dir(),"test_file_01.aaf")
        result_file = common.get_test_file('copy_all_mobs.aaf')

        with aaf2.open(test_file, 'r') as a:
            with aaf2.open(result_file, 'w', extensions=False) as b:
                b.dictionary.update(a.dictionary)
                for mob in a.content.mobs:
                    b.content.mobs.append(mob.copy(root=b))

        with aaf2.open(test_file, 'r') as a:
            with aaf2.open(result_file, 'r', extensions=False) as b:
                for mob in a.content.mobs:
                    other_mob = a.content.mobs.get(mob.mob_id, None)
                    self.assertEqual(mob.mob_id, other_mob.mob_id)
                    self.compare_objects(mob, other_mob)

                self.compare_objects(a.dictionary, b.dictionary, skip_some=True)

        result_file = common.get_test_file('copy_mobs_fail.aaf')
        with aaf2.open(test_file, 'r') as a:
            with aaf2.open(result_file, 'w', extensions=False) as b:
                with self.assertRaises(aaf2.exceptions.AAFAttachError):
                    b.content.mobs.append(mob.copy())

    def test_copy_toplevel(self):
        test_file = os.path.join(common.test_files_dir(),"test_file_01.aaf")
        result_file = common.get_test_file('copy_toplevel_mobs.aaf')

        mob_ids = []
        with aaf2.open(test_file, 'r') as a:
            with aaf2.open(result_file, 'w', extensions=False) as b:
                b.dictionary.update(a.dictionary)
                mobs = []

                # gather all the dependant mobs
                for mob in a.content.toplevel():
                    mobs.append(mob)
                    mobs.extend(mob.dependant_mobs())

                for mob in mobs:
                    mob_ids.append(mob.mob_id)
                    b.content.mobs.append(mob.copy(root=b))

        with aaf2.open(test_file, 'r') as a:
            with aaf2.open(result_file, 'r', extensions=False) as b:
                for mob_id in mob_ids:
                    self.assertTrue(mob_id in b.content.mobs)
                    mob_a = a.content.mobs[mob_id]
                    mob_b = a.content.mobs[mob_id]
                    self.compare_objects(mob_a, mob_b)

                self.compare_objects(a.dictionary, b.dictionary, skip_some=True)