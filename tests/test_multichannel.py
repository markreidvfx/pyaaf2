from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import math
import struct
import unittest
import aaf2
from aaf2 import components
from aaf2.auid import AUID
import common

# Audio Channel Combiner OperationDef AUID (from Pro Tools AAF exports)
CHANNEL_COMBINER_AUID = '6b46dd7a-132d-4856-ab21-8b751d8462ec'

# ParameterDef AUIDs (same as those registered in test_transitions.py)
PARAM_BYTE_ORDER_AUID = 'c0038672-a8cf-11d3-a05b-006094eb75cb'
PARAM_EFFECT_ID_AUID = '93994bd6-a81d-11d3-a05b-006094eb75cb'

# AvidEffectID payload: null-terminated ASCII string as byte list
EFFECT_ID_BYTES = list(b'EFF2_AUDIO_CHANNEL_COMBINER\x00')

# AvidParameterByteOrder: 0x4949 = little-endian
BYTE_ORDER_VALUE = 18761

# _TRACK_FORMAT tagged value constants
TRACK_FORMAT_STEREO = 2
TRACK_FORMAT_51 = 3
TRACK_FORMAT_71 = 4

# Channel layouts matching Pro Tools export conventions
CHANNEL_LAYOUTS = {
    'stereo': (['L', 'R'], TRACK_FORMAT_STEREO),
    '5.1':    (['L', 'C', 'R', 'Ls', 'Rs', 'LFE'], TRACK_FORMAT_51),
    '7.1':    (['L', 'C', 'R', 'Lss', 'Rss', 'Lsr', 'Rsr', 'LFE'], TRACK_FORMAT_71),
}


def generate_mono_pcm(num_samples, sample_rate=48000, freq=440):
    """Generate mono 16-bit PCM sine tone as raw bytes. No ffmpeg needed."""
    samples = bytearray()
    max_val = 2**15 - 1
    for i in range(num_samples):
        t = i / sample_rate
        val = int(0.5 * max_val * math.sin(2 * math.pi * freq * t))
        samples.extend(struct.pack('<h', val))
    return bytes(samples)


def register_channel_combiner(f):
    """Register Audio Channel Combiner OperationDef and its ParameterDefs."""

    pd_byte_order = f.create.ParameterDef(
        PARAM_BYTE_ORDER_AUID, 'AvidParameterByteOrder', '', 'aafInt16')
    f.dictionary.register_def(pd_byte_order)

    pd_effect_id = f.create.ParameterDef(
        PARAM_EFFECT_ID_AUID, 'AvidEffectID', '', 'AvidBagOfBits')
    f.dictionary.register_def(pd_effect_id)

    op_def = f.create.OperationDef(
        CHANNEL_COMBINER_AUID, 'Audio Channel Combiner', '')
    op_def.media_kind = 'sound'
    op_def['IsTimeWarp'].value = False
    op_def['Bypass'].value = 0
    op_def['NumberInputs'].value = 1  # matches Pro Tools exports
    op_def['OperationCategory'].value = 'OperationCategory_Effect'
    op_def.parameters.extend([pd_byte_order, pd_effect_id])
    f.dictionary.register_def(op_def)

    return op_def, pd_byte_order, pd_effect_id


def create_mono_essence_chain(f, clip_name, channel_suffix, edit_rate,
                               pcm_bytes, sample_rate, sample_width, num_frames):
    """
    Create a complete per-channel mob chain:
      TapeDescriptor SourceMob -> PCMDescriptor SourceMob (embedded) -> MasterMob

    Returns (master_mob, master_slot).
    """

    total_eu = int(num_frames * 30000 / (sample_rate * 1001))

    # TapeDescriptor SourceMob (end of chain)
    tape_mob = f.create.SourceMob()
    tape_mob.name = "Pro Tools:MultichannelTest.ptx"
    tape_mob.descriptor = f.create.TapeDescriptor()
    tape_sound_slot = tape_mob.create_timeline_slot(edit_rate=edit_rate)
    tape_clip = f.create.SourceClip(media_kind='sound')
    tape_clip.length = total_eu
    tape_sound_slot.segment = tape_clip
    f.content.mobs.append(tape_mob)

    # PCMDescriptor SourceMob (embedded audio)
    source_mob = f.create.SourceMob()
    source_mob.name = clip_name
    desc = f.create.PCMDescriptor()
    desc['Channels'].value = 1
    desc['BlockAlign'].value = sample_width
    desc['SampleRate'].value = sample_rate
    desc['AverageBPS'].value = sample_rate * sample_width
    desc['QuantizationBits'].value = sample_width * 8
    desc['AudioSamplingRate'].value = sample_rate
    desc.length = num_frames
    source_mob.descriptor = desc
    f.content.mobs.append(source_mob)

    essencedata = f.create.EssenceData()
    essencedata.mob_id = source_mob.mob_id
    f.content.essencedata.append(essencedata)
    stream = essencedata.open('w')
    stream.write(pcm_bytes)

    source_slot = source_mob.create_timeline_slot(edit_rate=edit_rate)
    tape_ref = tape_mob.create_source_clip(
        slot_id=tape_sound_slot.slot_id, length=total_eu)
    source_slot.segment = tape_ref

    # MasterMob
    master_mob = f.create.MasterMob()
    master_mob.name = "%s.%s" % (clip_name, channel_suffix)
    f.content.mobs.append(master_mob)

    master_slot = master_mob.create_timeline_slot(edit_rate=edit_rate)
    master_clip = source_mob.create_source_clip(
        slot_id=source_slot.slot_id, media_kind='sound')
    master_slot.segment = master_clip

    return master_mob, master_slot


def create_multichannel_aaf(f, layout_name, clip_name='TestTone'):
    """
    Create a complete multichannel AAF with one track and one clip.

    Returns the path written by the caller, for read-back verification.
    """

    channel_suffixes, track_format = CHANNEL_LAYOUTS[layout_name]
    num_channels = len(channel_suffixes)
    edit_rate = '30000/1001'
    sample_rate = 48000
    sample_width = 2  # 16-bit
    num_frames = 96000  # 2 seconds at 48kHz
    clip_length = 30    # edit units (video frames)
    clip_offset = 50    # filler before clip
    tc_start = 107892   # 01:00:00;00 DF

    total_eu = int(num_frames * 30000 / (sample_rate * 1001))
    clip_start_in_media = (total_eu - clip_length) // 2

    op_def, pd_byte_order, pd_effect_id = register_channel_combiner(f)

    # Build per-channel mob chains
    master_mobs = []
    master_slots = []
    for i, suffix in enumerate(channel_suffixes):
        freq = 440 + i * 100
        pcm = generate_mono_pcm(num_frames, sample_rate, freq)
        mm, ms = create_mono_essence_chain(
            f, clip_name, suffix, edit_rate,
            pcm, sample_rate, sample_width, num_frames)
        master_mobs.append(mm)
        master_slots.append(ms)

    # CompositionMob
    comp = f.create.CompositionMob()
    comp.name = "MultichannelTest_%s" % layout_name.replace('.', '_')
    comp['UsageCode'].value = 'Usage_TopLevel'
    f.content.mobs.append(comp)

    # Audio slot
    audio_slot = comp.create_timeline_slot(edit_rate=edit_rate)
    audio_slot['SlotName'].value = '%s Track' % layout_name

    tv = f.create.TaggedValue("_TRACK_FORMAT", track_format, 'aafInt32')
    audio_slot['TimelineMobAttributeList'].value = [tv]

    seq = f.create.Sequence(media_kind='sound')
    audio_slot.segment = seq

    filler = f.create.Filler(media_kind='sound', length=clip_offset)
    seq.components.append(filler)

    # OperationGroup (Audio Channel Combiner)
    op_group = f.create.OperationGroup(op_def, length=clip_length, media_kind='sound')

    tv2 = f.create.TaggedValue("_IGNORE_TRACKING", 0, 'aafInt32')
    op_group['ComponentAttributeList'].value = [tv2]

    cv_byte_order = f.create.ConstantValue(pd_byte_order, BYTE_ORDER_VALUE)
    cv_effect_id = f.create.ConstantValue(pd_effect_id, EFFECT_ID_BYTES)
    op_group.parameters.append(cv_byte_order)
    op_group.parameters.append(cv_effect_id)

    for mm, ms in zip(master_mobs, master_slots):
        clip = mm.create_source_clip(
            slot_id=ms.slot_id,
            start=clip_start_in_media,
            length=clip_length,
            media_kind='sound')
        op_group.segments.append(clip)

    seq.components.append(op_group)
    seq.length = clip_offset + clip_length

    # Timecode slot
    tc_slot = comp.create_timeline_slot(edit_rate=edit_rate)
    tc = f.create.Timecode(fps=30, drop=True)
    tc.start = tc_start
    tc.length = clip_offset + clip_length
    tc_slot.segment = tc

    return {
        'num_channels': num_channels,
        'track_format': track_format,
        'clip_length': clip_length,
        'clip_offset': clip_offset,
        'sample_rate': sample_rate,
        'sample_width': sample_width,
        'num_frames': num_frames,
        'channel_suffixes': channel_suffixes,
    }


def verify_multichannel_aaf(test_case, f, expected):
    """Read back and verify a multichannel AAF."""

    comp = next(f.content.toplevel())
    assert isinstance(comp, aaf2.mobs.CompositionMob)

    slots = list(comp.slots)
    test_case.assertEqual(len(slots), 2)  # audio + timecode

    audio_slot = slots[0]
    tc_slot = slots[1]

    # Verify _TRACK_FORMAT tagged value
    attr_list = audio_slot['TimelineMobAttributeList'].value
    track_format_tag = None
    for tv in attr_list:
        if tv.name == '_TRACK_FORMAT':
            track_format_tag = tv
    test_case.assertIsNotNone(track_format_tag)
    test_case.assertEqual(track_format_tag.value, expected['track_format'])

    # Verify Sequence structure
    seq = audio_slot.segment
    test_case.assertIsInstance(seq, components.Sequence)
    comps = list(seq.components)
    test_case.assertEqual(len(comps), 2)  # Filler + OperationGroup
    test_case.assertIsInstance(comps[0], components.Filler)
    test_case.assertEqual(comps[0].length, expected['clip_offset'])

    # Verify OperationGroup
    op_group = comps[1]
    test_case.assertIsInstance(op_group, components.OperationGroup)
    test_case.assertEqual(op_group.length, expected['clip_length'])
    test_case.assertEqual(op_group.operation.name, 'Audio Channel Combiner')
    test_case.assertEqual(str(op_group.operation.auid), CHANNEL_COMBINER_AUID)

    # Verify parameters
    params = list(op_group.parameters)
    test_case.assertEqual(len(params), 2)

    byte_order_param = None
    effect_id_param = None
    for p in params:
        pd = p.parameterdef
        if pd.name == 'AvidParameterByteOrder':
            byte_order_param = p
        elif pd.name == 'AvidEffectID':
            effect_id_param = p

    test_case.assertIsNotNone(byte_order_param)
    test_case.assertEqual(byte_order_param.value, BYTE_ORDER_VALUE)

    test_case.assertIsNotNone(effect_id_param)
    decoded = bytes(effect_id_param.value).rstrip(b'\x00').decode('utf-8')
    test_case.assertEqual(decoded, 'EFF2_AUDIO_CHANNEL_COMBINER')

    # Verify InputSegments
    inputs = list(op_group.segments)
    test_case.assertEqual(len(inputs), expected['num_channels'])

    # Verify each input resolves through the full mob chain
    all_mobs = list(f.content.mobs)
    mob_lookup = {}
    for m in all_mobs:
        try:
            mob_lookup[m.mob_id] = m
        except Exception:
            pass

    essence_byte_count = expected['num_frames'] * expected['sample_width']

    for i, inp in enumerate(inputs):
        test_case.assertIsInstance(inp, components.SourceClip)
        test_case.assertEqual(inp.length, expected['clip_length'])

        # Resolve to MasterMob
        mm = mob_lookup.get(inp.mob_id)
        test_case.assertIsNotNone(mm, "InputSegment[%d] MasterMob not found" % i)
        test_case.assertIsInstance(mm, aaf2.mobs.MasterMob)
        test_case.assertTrue(
            mm.name.endswith('.%s' % expected['channel_suffixes'][i]),
            "Expected suffix .%s, got name %r" % (expected['channel_suffixes'][i], mm.name))

        # Resolve MasterMob -> SourceMob
        mm_slot = list(mm.slots)[0]
        sc = mm_slot.segment
        test_case.assertIsInstance(sc, components.SourceClip)
        sm = mob_lookup.get(sc.mob_id)
        test_case.assertIsNotNone(sm, "SourceMob for channel %d not found" % i)
        test_case.assertIsInstance(sm, aaf2.mobs.SourceMob)

        # Verify PCMDescriptor
        desc = sm.descriptor
        test_case.assertIsInstance(desc, aaf2.essence.PCMDescriptor)
        test_case.assertEqual(desc['Channels'].value, 1)

        # Verify EssenceData exists and has correct size
        found_essence = False
        for ed in f.content.essencedata:
            if ed.mob_id == sm.mob_id:
                stream = ed.open('r')
                total = stream.seek(0, 2)
                stream.close()
                test_case.assertEqual(total, essence_byte_count,
                    "Channel %d essence: expected %d bytes, got %d" % (
                        i, essence_byte_count, total))
                found_essence = True
                break
        test_case.assertTrue(found_essence,
            "No EssenceData found for channel %d" % i)

    # Verify timecode slot
    test_case.assertIsInstance(tc_slot.segment, aaf2.components.Timecode)


class TestMultichannelAudio(unittest.TestCase):

    def test_stereo(self):
        result_file = common.get_test_file('multichannel_stereo.aaf')

        with aaf2.open(result_file, 'w') as f:
            expected = create_multichannel_aaf(f, 'stereo')

        with aaf2.open(result_file, 'r') as f:
            verify_multichannel_aaf(self, f, expected)

    def test_surround_51(self):
        result_file = common.get_test_file('multichannel_51.aaf')

        with aaf2.open(result_file, 'w') as f:
            expected = create_multichannel_aaf(f, '5.1')

        with aaf2.open(result_file, 'r') as f:
            verify_multichannel_aaf(self, f, expected)

    def test_surround_71(self):
        result_file = common.get_test_file('multichannel_71.aaf')

        with aaf2.open(result_file, 'w') as f:
            expected = create_multichannel_aaf(f, '7.1')

        with aaf2.open(result_file, 'r') as f:
            verify_multichannel_aaf(self, f, expected)

    def test_empty_multichannel_slot(self):
        """An empty multichannel track has _TRACK_FORMAT but no OperationGroup."""
        result_file = common.get_test_file('multichannel_empty.aaf')

        with aaf2.open(result_file, 'w') as f:
            comp = f.create.CompositionMob()
            comp.name = "EmptyMultichannelTest"
            comp['UsageCode'].value = 'Usage_TopLevel'
            f.content.mobs.append(comp)

            for layout_name, (suffixes, track_format) in CHANNEL_LAYOUTS.items():
                slot = comp.create_timeline_slot(edit_rate='30000/1001')
                slot['SlotName'].value = '%s Track' % layout_name

                tv = f.create.TaggedValue("_TRACK_FORMAT", track_format, 'aafInt32')
                slot['TimelineMobAttributeList'].value = [tv]

                seq = f.create.Sequence(media_kind='sound')
                filler = f.create.Filler(media_kind='sound', length=1000)
                seq.components.append(filler)
                seq.length = 1000
                slot.segment = seq

        with aaf2.open(result_file, 'r') as f:
            comp = next(f.content.toplevel())
            slots = list(comp.slots)
            self.assertEqual(len(slots), 3)

            expected_formats = [TRACK_FORMAT_STEREO, TRACK_FORMAT_51, TRACK_FORMAT_71]
            for slot, expected_tf in zip(slots, expected_formats):
                attr_list = slot['TimelineMobAttributeList'].value
                found = False
                for tv in attr_list:
                    if tv.name == '_TRACK_FORMAT':
                        self.assertEqual(tv.value, expected_tf)
                        found = True
                self.assertTrue(found, "_TRACK_FORMAT not found on slot")

                seq = slot.segment
                self.assertIsInstance(seq, components.Sequence)
                comps = list(seq.components)
                self.assertEqual(len(comps), 1)
                self.assertIsInstance(comps[0], components.Filler)


if __name__ == "__main__":
    unittest.main()
