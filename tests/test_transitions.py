from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import unittest
import aaf2
from aaf2.auid import AUID
import common

def register_defintiions(f):
    effect_id = AUID("89d9b67e-5584-302d-9abd-8bd330c46841")
    op_def = f.create.OperationDef(effect_id, 'VideoDissolve_2', '')
    f.dictionary.register_def(op_def)

    op_def.media_kind = 'picture'
    op_def['IsTimeWarp'].value = False
    op_def['Bypass'].value = 1
    op_def['NumberInputs'].value = 2
    op_def['OperationCategory'].value = 'OperationCategory_Effect'

    avid_param_byteorder_id = AUID("c0038672-a8cf-11d3-a05b-006094eb75cb")
    byteorder_typedef = f.dictionary.lookup_typedef("aafUInt16")

    avid_effect_id = AUID("93994bd6-a81d-11d3-a05b-006094eb75cb")
    avid_effect_typdef = f.dictionary.lookup_typedef("AvidBagOfBits")

    param_byteorder = f.create.ParameterDef(avid_param_byteorder_id, "AvidParameterByteOrder", "", byteorder_typedef)
    f.dictionary.register_def(param_byteorder)

    param_effect_id = f.create.ParameterDef(avid_effect_id, "AvidEffectID", "", avid_effect_typdef)
    f.dictionary.register_def(param_effect_id)

    op_def.parameters.extend([param_byteorder, param_effect_id])

    # note not part of VideoDissolve_2 op_def but still used...
    opacity_param_id = AUID('8d56813d-847e-11d5-935a-50f857c10000')
    opacity_param_def = f.dictionary.lookup_typedef("Rational")
    opacity_param = f.create.ParameterDef(opacity_param_id, 'AFX_FG_KEY_OPACITY_U', '', opacity_param_def)
    f.dictionary.register_def(opacity_param)

    linear_id = AUID('5b6c85a4-0ede-11d3-80a9-006008143e6f')
    linear = f.create.InterpolationDef(linear_id, 'LinearInterp', '')
    f.dictionary.register_def(linear)

def create_video_clip_import(f):
    frame_rate  = 25
    profile_name = 'dnx_1080p_36_25'
    sample = common.generate_dnxhd(profile_name, "transition.dnxhd", 200)

    tape = None
    master_mob = f.create.MasterMob("MasterMob")
    f.content.mobs.append(master_mob)
    slot = master_mob.import_dnxhd_essence(sample, frame_rate, tape=tape)

    return master_mob.create_source_clip(slot.slot_id, start=50)

def create_video_clip_offline(f):

    master_mob = f.create.MasterMob("MasterMob")
    master_slot = master_mob.create_picture_slot()
    f.content.mobs.append(master_mob)

    source_mob = f.create.SourceMob()
    f.content.mobs.append(source_mob)

    descriptor = f.create.CDCIDescriptor()
    source_mob.descriptor = descriptor

    descriptor['ComponentWidth'].value = 8
    descriptor['HorizontalSubsampling'].value = 2
    descriptor['FrameLayout'].value = "FullFrame"
    descriptor['ImageAspectRatio'].value = "16/9"
    descriptor['StoredWidth'].value = 1920
    descriptor['StoredHeight'].value = 1080
    descriptor['Length'].value = 200

    descriptor['SampleRate'].value = 25
    descriptor['VideoLineMap'].value = [42, 0]
    descriptor['ContainerFormat'].value = f.dictionary.lookup_containerdef("AAF")
    dnxhd_codec_auid = aaf2.auid.AUID("8ef593f6-9521-4344-9ede-b84e8cfdc7da")
    descriptor['CodecDefinition'].value = f.dictionary.lookup_codecdef(dnxhd_codec_auid)

    source_slot = source_mob.create_picture_slot()
    clip = f.create.SourceClip()
    clip.length = 200
    source_slot.segment.components.append(clip)

    clip = source_mob.create_source_clip(slot_id= source_slot.slot_id, start = 0, length = 200)
    master_slot.segment.components.append(clip)

    return master_mob.create_source_clip(master_slot.slot_id, start=50)

def create_video_transition(f):
    video_dissolve_def = f.dictionary.lookup_operationdef('VideoDissolve_2')

    length = 20
    cut_point = 10

    transition = f.create.Transition()
    transition.length = length
    transition['CutPoint'].value = cut_point

    op_group = f.create.OperationGroup(video_dissolve_def)
    op_group.media_kind = 'picture'
    transition['OperationGroup'].value = op_group

    # now setup the dissovle curve
    opacity_u = f.create.VaryingValue()
    opacity_u.parameterdef = f.dictionary.lookup_parameterdef("AFX_FG_KEY_OPACITY_U")
    opacity_u['Interpolation'].value = f.dictionary.lookup_interperlationdef("LinearInterp")

    a = f.create.ControlPoint()
    # setting edit hint makes some avid warnings go away
    a['EditHint'].value = "Proportional"
    a.value = 0.0
    a.time =  0.0

    b = f.create.ControlPoint()
    b['EditHint'].value = "Proportional"
    b.value =  100.0
    b.time  =  1.0

    opacity_u['PointList'].extend([a, b])

    # not sure what the AUID is suppose to represent
    opacity_u['VVal_Extrapolation'].value = AUID('0e24dd54-66cd-4f1a-b0a0-670ac3a7a0b3')
    opacity_u['VVal_FieldCount'].value = 1
    op_group.parameters.append(opacity_u)

    op_group.length = length
    # transition.dump()
    return transition

class TestTransitions(unittest.TestCase):

    def test_video_transition(self):
        result_file = common.get_test_file('create_transition.aaf')

        with aaf2.open(result_file, 'w') as f:
            register_defintiions(f)

            comp = f.create.CompositionMob("Transition Timeline")
            comp.usage = 'Usage_TopLevel'

            f.content.mobs.append(comp)

            slot = comp.create_picture_slot()
            seq = f.create.Sequence()
            slot.segment = seq

            filler = f.create.Filler()
            filler.length= 50
            seq.components.append(filler)

            transition = create_video_transition(f)
            seq.components.append(transition)

            clip = create_video_clip_import(f)
            clip.length = 50
            seq.components.append(clip)

            transition = create_video_transition(f)
            seq.components.append(transition)

            clip = create_video_clip_offline(f)
            clip.length = 50
            seq.components.append(clip)

            transition = create_video_transition(f)
            seq.components.append(transition)

            filler = f.create.Filler()
            filler.length= 50
            seq.components.append(filler)


        with aaf2.open(result_file, 'r') as f:
            comp = next(f.content.toplevel())

            slot = comp.slots[0]
            transitions = []
            for item in slot.segment.components:
                if isinstance(item, aaf2.components.Transition):
                    transitions.append(item)

            assert len(transitions) == 3
            for t in transitions:
                op_group = t['OperationGroup'].value
                opacity_u = None
                for p in op_group.parameters:
                    if p.name == 'AFX_FG_KEY_OPACITY_U':
                        opacity_u = p
                        break
                for point in opacity_u['PointList'].value:
                    assert isinstance(point['Value'].value, aaf2.rational.AAFRational)


if __name__ == "__main__":
    unittest.main()
