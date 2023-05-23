from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import os
import unittest
import aaf2
from aaf2.file import AAFFile
from aaf2 import properties

import common
import shutil

class AAFTests(unittest.TestCase):


    def test_walk_all(self):
        test_file = os.path.join(common.test_files_dir(),"test_file_01.aaf")
        with AAFFile(test_file) as f:
            common.walk_aaf(f.root)

    def test_save_as(self):

        new_file = os.path.join(common.sandbox(), 'save_r+.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        with aaf2.open(new_file, 'r+') as f:
            f.save()


        # should contents compare!
        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)

    def test_exit_with_exception_no_save(self):
        new_file = os.path.join(common.sandbox(), 'test_exit_with_exception_no_save.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        test_mob_id = None
        with self.assertRaises(ValueError):
            with aaf2.open(new_file, 'r+') as f:
                mob = f.create.MasterMob("TestExitMob")
                test_mob_id = mob.mob_id
                f.content.mobs.append(mob)

                raise ValueError('asd')

        self.assertTrue(f.f.closed)
        self.assertFalse(f.is_open)
        self.assertFalse(f.cfb.is_open)

        with open(test_file, 'rb') as testFile:
            with open(new_file, 'rb') as newFile:
                self.assertNotEqual(testFile.read(), newFile.read())

        with aaf2.open(new_file, 'r') as f:
            # Make sure that the file can still be opened with aaf2.open
            # and that the save method wasn't run.
            self.assertIsNone(f.content.mobs.get(test_mob_id, None))

    def test_exit_with_exception_with_save(self):

        new_file = os.path.join(common.sandbox(), 'test_exit_with_exception_with_save.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        test_mob_id = None

        with self.assertRaises(ValueError):
            with aaf2.open(new_file, 'r+') as f:
                mob = f.create.MasterMob("TestExitMob")
                test_mob_id = mob.mob_id
                f.content.mobs.append(mob)

                f.save()

                raise ValueError('asd')

        self.assertTrue(f.f.closed)
        self.assertFalse(f.is_open)
        self.assertFalse(f.cfb.is_open)

        with open(test_file, 'rb') as testFile:
            with open(new_file, 'rb') as newFile:
                self.assertNotEqual(testFile.read(), newFile.read())

        with aaf2.open(new_file, 'r') as f:
            # Make sure that the file can still be opened with aaf2.open
            # and that the save method wasn't run.
            for mob in f.content.mobs:
                print(mob)
            self.assertIsNotNone(f.content.mobs.get(test_mob_id, None))

    def test_exit_with_internal_exception(self):
        """This scenario is a bad situation... explosion
        Exercise the scenario where no exception occurs inside with with block, but
        an exception occurs during the exit phase of the context manager.
        """

        new_file = os.path.join(common.sandbox(), 'test_exit_with_internal_exception.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        with self.assertRaises(RuntimeError):
            with aaf2.open(new_file, 'r+') as f:
                def mock(*args, **kwargs):
                    raise RuntimeError('asd')

                # This will result in a corrupted file
                f.cfb.close = mock

                # mobs = f.content.mobs
                mob = f.create.MasterMob("TestExitMob")
                f.content.mobs.append(mob)

                f.save()

        self.assertFalse(f.f.closed)
        self.assertTrue(f.is_open)
        self.assertTrue(f.cfb.is_open)

        with open(test_file, 'rb') as testFile:
            with open(new_file, 'rb') as newFile:
                self.assertNotEqual(testFile.read(), newFile.read())

        with self.assertRaises(IndexError):
            # new_file is now corrupted.
            with aaf2.open(new_file, 'r') as f:
                pass

    def test_exit_with_internal_and_external_exception(self):
        # Exception occurs in with block and also in the except clause
        # while closing file descriptors.

        new_file = os.path.join(common.sandbox(), 'test_exit_with_internal_and_external_exception.aaf')
        test_file = common.test_file_01()
        shutil.copy(test_file, new_file)

        # Notice how the exception propagated is not a ValueError.
        with self.assertRaises(RuntimeError):
            with aaf2.open(new_file, 'r+') as f:
                def mock(*args, **kwargs):
                    raise RuntimeError('asd')

                # This will result in a corrupted file
                f.cfb.close = mock

                # mobs = f.content.mobs
                mob = f.create.MasterMob("TestExitMob")
                f.content.mobs.append(mob)

                f.save()

                raise ValueError('asd')

        # And also the file is still closed even if the cfb failed to be closed.
        self.assertTrue(f.f.closed)
        self.assertFalse(f.is_open)
        self.assertTrue(f.cfb.is_open)

        with open(test_file, 'rb') as testFile:
            with open(new_file, 'rb') as newFile:
                self.assertNotEqual(testFile.read(), newFile.read())

        with self.assertRaises(IndexError):
            # new_file is now corrupted.
            with aaf2.open(new_file, 'r') as f:
                pass

    def test_raise_on_close_in_except(self):
        # Test that AAFFile.f.close exceptions are propagated to
        # the user's code.
        with self.assertRaises(RuntimeError):
            with aaf2.open() as fd:
                def mock(*args, **kwargs):
                    raise RuntimeError('asd')

                originalClose = fd.f.close
                fd.f.close = mock
                raise ValueError('asd')

        originalClose()

    def test_save_after_close(self):
        aaf_file = aaf2.open()
        aaf_file.close()
        with self.assertRaises(IOError):
            aaf_file.save()


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
