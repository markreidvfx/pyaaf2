from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import aaf2
import os
import io
import time
import common
import unittest

DIFSECT    = 0xFFFFFFFC
FATSECT    = 0xFFFFFFFD
ENDOFCHAIN = 0xFFFFFFFE
FREESECT   = 0xFFFFFFFF

RANGELOCKSECT = (0x7FFFFF00 // 4096) - 1
class ImportTests(unittest.TestCase):
    def test_range_lock(self):

        frame_rate = '23.97'
        size = (960, 540)
        profile_name = 'dnxhr_lb'
        frames = 1600
        overwrite = True
        sample = common.generate_dnxhd(profile_name, "%s-import.dnxhd" % profile_name,
               frames=frames, size=size, frame_rate=frame_rate, overwrite=overwrite)

        test_file = common.get_test_file("test-rangelock.aaf")
        with aaf2.open(test_file, 'wb+') as f:
            pass
        mobids = []
        s =time.time()

        # generate a aaf file thats larger then 2gb
        with aaf2.open(test_file, 'rb+') as f:
            for v in range(30):
                start = time.time()
                mob = f.create.MasterMob("item-%d" % v)
                f.content.mobs.append(mob)
                mob.import_dnxhd_essence(sample, frame_rate)

                # print(v, time.time() - start)

        print('%d secs' % (time.time() - s))
        with aaf2.open(test_file, 'r') as f:
            # print(RANGELOCKSECT)
            # print(len(f.cfb.fat))
            # print(f.cfb.fat[RANGELOCKSECT])
            assert f.cfb.fat[RANGELOCKSECT] == ENDOFCHAIN

            # for m in f.content.essencedata:
            #     print(m)
            # for m in mobids:
            #     print(f.content.essencedata.get(m))


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
