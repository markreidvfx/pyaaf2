from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import unittest
import common
import aaf2
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

    def test_wav(self):
        new_file = os.path.join(common.sandbox(), 'ama_wav.aaf')
        with aaf2.open(new_file, 'w') as f:

            wavfile = common.generate_pcm_audio_mono('test_ama.wav', fmt='wav')
            meta = common.probe(wavfile)
            # print(meta['streams'][0]['profile'])

            mobs = f.content.create_ama_link(wavfile, meta)
            self.assertTrue(len(mobs),3)


        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)
            self.assertTrue(len(f.content.mobs) == 3)


    def test_avc_mov(self):
        new_file = os.path.join(common.sandbox(), 'avc_mov.aaf')
        with aaf2.open(new_file, 'w') as f:

            a_chan_count = 2
            created_mastermob_ids = []
            for (pix_fmt, profile) in avc_profiles:
                vcodec = ['-pix_fmt', pix_fmt, '-c:v', 'h264', '-profile:v', profile ]

                mov = common.generate_mov('ama_avc_%s.mov' % profile, overwrite=False, vcodec=vcodec, audio_channels=a_chan_count)
                meta = common.probe(mov)
                # print(meta['streams'][0]['profile'])

                mobs = f.content.create_ama_link(mov, meta)
                self.assertEqual(len(mobs),3)
                self.assertIsInstance(mobs[0], aaf2.mobs.MasterMob)
                self.assertIsInstance(mobs[1], aaf2.mobs.SourceMob)
                self.assertIsInstance(mobs[2], aaf2.mobs.SourceMob)
                created_mastermob_ids.append(mobs[0].mob_id)


        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)
            self.assertEqual(len(f.content.mobs), len(avc_profiles) * 3,
                             "Failed to create exactly three MOBs per avc_profile")
            self.assertEqual(len(list(f.content.mastermobs())), len(avc_profiles),
                             "Failed to create exactly one MasterMOB per avc_profile")


            for mastermob_id in created_mastermob_ids:
                physical_sound_tracks = []
                mastermob = next( (mob for mob in f.content.mobs if mob.mob_id == mastermob_id) ,None)
                self.assertIsNotNone(mastermob, "Failed to find MasterMob by saved ID")
                self.assertEqual(len(mastermob.slots), 3, "Failed to find correct number of slots in MasterMob")

                sound_slots = list([slot for slot in mastermob.slots if slot.segment.media_kind == 'Sound'])
                picture_slots = list([slot for slot in mastermob.slots if slot.segment.media_kind == 'Picture'])

                self.assertEqual(len(sound_slots), 2)
                self.assertEqual(len(picture_slots), 1)

                source_mob = None
                for mobslot in mastermob.slots:
                    self.assertIsNotNone(mobslot.segment)
                    self.assertIsInstance(mobslot.segment, aaf2.components.Sequence)
                    self.assertEqual(len(mobslot.segment.components), 1)
                    self.assertIsInstance(mobslot.segment.components[0], aaf2.components.SourceClip)
                    source_clip = mobslot.segment.components[0]
                    self.assertIsNotNone(source_clip.mob)
                    if source_mob is None:
                        source_mob = source_clip.mob
                    else:
                        self.assertEqual(source_clip.mob, source_mob,
                                         "MasterMob slots appear to reference different SourceMOBs")

                    if mobslot.media_kind == 'Sound':
                        physical_sound_tracks.append(int(mobslot['PhysicalTrackNumber'].value))

                    self.assertIsInstance(source_clip.mob.descriptor, aaf2.essence.MultipleDescriptor)
                    self.assertEqual(len(source_clip.mob.slots),3)
                    self.assertEqual(len(source_clip.mob.descriptor['FileDescriptors'].value), 2)
                    for descriptor in source_clip.mob.descriptor['FileDescriptors'].value:
                        self.assertIsNotNone(descriptor['Locator'].value)
                        if isinstance(descriptor,aaf2.essence.PCMDescriptor):
                            self.assertEqual(descriptor['Channels'].value, a_chan_count)
                        elif isinstance(descriptor, aaf2.essence.CDCIDescriptor):
                            continue
                        else:
                            self.fail("Encountered unexpected essence descriptor")

                self.assertEqual(physical_sound_tracks.count(1), 1)
                self.assertEqual(physical_sound_tracks.count(2), 1)
                self.assertEqual(len(physical_sound_tracks), 2)

    # def test_mxf(self):
    #     new_file = os.path.join(common.sandbox(), 'prores_mxf.aaf')
    #
    #     with aaf2.open(new_file, 'w') as f:
    #         vcodec = ['-c:v','prores','-profile:v','0']
    #         mxf_mov = common.generate_dnxhd(profile_name='dnx_1080p_36_23.97',name=new_file,frames=240,fmt='mxf')
    #         meta = common.probe(mxf_mov)
    #         mobs = f.content.create_ama_link(mxf_mov,meta)

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
