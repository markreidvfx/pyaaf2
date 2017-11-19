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
from uuid import UUID
from aaf2 import video, audio, mobid, mobs, essence

avc_profiles = [('yuv420p', 'baseline'),
                ('yuv420p', 'main'),
                ('yuv420p', 'high'),
                ('yuv422p', 'high422'),
                ('yuv444p', 'high444')]

class AMATests(unittest.TestCase):


    def test_avc_mov(self):

        new_file = os.path.join(common.sandbox(), 'ama_mov.aaf')
        with aaf2.open(new_file, 'w') as f:

            for (pix_fmt, profile) in avc_profiles:
                vcodec = ['-pix_fmt', pix_fmt, '-c:v', 'h264', '-profile:v', profile ]

                mov = common.generate_mov('ama_%s.mov' % profile, overwrite=True, vcodec=vcodec)
                meta = common.probe(mov)
                # print(meta['streams'][0]['profile'])

                mobs = f.content.create_ama_link(mov, meta)

        # with aaf2.open(new_file, 'r') as f:
        #     f.content.dump()

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
