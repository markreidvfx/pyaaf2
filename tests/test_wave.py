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


class WAVETests(unittest.TestCase):
    
    def test_wav_link(self):
        test_outfile = os.path.join(common.sandbox(), 'wav_link.aaf')

        test_link_targets = [
            common.generate_pcm_audio_mono('testmono', sample_rate=48000, duration=10,
                sample_format='pcm_s16le', fmt='wav'),
            common.generate_pcm_audio_mono('testmono24', sample_rate=48000, duration=10,
                sample_format='pcm_s24le', fmt='wav'),
            common.generate_pcm_audio_stereo('testmono', sample_rate=48000, duration=10,
                sample_format='pcm_s24le', fmt='wav')
                ]

        with aaf2.open(test_outfile,'w') as f:
            for target in test_link_targets:
                meta = common.probe(target)
                mobs = f.content.link_external_wav(meta)
                

if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
