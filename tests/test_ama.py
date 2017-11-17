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
import common
import aaf2
from aaf2 import video, audio, mobid, mobs, essence

class AMATests(unittest.TestCase):


    def test_mov(self):

        mov = common.generate_mov('ama.mov', overwrite=False)
        meta = common.probe(mov)

        new_file = os.path.join(common.sandbox(), 'mxf_link_video.aaf')

        with aaf2.open(new_file, 'w') as f:
            f.content.create_ama_link(mov, meta)


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
