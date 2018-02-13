from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import aaf2

import unittest

import common
import datetime

class TaggedValueTests(unittest.TestCase):


    def test_tagged_value(self):
        result_file = common.get_test_file('tagged_value.aaf')

        with aaf2.open(result_file, 'w') as f:

            t1 = f.create.TaggedValue("name1", 3221)

            typedef = f.dictionary.lookup_typedef("aafInt32")
            assert t1.value_typedef == typedef

            t2 =  f.create.TaggedValue("name2", 45, 'aafInt64')

            typedef = f.dictionary.lookup_typedef("aafInt64")
            assert t2.value_typedef == typedef

            t3 = f.create.TaggedValue()

            t3.name = "name3"
            t3.encode_value("24000/10001", 'Rational')

            typedef = f.dictionary.lookup_typedef("Rational")
            assert t3.value_typedef == typedef



if __name__ == "__main__":
    unittest.main()
