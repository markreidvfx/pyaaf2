from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import unittest
import aaf2
from aaf2.auid import AUID
from aaf2 import audio
import common

def register_definitions(f):
    op_def = f.create.OperationDef('89d9b67e-5584-302d-9abd-8bd330c46841', 'VideoDissolve_2', '')
    f.dictionary.register_def(op_def)

    op_def.media_kind = 'picture'
    op_def['IsTimeWarp'].value = False
    op_def['Bypass'].value = 1
    op_def['NumberInputs'].value = 2
    op_def['OperationCategory'].value = 'OperationCategory_Effect'

    param_byteorder = f.create.ParameterDef("c0038672-a8cf-11d3-a05b-006094eb75cb", "AvidParameterByteOrder", "", 'aafUInt16')
    f.dictionary.register_def(param_byteorder)

    param_effect_id = f.create.ParameterDef("93994bd6-a81d-11d3-a05b-006094eb75cb", "AvidEffectID", "", 'AvidBagOfBits')
    f.dictionary.register_def(param_effect_id)

    op_def.parameters.extend([param_byteorder, param_effect_id])

    # note not part of VideoDissolve_2 op_def but still used...
    opacity_param = f.create.ParameterDef('8d56813d-847e-11d5-935a-50f857c10000', 'AFX_FG_KEY_OPACITY_U', '', 'Rational')
    f.dictionary.register_def(opacity_param)

    linear = f.create.InterpolationDef('5b6c85a4-0ede-11d3-80a9-006008143e6f', 'LinearInterp', '')
    f.dictionary.register_def(linear)

    op_def = f.create.OperationDef('0c3bea41-fc05-11d2-8a29-0050040ef7d2', 'Audio Dissolve', '')
    f.dictionary.register_def(op_def)

    op_def.media_kind = 'sound'
    op_def['IsTimeWarp'].value = False
    op_def['Bypass'].value = 1
    op_def['NumberInputs'].value = 2
    op_def['OperationCategory'].value = 'OperationCategory_Effect'
    op_def.parameters.extend([param_byteorder, param_effect_id])

def create_video_clip_import(f):
    frame_rate  = 25
    profile_name = 'dnx_1080p_36_25'
    sample = common.generate_dnxhd(profile_name, "transition.dnxhd", 200)

    tape = None
    master_mob = f.create.MasterMob("MasterMob")
    f.content.mobs.append(master_mob)
    slot = master_mob.import_dnxhd_essence(sample, frame_rate, tape=tape)

    return master_mob.create_source_clip(slot.slot_id, start=50)

def create_audio_clip_import(f):
    audio_profile_name = 'pcm_48000_s24le'
    frame_rate = 25
    frames = 200
    audio_duration = frames/frame_rate

    sample_format = audio.pcm_profiles[audio_profile_name]['sample_format']
    sample_rate = audio.pcm_profiles[audio_profile_name]['sample_rate']
    audio_sample = common.generate_pcm_audio_mono(audio_profile_name, sample_format=sample_format, sample_rate=sample_rate, duration=audio_duration)

    master_mob = f.create.MasterMob("MasterMob")
    f.content.mobs.append(master_mob)
    slot = master_mob.import_audio_essence(audio_sample, frame_rate)
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

    length = 20
    cut_point = 10

    transition = f.create.Transition()
    transition.length = length
    transition['CutPoint'].value = cut_point

    op_group = f.create.OperationGroup('VideoDissolve_2')
    op_group.media_kind = 'picture'
    transition['OperationGroup'].value = op_group

    # now setup the dissovle curve
    opacity_u = f.create.VaryingValue("AFX_FG_KEY_OPACITY_U", "LinearInterp")

    # setting edit hint Proportional makes some avid warnings go away
    opacity_u.add_keyframe(0.0,   0.0, 'Proportional')
    opacity_u.add_keyframe(1.0, 100.0, 'Proportional')

    # not sure what the AUID is suppose to represent
    opacity_u['VVal_Extrapolation'].value = AUID('0e24dd54-66cd-4f1a-b0a0-670ac3a7a0b3')
    opacity_u['VVal_FieldCount'].value = 1
    op_group.parameters.append(opacity_u)

    op_group.length = length
    # transition.dump()
    return transition

def create_audio_transition(f):

    length = 40
    cut_point = 20

    transition = f.create.Transition('sound')
    transition.length = length
    transition['CutPoint'].value = cut_point

    op_group = f.create.OperationGroup('Audio Dissolve')
    op_group.media_kind = 'sound'
    transition['OperationGroup'].value = op_group

    return transition

class TestTransitions(unittest.TestCase):

    def test_video_transition(self):
        result_file = common.get_test_file('video_transition.aaf')

        with aaf2.open(result_file, 'w') as f:
            register_definitions(f)

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
            clip.mob.name = "clip1"
            clip.length = 50
            seq.components.append(clip)

            transition = create_video_transition(f)
            seq.components.append(transition)

            clip = create_video_clip_offline(f)
            clip.length = 50
            clip.mob.name = "clip2"
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
            seq = slot.segment
            clip = seq.component_at_time(0)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(29)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(30)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(39)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(40)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(49)
            assert isinstance(clip, aaf2.components.Transition)

            clip = seq.component_at_time(50)
            assert isinstance(clip, aaf2.components.SourceClip)
            assert clip.mob.name == 'clip1'

            clip = seq.component_at_time(59)
            assert isinstance(clip, aaf2.components.SourceClip)
            assert clip.mob.name == 'clip1'

            clip = seq.component_at_time(60)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(69)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(70)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(79)
            assert isinstance(clip, aaf2.components.Transition)

            clip = seq.component_at_time(80)
            assert isinstance(clip, aaf2.components.SourceClip)
            assert clip.mob.name == 'clip2'

            clip = seq.component_at_time(89)
            assert isinstance(clip, aaf2.components.SourceClip)
            assert clip.mob.name == 'clip2'

            clip = seq.component_at_time(90)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(99)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(109)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(110)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(139)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(150)
            assert isinstance(clip, aaf2.components.Filler)

    def test_audio_transition(self):
        result_file = common.get_test_file('audio_transition.aaf')

        with aaf2.open(result_file, 'w') as f:
            register_definitions(f)

            comp = f.create.CompositionMob("Transition Timeline")
            comp.usage = 'Usage_TopLevel'

            f.content.mobs.append(comp)

            slot = comp.create_sound_slot()
            seq = f.create.Sequence('sound')
            slot.segment = seq

            filler = f.create.Filler('sound')
            filler.length = 50
            seq.components.append(filler)

            t = create_audio_transition(f)
            seq.components.append(t)

            clip = create_audio_clip_import(f)
            clip.mob.name = "clip1"
            clip.length = 100
            seq.components.append(clip)

            t = create_audio_transition(f)
            seq.components.append(t)

            filler = f.create.Filler('sound')
            filler.length = 50
            seq.components.append(filler)

        with aaf2.open(result_file, 'r') as f:
            comp = next(f.content.toplevel())

            slot = comp.slots[0]
            seq = slot.segment
            clip = seq.component_at_time(0)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(9)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(10)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(29)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(30)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(49)
            assert isinstance(clip, aaf2.components.Transition)

            clip = seq.component_at_time(50)
            assert isinstance(clip, aaf2.components.SourceClip)
            assert clip.mob.name == 'clip1'

            clip = seq.component_at_time(69)
            assert isinstance(clip, aaf2.components.SourceClip)
            assert clip.mob.name == 'clip1'

            clip = seq.component_at_time(70)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(89)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(90)
            assert isinstance(clip, aaf2.components.Transition)
            clip = seq.component_at_time(109)
            assert isinstance(clip, aaf2.components.Transition)

            clip = seq.component_at_time(110)
            assert isinstance(clip, aaf2.components.Filler)
            clip = seq.component_at_time(300)
            assert isinstance(clip, aaf2.components.Filler)





if __name__ == "__main__":
    unittest.main()
