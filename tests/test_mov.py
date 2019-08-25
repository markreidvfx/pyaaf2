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
import aaf2.mov


class MovTests(unittest.TestCase):
    def test_simple(self):
        pix_fmt = 'yuv420p'
        profile = 'baseline'
        # vcodec = ['-pix_fmt', pix_fmt, '-c:v', 'h264', '-profile:v', profile ]
        vcodec = ['-c:v', 'prores_ks', '-profile:v', '3']

        mov_path = common.generate_mov('mov_simple.mov', overwrite=False, vcodec=vcodec)

        f = aaf2.mov.MOVFile(mov_path)
        f.dump()

        for track in f.tracks:
            if track.media_kind == 'TimeCodeHandle':
                track.media.dump()
                print(track.media_kind)
                print(track.descriptor)

                samples = track.info.sample_table
                print(samples)
                # print(track.media.info.handler)
        # # f.dump()


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
