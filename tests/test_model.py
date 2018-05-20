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

class ModelTests(unittest.TestCase):

    def test_no_root_class(self):

        # make sure we don't write the root_class definition
        result_file = common.get_test_file('root_tess.aaf')
        with aaf2.open(result_file, 'w') as f:
            pass
        root_uuid = UUID('b3b398a5-1c90-11d4-8053-080036210804')
        with aaf2.open(result_file, 'r') as f:
            for classdef in f.metadict['ClassDefinitions'].value:
                self.assertFalse(classdef.class_name == "Root")
                self.assertFalse(classdef.uuid == root_uuid)

    def test_register(self):

        result_file = common.get_test_file('register_class.aaf')

        test_classdef_uuid = UUID(int=1)
        test_prop_uuid = UUID(int=42)
        test_prop_pid = 0xBEEF
        parent_class_name = 'EssenceDescriptor'
        with aaf2.open(result_file, 'w') as f:
            test_classdef = f.metadict.register_classdef("TestClass", test_classdef_uuid, parent_class_name, True)
            assert isinstance(test_classdef, aaf2.metadict.ClassDef)
            p = test_classdef.register_propertydef("TheAnswer", test_prop_uuid, test_prop_pid, 'aafInt64', True, False)
            assert isinstance(p, aaf2.metadict.PropertyDef)

        with aaf2.open(result_file, 'r') as f:
            parent_classdef = f.metadict.lookup_classdef(parent_class_name)
            test_classdef = f.metadict.lookup_classdef('TestClass')

            self.assertTrue(test_classdef.uuid == test_classdef_uuid)
            self.assertTrue(test_classdef.class_name == "TestClass")
            self.assertTrue(test_classdef.parent is parent_classdef)

            p = test_classdef['Properties'].value[0]
            self.assertTrue(p.uuid == test_prop_uuid)
            self.assertTrue(p.pid == test_prop_pid)

            self.assertTrue(p.property_name == "TheAnswer")

            prop_typedef = f.metadict.lookup_typedef("aafInt64")
            self.assertTrue(p.typedef is prop_typedef)


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
