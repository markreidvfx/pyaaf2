from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import unittest

import aaf2
import common


class AAFCopyTests(unittest.TestCase):

    def test_mob_copy(self):
        test_file = os.path.join(common.test_files_dir(),"test_file_01.aaf")
        result_file = common.get_test_file('copy_mobs.aaf')

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

        result_file = common.get_test_file('copy_mobs_fail.aaf')
        with aaf2.open(test_file, 'r') as a:
            with aaf2.open(result_file, 'w', extensions=False) as b:
                with self.assertRaises(aaf2.exceptions.AAFAttachError):
                    b.content.mobs.append(mob.copy())
