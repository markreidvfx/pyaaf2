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

class CreatAAFTests(unittest.TestCase):


    def test_marker(self):
        result_file = common.get_test_file('descriptive_marker.aaf')
        described_slots = set([1,2,3,4])

        with aaf2.open(result_file, 'w') as f:
            ems = f.create.EventMobSlot()
            ems['EditRate'].value = '25'
            ems['SlotID'].value = 1000

            sequence = f.create.Sequence("DescriptiveMetadata")
            marker = f.create.DescriptiveMarker()
            marker['DescribedSlots'].value = described_slots
            marker['Position'].value = 100
            marker['DataDefinition'].value = f.dictionary.lookup_datadef("DescriptiveMetadata")

            sequence.components.append(marker)
            ems.segment = sequence

            mob = f.create.MasterMob()
            mob.slots.append(ems)
            f.content.mobs.append(mob)

        with aaf2.open(result_file, 'r') as f:

            mob = next(f.content.mobs.values())
            slot = mob.slots.value[0]
            marker = slot.segment.components.value[0]

            assert marker['DescribedSlots'].value == described_slots
            assert marker['Position'].value == 100




if __name__ == "__main__":
    unittest.main()
