from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import aaf2

import unittest

import common
import datetime

class ComponentAAFTests(unittest.TestCase):


    def test_marker(self):
        result_file = common.get_test_file('descriptive_marker.aaf')
        described_slots = set([1,2,3,4])

        with aaf2.open(result_file, 'w') as f:
            ems = f.create.EventMobSlot()
            ems['EditRate'].value = '25'
            ems['SlotID'].value = 1000
            # doesn't work in avid unless you specify
            # the same PhysicalTrackNumber as the target TimelineMobSlot.
            ems['PhysicalTrackNumber'].value = 1

            sequence = f.create.Sequence("DescriptiveMetadata")
            marker = f.create.DescriptiveMarker()
            marker['DescribedSlots'].value = described_slots
            marker['Position'].value = 100
            marker['Comment'].value = "This is a comment"
            marker['CommentMarkerUser'].value = "username"

            sequence.components.append(marker)
            ems.segment = sequence

            mob = f.create.CompositionMob()
            mob.name = "marker_sequence"
            p_slot = mob.create_picture_slot()
            filler  = f.create.Filler()
            filler.media_kind = "picture"
            filler.length = 500
            p_slot.segment.components.append(filler)
            p_slot['PhysicalTrackNumber'].value = 1

            mob.slots.append(ems)
            f.content.mobs.append(mob)

        with aaf2.open(result_file, 'r') as f:

            mob = next(f.content.mobs.values())
            slot = mob.slots.value[1]
            marker = slot.segment.components.value[0]

            assert marker['DescribedSlots'].value == described_slots
            assert marker['Position'].value == 100




if __name__ == "__main__":
    unittest.main()
