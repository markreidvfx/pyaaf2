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

class MXFTests(unittest.TestCase):


    def test_basic_video_link(self):
        profile_name = 'dnx_1080p_36_23.97'
        video_sample = common.generate_dnxhd(profile_name, "mxf_link_video.mxf", 10, fmt='mxf_opatom')

        meta = common.probe(video_sample)
        video_mob_id = mobid.MobID(meta['format']['tags']['material_package_umid'])
        video_source_mob_id = mobid.MobID(meta['streams'][0]['tags']['file_package_umid'])

        new_file = os.path.join(common.sandbox(), 'mxf_link_video.aaf')

        with aaf2.open(new_file, 'w') as f:
            f.content.link_external_mxf(video_sample)

        with aaf2.open(new_file, 'r') as f:
            assert len(f.content.mobs) == 2
            for mob in f.content.mobs:
                if isinstance(mob, mobs.MasterMob):
                    assert mob.mob_id == video_mob_id
                elif isinstance(mob, mobs.SourceMob):
                    if isinstance(mob.descriptor, essence.CDCIDescriptor):
                        assert mob.mob_id == video_source_mob_id

    def test_basic_audio_link(self):

        audio_profile_name = 'pcm_48000_s24le'
        sample_format = audio.pcm_profiles[audio_profile_name]['sample_format']
        sample_rate = audio.pcm_profiles[audio_profile_name]['sample_rate']
        audio_duration = 1

        audio_sample = common.generate_pcm_audio_mono(audio_profile_name, sample_format=sample_format,
                         sample_rate=sample_rate, duration=audio_duration, fmt='mxf_opatom')

        meta = common.probe(audio_sample)
        audio_mob_id = mobid.MobID(meta['format']['tags']['material_package_umid'])
        audio_source_mob_id = mobid.MobID(meta['streams'][0]['tags']['file_package_umid'])

        new_file = os.path.join(common.sandbox(), 'mxf_link_audio.aaf')

        with aaf2.open(new_file, 'w') as f:
            f.content.link_external_mxf(audio_sample)

        with aaf2.open(new_file, 'r') as f:
            assert len(f.content.mobs) == 2
            for mob in f.content.mobs:
                if isinstance(mob, mobs.MasterMob):
                    assert mob.mob_id == audio_mob_id
                elif isinstance(mob, mobs.SourceMob):
                    if isinstance(mob.descriptor, essence.PCMDescriptor):
                        assert mob.mob_id == audio_source_mob_id


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
