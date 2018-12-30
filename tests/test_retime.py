from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import os
import aaf2
import common
import unittest

from aaf2.misc import generate_offset_map

def find_retime(f):
    comp = next(f.content.toplevel())
    # comp.dump()
    video_tracks = []
    for component in [item.segment for item in comp.slots]:
        # print(component.media_kind)
        if component.media_kind == 'Picture':
            video_tracks.append(component)

    seq = video_tracks[0]

    spatial_adapter = list(seq.components)[0]
    op_group = list(list(spatial_adapter.segments)[0].components)[0]
    speed_map = None
    offset_map = None

    for param in op_group.parameters:

        if param.name == "PARAM_SPEED_MAP_U":
            speed_map = param
        if param.name == 'PARAM_SPEED_OFFSET_MAP_U':
            offset_map = param

    return (op_group, spatial_adapter), speed_map, offset_map


def compare_speedmap_to_offset_map(path):

    with aaf2.open(path) as f:
        op_group, speed_map, offset_map = find_retime(f)
        start = int(offset_map['PointList'].value[0].time)

        length = op_group[0].length

        error_list = []

        for t, v in generate_offset_map(speed_map, start, length):
            target_value = offset_map.value_at(t)
            error_list.append(abs(target_value - v))

        # print("average error:", sum(error_list) / len(error_list))

        return sum(error_list) / len(error_list)

def error_ok(value, path):
    # print(os.path.basename(path), 'error =', value)
    if value > 1.0e-07:
        return False
    return True

class TestRetime(unittest.TestCase):

    def test_speedmap_step(self):
        test_file = os.path.join(common.test_files_dir(), 'retimes/step01.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/step02.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/step03.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))

    def test_speedmap_linear(self):
        test_file = os.path.join(common.test_files_dir(), 'retimes/linear01.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/linear02.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/linear03.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))

    def test_speedmap_spline(self):
        test_file = os.path.join(common.test_files_dir(), 'retimes/spline01.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/spline02.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/spline03.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))

    def test_speedmap_bezier(self):
        test_file = os.path.join(common.test_files_dir(), 'retimes/bezier01.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/bezier02.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))
        test_file = os.path.join(common.test_files_dir(), 'retimes/bezier03.aaf')
        error = compare_speedmap_to_offset_map(test_file)
        self.assertTrue(error_ok(error, test_file))

    def skip_test_retime_manually(self):

        test_file = os.path.join(common.test_files_dir(), 'retimes/spline02.aaf')
        test_file = os.path.join(common.test_files_dir(), 'retimes/spline04.aaf')
        # compare_speedmap_to_offset_map(test_file)


        # manual testing here

        import matplotlib.pyplot as plt
        import numpy as np

        with aaf2.open(test_file) as f:
            op_group, speed_map, offset_map = find_retime(f)

            target =[[], []]

            p0 = offset_map['PointList'].value[0]
            # p0.dump()
            sp0 = speed_map['PointList'].value[0]
            sp0.dump()

            # p0 = speed_map['PointList'].value[0]

            # for i in range(0, 200):
            #     target[0].append(i)
            #     target[1].append(offset_map.value_at(i))

            for item in offset_map['PointList'].value:
                target[0].append(item.time)
                target[1].append(item.value)

            start = int(p0.time)
            print(p0.time)
            # op_group[1].dump()

            # print(end, p_last.time)
            pos = 0
            error_list = []

            offset_map_gen = generate_offset_map(speed_map, start, op_group[0].length)
            calcuated = [[], []]
            for t,v in offset_map_gen:
                calcuated[0].append(t)
                calcuated[1].append(v)
                tar = offset_map.value_at(t)
                error = abs(tar - v)
                print(t, error, tar, pos)
                error_list.append(error)

            print("average error:", sum(error_list) / len(error_list))


            plt.plot(target[0], target[1])
            plt.plot(calcuated[0], calcuated[1])

            plt.show()


if __name__ == "__main__":
    import logging
    # logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    # test_spline2d()
