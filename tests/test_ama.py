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
from aaf2 import ama

avc_profiles = [('yuv420p', 'baseline'),
                ('yuv420p', 'main'),
                ('yuv420p', 'high'),
                ('yuv422p', 'high422'),
                # ('yuv444p', 'high444')# unsupported in MC?
                ]

prores_profiles = [
    (0, 'proxy'),
    (1, 'LT'),
    (2, 'standard'),
    (3, 'HQ'),
    (4, '4444'),
]


class AMATests(unittest.TestCase):


    def assert_mastermob_valid_edit_spec(self, master_mob, expected_picture_slots, expected_sound_slots):
        """
        Verifies that a MasterMob has all the required elements for the edit spec
        :param master_mob:
        :return:
        """
        physical_sound_tracks = []
        self.assertIsNotNone(master_mob, "Failed to find MasterMob by saved ID")
        self.assertEqual(len(master_mob.slots), expected_picture_slots + expected_sound_slots,
                         "Failed to find correct number of slots in MasterMob")

        sound_slots = list([slot for slot in master_mob.slots if slot.segment.media_kind == 'Sound'])
        picture_slots = list([slot for slot in master_mob.slots if slot.segment.media_kind == 'Picture'])

        self.assertEqual(len(sound_slots), expected_sound_slots, "MasterMob has incorrect number of sound slots")
        self.assertEqual(len(picture_slots), expected_picture_slots, "MasterMon has incorrect number of picture slots")

        file_source_mob = None
        for mob_slot in master_mob.slots:
            self.assertIsInstance(mob_slot.segment, aaf2.components.Sequence, "MobSlot has no Sequence")
            self.assertEqual(len(mob_slot.segment.components), 1, "Mob slot must have exactly one component")
            self.assertIsInstance(mob_slot.segment.components[0], aaf2.components.SourceClip,
                                  "Mob slot sequence has incorrect component type")
            source_clip = mob_slot.segment.components[0]

            self.assertIsNotNone(source_clip.start, "SourceClip does not have a start time")
            self.assertIsNotNone(source_clip.length, "SourceClip does not have a length time")
            self.assertTrue(source_clip.length > 0, "SourceClip appears to have invalid length")

            self.assertIsNotNone(source_clip.mob, "MasterMob SourceClip does not have a linked SourceMob")
            if file_source_mob is None:
                file_source_mob = source_clip.mob
            else:
                self.assertEqual(source_clip.mob, file_source_mob,
                                 "MasterMob slots appear to reference different SourceMOBs")

            if mob_slot.media_kind == 'Sound':
                physical_sound_tracks.append(int(mob_slot['PhysicalTrackNumber'].value))

            self.assertEqual(len(source_clip.mob.slots), expected_picture_slots + expected_sound_slots,
                             "SourceMob has incorrect number of slots")

            tape_source_clip = file_source_mob.slot_at(mob_slot.slot_id).segment.components[0]
            self.assertIsInstance(tape_source_clip, aaf2.components.SourceClip,
                                  "File SourceMob does not have a tape SourceMob")

            if isinstance(tape_source_clip.mob.descriptor, aaf2.essence.TapeDescriptor):
                pass
            elif isinstance(tape_source_clip.mob.descriptor, aaf2.essence.ImportDescriptor):
                pass
            else:
                self.fail("Tape SourceMob descriptor must be either a TapeDescriptor or ImportDescriptor")

        for chan_num in range(expected_sound_slots):
            self.assertEqual(physical_sound_tracks.count(chan_num + 1), 1,
                             "Incorrect PhysicalTrackNumber property on master mob slot")

        self.assertEqual(len(physical_sound_tracks), expected_sound_slots,
                         "Incorrect PhysicalTrackNumber count on master mob slot")

    def assert_valid_multiple_descriptor(self, mastermob, expected_audio_channel_count):
        for mob_slot in mastermob.slots:
            source_clip = mob_slot.segment.components[0]
            self.assertIsNotNone(source_clip.mob.comments['Video'],
                                 "SourceMob must have a value for 'Video' comment")

            self.assertEqual(len(source_clip.mob.descriptor['FileDescriptors'].value), 2,
                             "SourceMob's descriptor has incorrect 'FileDescriptor' property value")

            self.assertIsInstance(source_clip.mob.descriptor, aaf2.essence.MultipleDescriptor,
                                  "SourceClip Mob has incorrect descriptor")

            for descriptor in source_clip.mob.descriptor['FileDescriptors'].value:
                self.assertIsNotNone(descriptor['Locator'].value,
                                     "SourceClip descriptor not properly formatted")

                locators = descriptor['Locator'].value
                self.assertTrue(len(locators) >= 1)

                if isinstance(descriptor, aaf2.essence.PCMDescriptor):
                    self.assertEqual(descriptor['Channels'].value, expected_audio_channel_count,
                                     "SourceClip descriptor not properly formatted")
                elif isinstance(descriptor, aaf2.essence.CDCIDescriptor):
                    self.assertIsInstance(descriptor['ComponentWidth'].value, int)
                    self.assertIsInstance(descriptor['HorizontalSubsampling'].value, int)

                else:
                    self.fail("Encountered unexpected essence descriptor")

    def test_monoaural_wav(self):
        new_file = os.path.join(common.sandbox(), 'ama_wav.aaf')
        with aaf2.open(new_file, 'w') as f:
            wavfile = common.generate_pcm_audio_mono('test_ama.wav', fmt='wav')
            meta = common.probe(wavfile)
            mobs = ama.create_media_link(f, wavfile, meta)
            self.assertTrue(len(mobs), 3)

        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)
            self.assertTrue(len(f.content.mobs) == 3)
            self.assertTrue(len(list(f.content.mastermobs())) == 1)
            master_mob = next(f.content.mastermobs())
            self.assert_mastermob_valid_edit_spec(master_mob=master_mob, expected_sound_slots=1,
                                                  expected_picture_slots=0)
            self.assertEqual(len(master_mob.slots), 1, "MasterMob should only have one slot")
            self.assertEqual(master_mob.slots[0].media_kind, 'Sound', "MasterMob slot has incorrect media_kind")
            source_clip = master_mob.slots[0].segment.components[0]
            descriptor = source_clip.mob.descriptor
            self.assertIsNotNone(descriptor, "File SourceMob has no WAVEDescriptor")
            self.assertIsInstance(descriptor, aaf2.essence.WAVEDescriptor, "File SourceMob has no WAVEDescriptor")
            self.assertIsNotNone(descriptor['Summary'].value, "WAVEDescriptor missing required 'Summary' property")

    def test_monoaural_aiff(self):
        new_file = os.path.join(common.sandbox(), 'ama_aiff.aaf')
        with aaf2.open(new_file, 'w') as f:
            aiff_file = common.generate_pcm_audio_mono('test_ama_aiff', fmt='aiff')
            meta = common.probe(aiff_file)
            mobs = ama.create_media_link(f, aiff_file, meta)
            self.assertTrue( len(mobs), 3)

        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)
            self.assertTrue(len(f.content.mobs) == 3)
            self.assertTrue(len(list(f.content.mastermobs())) == 1)
            master_mob = next(f.content.mastermobs())
            self.assert_mastermob_valid_edit_spec(master_mob=master_mob, expected_sound_slots=1,
                                                  expected_picture_slots=0)
            self.assertEqual(len(master_mob.slots), 1, "MasterMob should only have one slot")
            self.assertEqual(master_mob.slots[0].media_kind, 'Sound', "MasterMob slot has incorrect media_kind")
            source_clip = master_mob.slots[0].segment.components[0]
            descriptor = source_clip.mob.descriptor
            self.assertIsNotNone(descriptor, "File SourceMob has no WAVEDescriptor")
            self.assertIsInstance(descriptor, aaf2.essence.AIFCDescriptor, "File SourceMob has no AIFCDescriptor")
            self.assertIsNotNone(descriptor['Summary'].value, "AIFCDescriptor missing required 'Summary' property")

    def test_avc_mov(self):
        new_file = os.path.join(common.sandbox(), 'avc_mov.aaf')

        audio_channel_count = 2
        created_mastermob_ids = []
        with aaf2.open(new_file, 'w') as f:
            for (pix_fmt, profile) in avc_profiles:
                vcodec = ['-pix_fmt', pix_fmt, '-c:v', 'h264', '-profile:v', profile]

                mov = common.generate_mov('ama_avc_%s.mov' % profile, overwrite=False, vcodec=vcodec,
                                          audio_channels=audio_channel_count)
                meta = common.probe(mov)
                # print(meta['streams'][0]['profile'])

                mobs = f.content.create_ama_link(mov, meta)
                self.assertEqual(len(mobs), 3)
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
                mastermob = next((mob for mob in f.content.mobs if mob.mob_id == mastermob_id), None)
                self.assert_mastermob_valid_edit_spec(mastermob, expected_picture_slots=1, expected_sound_slots=2)
                self.assert_valid_multiple_descriptor(mastermob, audio_channel_count)

    def test_prores(self):
        new_file = os.path.join(common.sandbox(), 'prores_mov.aaf')
        created_mastermob_ids = []
        with aaf2.open(new_file, 'w') as f:

            for profile, name in prores_profiles:
                vcodec = ['-c:v', 'prores_ks', '-profile:v', str(profile)]
                mov = common.generate_mov('ama_prores_%s.mov' % (name,), overwrite=False, vcodec=vcodec,
                                          audio_channels=2)
                meta = common.probe(mov)
                mobs = ama.create_media_link(f, mov, meta)
                self.assertEqual(len(mobs), 3, "create_ama_link must return exactly three mobs")
                created_mastermob_ids.append(mobs[0].mob_id)

        with aaf2.open(new_file, 'r') as f:
            common.walk_aaf(f.root)
            self.assertEqual(len(f.content.mobs), len(prores_profiles) * 3,
                             "Failed to create exactly three MOBs per prores_profile")
            self.assertEqual(len(list(f.content.mastermobs())), len(prores_profiles),
                             "Failed to create exactly one MasterMOB per prores_profile")

            for mastermob_id in created_mastermob_ids:
                mastermob = next((mob for mob in f.content.mobs if mob.mob_id == mastermob_id), None)
                self.assert_mastermob_valid_edit_spec(mastermob, expected_picture_slots=1, expected_sound_slots=2)
                self.assert_valid_multiple_descriptor(mastermob, 2)


if __name__ == "__main__":
    import logging

    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
