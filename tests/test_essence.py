from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import unittest
import common
import os
import aaf2

class EssenceTests(unittest.TestCase):

    def test_create(self):
        new_file = os.path.join(common.sandbox(), 'create_essence.aaf')
        test_data = b"Essence Data!!"
        mob_id =  aaf2.mobid.MobID()
        mob_id.int = 1

        with aaf2.open(new_file, 'w') as f:
            e = f.create.EssenceData()
            e.id = mob_id
            f.content.add_essencedata(e)
            stream = e.open("w")
            stream.write(test_data)

        with aaf2.open(new_file, 'r') as f:
            e = next(f.content.essencedata())
            assert e.id == mob_id
            stream = e.open("r")
            assert stream.read() == test_data






if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
