from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import unittest
import aaf2
import common

class TestCreateSequence(unittest.TestCase):

    def test_create_sequence(self):

        result_file = common.get_test_file('create_sequence.aaf')
        mob_count = 0
        components = 0

        with aaf2.open(result_file, "w")  as f:

            video_rate = " 30000/1001"

            comp_mob = f.create.CompositionMob()
            sequence = f.create.Sequence(media_kind="picture")

            timeline_slot = comp_mob.create_timeline_slot(video_rate)
            timeline_slot.segment= sequence

            f.content.mobs.append(comp_mob)

            length = 60 * 30
            filler_len = 100
            timecode_fps = 30
            mob_count += 1

            test_path = "some_path.mov"

            for i in range(10):

                # Make the Tape MOB
                tape_mob = f.create.SourceMob()
                tape_name = "tape_name"
                tape_slot, tape_timecode_slot = tape_mob.create_tape_slots(tape_name, video_rate, timecode_fps)
                tape_slot.segment.length = length

                f.content.mobs.append(tape_mob)
                mob_count += 1
                # Make a FileMob
                file_mob = f.create.SourceMob()

                # Make a locator
                loc = f.create.NetworkLocator()
                loc['URLString'].value = test_path

                file_description = f.create.CDCIDescriptor()
                file_description.locator.append(loc)

                file_description['ComponentWidth'].value = 8
                file_description['HorizontalSubsampling'].value = 4
                file_description['ImageAspectRatio'].value = '16/9'
                file_description['StoredWidth'].value = 1920
                file_description['StoredHeight'].value = 1080
                file_description['FrameLayout'].value = 'FullFrame'
                file_description['VideoLineMap'].value = [42, 0]
                file_description['SampleRate'].value = video_rate
                file_description['Length'].value = 10

                file_mob.descriptor = file_description

                clip = tape_mob.create_source_clip(slot_id=1, length=length)
                slot = file_mob.create_picture_slot(video_rate)
                slot.segment.components.append(clip)


                f.content.mobs.append(file_mob)
                mob_count += 1

                # Make the Master MOB
                master_mob = f.create.MasterMob()
                master_mob.name = "Master Mob %i" % i

                master_mob.comments['Test'] = 'Value'
                master_mob.comments.append(f.create.TaggedValue("Test2", 42))

                assert master_mob.comments['Test'] == "Value"
                assert master_mob.comments['Test2'] == 42

                clip = file_mob.create_source_clip(slot_id=1)
                assert clip.length == length
                slot = master_mob.create_picture_slot(video_rate)
                slot.segment.components.append(clip)

                f.content.mobs.append(master_mob)
                mob_count += 1

                # Create a SourceClip
                clip = master_mob.create_source_clip(slot_id=1)
                assert clip.length == length
                sequence.components.append(clip)
                components += 1

                # Create a filler
                comp_fill = f.create.Filler("picture", filler_len)
                sequence.components.append(comp_fill)
                components += 1

        with aaf2.open(result_file, "r")  as f:
            assert len(f.content.mobs) == mob_count
            comp = next(f.content.compositionmobs())
            slot = comp.slot_at(1)
            assert len(slot.segment.components) == components




if __name__ == "__main__":
    unittest.main()
