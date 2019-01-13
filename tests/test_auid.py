from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2.auid import AUID
from uuid import UUID
import uuid
import unittest

class MobIDTests(unittest.TestCase):

    def test_basic(self):
        s = "0d010101-0101-2100-060e-2b3402060101"
        v = AUID(s)
        u = UUID(s)
        assert str(v) == s
        assert str(v.uuid) == s
        assert v.uuid == u

    def test_be(self):
        s = "0d010101-0101-2100-060e-2b3402060101"
        v = AUID(s)
        u = UUID(s)
        assert v.uuid.bytes == v.bytes_be

    def test_int(self):
        s = "0d010101-0101-2100-060e-2b3402060101"
        v = AUID(s)
        u = UUID(s)
        assert v.int == u.int

        v = AUID(int=100)
        u = UUID(int=100)
        assert v.int == u.int
        for i in range(10):
            u = uuid.uuid4()
            a = AUID(int= u.int)
            assert u.int == a.int

    def test_noargs(self):
        # expected behavour matches uuid.py
        with self.assertRaises(TypeError):
            AUID()

        # print(v.int)

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
