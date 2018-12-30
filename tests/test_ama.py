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
                #('yuv444p', 'high444')# unsupported in MC?
                ]


prores_profiles = [
(0, 'proxy'),
(1, 'LT'),
(2, 'standard'),
(3, 'HQ'),
(4, '4444'),
]

class AMATests(unittest.TestCase):


    def test_avc_mov(self):

        new_file = os.path.join(common.sandbox(), 'avc_mov.aaf')
        with aaf2.open(new_file, 'w') as f:

            for (pix_fmt, profile) in avc_profiles:
                vcodec = ['-pix_fmt', pix_fmt, '-c:v', 'h264', '-profile:v', profile ]

                mov = common.generate_mov('ama_avc_%s.mov' % profile, overwrite=False, vcodec=vcodec)
                meta = common.probe(mov)
                # print(meta['streams'][0]['profile'])

                mobs = f.content.create_ama_link(mov, meta)


        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)

    def test_prores(self):

        new_file = os.path.join(common.sandbox(), 'prores_mov.aaf')
        with aaf2.open(new_file, 'w') as f:

            for profile, name in prores_profiles:
                vcodec = ['-c:v', 'prores_ks', '-profile:v', str(profile)]
                mov = common.generate_mov('ama_prores_%s.mov' % (name,), overwrite=False, vcodec=vcodec)
                meta = common.probe(mov)
                mobs = f.content.create_ama_link(mov, meta)
            # for (pix_fmt, profile) in avc_profiles:

        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
