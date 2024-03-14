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

KEYFRAME_VALUE_MARGIN_OF_ERROR = .1


class TestKeyframeInterpolation(unittest.TestCase):
    def test_normal_bezier(self):
        file = os.path.join(common.test_files_dir(), 'keyframes/normal_bezier.aaf')
        # these values are transcribed by hand from media composer
        expected_result = {
            0: 0.0,
            1: 147.50,
            2: 257.19,
            3: 343.74,
            4: 413.91,
            5: 471.47,
            6: 518.72,
            7: 557.20,
            8: 587.92,
            9: 611.60,
            10: 628.70,
            11: 639.51,
            12: 644.18,
            13: 642.68,
            14: 634.87,
            15: 620.42,
            16: 598.80,
            17: 569.19,
            18: 530.32,
            19: 480.22,
            20: 415.59,
            21: 330.32,
            22: 210.33,
            23: 0.0,
        }
        with aaf2.open(file) as f:
            # Grab the Y position parameter from this AAF
            op_group = next(f.content.compositionmobs()).slots[8].segment.components[1]
            param_y_pos = next(
                param for param in op_group.parameters
                if isinstance(param, aaf2.misc.VaryingValue)
                and param.name == "DVE_POS_Y_U"
            )
            self.compare_interpolated_values(param_y_pos, expected_result)

    def test_handle_past_last_keyframe(self):
        file = os.path.join(common.test_files_dir(), 'keyframes/bezier_handle_past_last_keyframe.aaf')
        # these values are transcribed by hand from media composer
        expected_result = {
            0: 0.0,
            1: 40.2,
            2: 79.92,
            3: 119.09,
            4: 157.63,
            5: 195.45,
            6: 232.43,
            7: 268.39,
            8: 303.14,
            9: 336.38,
            10: 367.72,
            11: 396.57,
            12: 422.01,
            13: 442.48,
            14: 454.99,
            15: 452.45,
            16: 409.92,
            17: 227.30,
            18: 107.82,
            19: 55.0,
            20: 26.25,
            21: 10.24,
            22: 2.3,
            23: 0.0,
        }
        with aaf2.open(file) as f:
            # Grab the Y position parameter from this AAF
            op_group = next(f.content.compositionmobs()).slots[8].segment.components[1]
            param_y_pos = next(
                param for param in op_group.parameters
                if isinstance(param, aaf2.misc.VaryingValue)
                and param.name == "DVE_POS_Y_U"
            )
            self.compare_interpolated_values(param_y_pos, expected_result)

    def compare_interpolated_values(self, parameter, expected_values):
        # Generate the interpolated values
        for frame_num, expected_value in expected_values.items():
            actual_value = parameter.value_at(frame_num)
            difference = abs(actual_value - expected_value)
            assert difference < KEYFRAME_VALUE_MARGIN_OF_ERROR, \
                "Expected value of {:.02f} for frame {} but got {:.02f}. Difference: {:.02f}".format(
                    expected_value, frame_num, actual_value, difference
                )
