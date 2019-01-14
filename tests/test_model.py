from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import aaf2
from uuid import UUID
import uuid
import unittest
import common
import shutil
from aaf2.auid import AUID

def has_duplicate_pid(f):
    pids = []
    for classdef in f.metadict['ClassDefinitions'].values():
        for pdef in classdef['Properties'].values():
            pid = pdef['LocalIdentification'].value
            if pid in pids:
                return True
            pids.append(pid)
    return False

class ModelTests(unittest.TestCase):

    def test_no_root_class(self):

        # make sure we don't write the root_class definition
        result_file = common.get_test_file('root_tess.aaf')
        with aaf2.open(result_file, 'w') as f:
            pass
        root_auid = AUID('b3b398a5-1c90-11d4-8053-080036210804')
        with aaf2.open(result_file, 'r') as f:
            for classdef in f.metadict['ClassDefinitions'].value:
                self.assertFalse(classdef.class_name == "Root")
                self.assertFalse(classdef.auid == root_auid)
                self.assertFalse(classdef.uuid == UUID(bytes_le=bytes(root_auid.bytes_le)))

    def test_register(self):

        result_file = common.get_test_file('register_class.aaf')

        test_classdef_auid = AUID(int=1)
        test_prop_auid = AUID(int=42)
        test_prop_pid = 0xBEEF
        parent_class_name = 'EssenceDescriptor'
        with aaf2.open(result_file, 'w') as f:
            test_classdef = f.metadict.register_classdef("TestClass", test_classdef_auid, parent_class_name, True)
            assert isinstance(test_classdef, aaf2.metadict.ClassDef)
            p = test_classdef.register_propertydef("TheAnswer", test_prop_auid, test_prop_pid, 'aafInt64', True, False)
            assert isinstance(p, aaf2.metadict.PropertyDef)

        with aaf2.open(result_file, 'r') as f:
            parent_classdef = f.metadict.lookup_classdef(parent_class_name)
            test_classdef = f.metadict.lookup_classdef('TestClass')

            self.assertTrue(test_classdef.auid == test_classdef_auid)
            self.assertTrue(test_classdef.uuid == UUID(bytes_le=bytes(test_classdef_auid.bytes_le)))
            self.assertTrue(test_classdef.class_name == "TestClass")
            self.assertTrue(test_classdef.parent is parent_classdef)

            p = test_classdef['Properties'].value[0]
            self.assertTrue(p.auid == test_prop_auid)
            self.assertTrue(p.pid == test_prop_pid)

            self.assertTrue(p.property_name == "TheAnswer")

            prop_typedef = f.metadict.lookup_typedef("aafInt64")
            self.assertTrue(p.typedef is prop_typedef)

    def test_add_extensions(self):
        result_file = common.get_test_file('basic_model.aaf')
        # create a file with basic model

        base_model_dynamic_pids = 0
        with aaf2.open(result_file, 'w', extensions=False) as f:
            for classdef in f.metadict['ClassDefinitions'].values():
                for pdef in classdef['Properties'].values():
                    if pdef['LocalIdentification'].value < 0x8000:
                        base_model_dynamic_pids += 1


        # check there are no extensions
        written_model_dynamic_pids = 0
        with aaf2.open(result_file, 'r') as f:
            for classdef in f.metadict['ClassDefinitions'].values():
                # make sure non of the properties and dynamics
                for pdef in classdef['Properties'].values():
                    if pdef['LocalIdentification'].value < 0x8000:
                        written_model_dynamic_pids +=1

        self.assertTrue(base_model_dynamic_pids == written_model_dynamic_pids)

        # open files 'rw' and add extensions
        with aaf2.open(result_file, 'rw', extensions=True) as f:
            pass

        dynamic_pids = set()
        # check that dynamic properties got added
        with aaf2.open(result_file, 'r') as f:
            for classdef in f.metadict['ClassDefinitions'].values():
                for pdef in classdef['Properties'].values():
                    if pdef['LocalIdentification'].value >= 0x8000:
                        pid = pdef['LocalIdentification'].value
                        self.assertTrue(pid not in dynamic_pids)
                        dynamic_pids.add(pid)

        assert len(dynamic_pids) > 0

    def test_duplicate_pids(self):
        result_file = common.get_test_file('duplicate_pids.aaf')
        with aaf2.open(result_file, 'w', extensions=True) as f:
            self.assertFalse(has_duplicate_pid(f))

    def test_duplicate_pids_add(self):
        result_file = common.get_test_file('duplicate_pids_add.aaf')
        with aaf2.open(result_file, 'w', extensions=False) as f:
            self.assertFalse(has_duplicate_pid(f))

        with aaf2.open(result_file, 'r') as f:
            self.assertFalse(has_duplicate_pid(f))

        with aaf2.open(result_file, 'rw', extensions=True) as f:
            self.assertFalse(has_duplicate_pid(f))

        with aaf2.open(result_file, 'r') as f:
            self.assertFalse(has_duplicate_pid(f))

    def test_duplicate_pids_existing(self):
        result_file = common.get_test_file('duplicate_pids_existing.aaf')
        shutil.copy(common.test_file_01(), result_file)

        with aaf2.open(result_file, 'w', extensions=False) as f:
            self.assertFalse(has_duplicate_pid(f))

        with aaf2.open(result_file, 'r') as f:
            self.assertFalse(has_duplicate_pid(f))

        with aaf2.open(result_file, 'rw', extensions=True) as f:
            self.assertFalse(has_duplicate_pid(f))

        with aaf2.open(result_file, 'r') as f:
            self.assertFalse(has_duplicate_pid(f))

    def test_add_extension_existing(self):
        test_file = common.get_test_file('extension_add_existing.aaf')
        shutil.copy(common.test_file_01(), test_file)

        original_pids = []
        original_classdefs_count = None
        original_typedef_count = None
        with aaf2.open(test_file, 'r') as f:
            original_classdefs_count = len(f.metadict['ClassDefinitions'])
            original_typedef_count = len(f.metadict['TypeDefinitions'])
            for classdef in f.metadict['ClassDefinitions'].values():
                # make sure non of the properties and dynamics
                for pdef in classdef['Properties'].values():
                    pid = pdef['LocalIdentification'].value
                    if pdef['LocalIdentification'].value >= 0x8000:
                        original_pids.append(pid)

        # open files 'rw' and add extensions
        with aaf2.open(test_file, 'rw', extensions=True) as f:
            pass

        all_pids = []
        with aaf2.open(test_file, 'r') as f:
            new_classdefs_count = len(f.metadict['ClassDefinitions'])
            new_typedef_count = len(f.metadict['TypeDefinitions'])
            for classdef in f.metadict['ClassDefinitions'].values():
                for pdef in classdef['Properties'].values():
                    pid = pdef['LocalIdentification'].value
                    # make sure there are no duplicate pids
                    self.assertTrue(pid not in all_pids)
                    all_pids.append(pid)

        self.assertTrue(new_classdefs_count > original_classdefs_count)
        self.assertTrue(new_typedef_count > original_typedef_count)

        # print(new_typedef_count, original_typedef_count)
        # print(new_classdefs_count, original_classdefs_count)


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
