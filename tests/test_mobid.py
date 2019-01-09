from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2.mobid import MobID
from uuid import UUID
from aaf2.auid import AUID
import uuid
import unittest

class MobIDTests(unittest.TestCase):
    def test_mob_id(self):
        m = MobID.new()
        material_uuid = AUID("52c02cd8-6801-4806-986a-b68c0a0cf9d3")
        m.material = material_uuid
        m_str = "urn:smpte:umid:060a2b34.01010105.01010f20.13000000.52c02cd8.68014806.986ab68c.0a0cf9d3"

        m2 = MobID(str(m))

        assert m == m2
        m2 = MobID(bytes_le=m.bytes_le)
        assert m == m2
        assert m.int == m2.int

        assert m == MobID(m_str)
        assert hash(m) == hash(m2)
        assert str(m) == m_str

        assert m.material == material_uuid

    def test_int(self):

        for i in range(1000):
            m = MobID()
            m.int = i
            assert m.int == i

    def test_material_id(self):
        for i in range(10000):
            material = AUID(int=i)
            m = MobID(int=i)
            assert m.material == material

        for i in range(100):
            material = uuid.uuid4()
            m = MobID.new()
            m.material = material
            assert m.material == material




if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
