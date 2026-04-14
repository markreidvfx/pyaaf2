#!/usr/bin/env python3
"""
Create AAF files with multichannel audio tracks (stereo, 5.1, 7.1) that
Pro Tools imports as native multichannel tracks.

Background
----------
Pro Tools represents multichannel audio clips using an "Audio Channel Combiner"
OperationGroup. Each multichannel track has ONE composition slot containing a
Sequence of OperationGroups (one per clip). Each OperationGroup wraps N mono
SourceClips (one per channel), and each channel has its own independent mob
chain: MasterMob -> SourceMob (PCMDescriptor, mono) -> SourceMob (Tape).

The _TRACK_FORMAT tagged value on the TimelineMobSlot tells Pro Tools the
channel layout:
    2 = stereo
    3 = 5.1 surround
    4 = 7.1 surround

Channel order (InputSegment index -> channel):
    Stereo: L, R
    5.1:    L, C, R, Ls, Rs, LFE
    7.1:    L, C, R, Lss, Rss, Lsr, Rsr, LFE

This pattern was discovered by analyzing Pro Tools AAF exports created with
"Enforce Media Composer Compatibility" and "Export stereo, 5.1 and 7.1 tracks
as multi-channel" enabled. It has been verified to round-trip through both
pyaaf2 and Pro Tools.

See also: https://github.com/markreidvfx/pyaaf2/issues/145
          https://github.com/markreidvfx/pyaaf2/issues/102
          https://github.com/markreidvfx/pyaaf2/issues/93

Usage
-----
    python multichannel_audio.py [output_directory]

Produces two files in the output directory (default: current directory):
    stereo_example.aaf   - stereo track with one clip
    surround_51_example.aaf - 5.1 track with one clip
"""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import math
import os
import struct
import sys

import aaf2
import aaf2.auid

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Audio Channel Combiner OperationDef (from Pro Tools AAF exports)
CHANNEL_COMBINER_AUID = '6b46dd7a-132d-4856-ab21-8b751d8462ec'

# ParameterDef AUIDs
PARAM_BYTE_ORDER_AUID = 'c0038672-a8cf-11d3-a05b-006094eb75cb'
PARAM_EFFECT_ID_AUID  = '93994bd6-a81d-11d3-a05b-006094eb75cb'

# Parameter values (constant across all multichannel formats)
BYTE_ORDER_VALUE = 18761  # 0x4949 = little-endian
EFFECT_ID_BYTES = list(b'EFF2_AUDIO_CHANNEL_COMBINER\x00')

# _TRACK_FORMAT values
TRACK_FORMAT = {
    'stereo': 2,
    '5.1': 3,
    '7.1': 4,
}

# Channel suffixes (order matches Pro Tools InputSegment convention)
CHANNELS = {
    'stereo': ['L', 'R'],
    '5.1': ['L', 'C', 'R', 'Ls', 'Rs', 'LFE'],
    '7.1': ['L', 'C', 'R', 'Lss', 'Rss', 'Lsr', 'Rsr', 'LFE'],
}

# ---------------------------------------------------------------------------
# Audio generation (pure Python, no external dependencies)
# ---------------------------------------------------------------------------

def generate_mono_tone(freq, num_samples, sample_rate=48000):
    """Return raw mono 16-bit little-endian PCM sine tone."""
    data = bytearray()
    max_val = 2**15 - 1
    for i in range(num_samples):
        t = i / sample_rate
        val = int(0.5 * max_val * math.sin(2 * math.pi * freq * t))
        data.extend(struct.pack('<h', val))
    return bytes(data)

# ---------------------------------------------------------------------------
# AAF helpers
# ---------------------------------------------------------------------------

def register_channel_combiner(f):
    """
    Register the Audio Channel Combiner OperationDef and its ParameterDefs
    in the AAF dictionary. Call once per file.
    """

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
    # NumberInputs=1 matches Pro Tools' own exports. The AAF spec might
    # suggest this should be 2 (or N), but PT writes 1 and reads it back.
    op_def['NumberInputs'].value = 1
    op_def['OperationCategory'].value = 'OperationCategory_Effect'
    op_def.parameters.extend([pd_byte_order, pd_effect_id])
    f.dictionary.register_def(op_def)

    return op_def, pd_byte_order, pd_effect_id


def create_mono_mob_chain(f, clip_name, channel_suffix, edit_rate,
                           pcm_bytes, sample_rate, sample_width, num_frames):
    """
    Create a complete per-channel mob chain with embedded mono audio:

        TapeDescriptor SourceMob  (end of chain)
            <- PCMDescriptor SourceMob  (holds embedded PCM essence)
                <- MasterMob  (named "ClipName.L", "ClipName.R", etc.)

    Returns (master_mob, master_slot).
    """

    total_eu = int(num_frames * 30000 / (sample_rate * 1001))

    # --- TapeDescriptor SourceMob (terminates the chain) ---
    tape_mob = f.create.SourceMob()
    tape_mob.name = "Pro Tools:Example.ptx"
    tape_mob.descriptor = f.create.TapeDescriptor()

    tape_slot = tape_mob.create_timeline_slot(edit_rate=edit_rate)
    end_clip = f.create.SourceClip(media_kind='sound')
    end_clip.length = total_eu
    tape_slot.segment = end_clip

    f.content.mobs.append(tape_mob)

    # --- PCMDescriptor SourceMob (embedded mono audio) ---
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

    # Write audio data into the AAF
    essencedata = f.create.EssenceData()
    essencedata.mob_id = source_mob.mob_id
    f.content.essencedata.append(essencedata)
    stream = essencedata.open('w')
    stream.write(pcm_bytes)

    source_slot = source_mob.create_timeline_slot(edit_rate=edit_rate)
    source_slot.segment = tape_mob.create_source_clip(
        slot_id=tape_slot.slot_id, length=total_eu)

    # --- MasterMob ---
    master_mob = f.create.MasterMob()
    master_mob.name = "%s.%s" % (clip_name, channel_suffix)
    f.content.mobs.append(master_mob)

    master_slot = master_mob.create_timeline_slot(edit_rate=edit_rate)
    master_slot.segment = source_mob.create_source_clip(
        slot_id=source_slot.slot_id, media_kind='sound')

    return master_mob, master_slot


def create_multichannel_aaf(output_path, layout_name, clip_name,
                             track_name, edit_rate='30000/1001'):
    """
    Create an AAF file with one multichannel track containing one clip.

    Parameters
    ----------
    output_path : str
        Where to write the AAF file.
    layout_name : str
        Channel layout: 'stereo', '5.1', or '7.1'.
    clip_name : str
        Base name for the clip (channel suffixes are appended automatically).
    track_name : str
        Name for the audio track in the composition.
    edit_rate : str
        Edit rate as fraction string (default: 29.97fps drop-frame).
    """

    channel_suffixes = CHANNELS[layout_name]
    track_format = TRACK_FORMAT[layout_name]

    sample_rate = 48000
    sample_width = 2  # 16-bit
    num_frames = 96000  # 2 seconds of audio

    total_eu = int(num_frames * 30000 / (sample_rate * 1001))
    clip_length = 30  # visible clip = 30 video frames (~1 second)
    clip_offset = 50  # gap before clip
    clip_start_in_media = (total_eu - clip_length) // 2  # center for handles

    with aaf2.open(output_path, 'w') as f:

        op_def, pd_byte_order, pd_effect_id = register_channel_combiner(f)

        # Build one mob chain per channel
        master_mobs = []
        master_slots = []
        for i, suffix in enumerate(channel_suffixes):
            freq = 440 + i * 100  # different frequency per channel
            pcm = generate_mono_tone(freq, num_frames, sample_rate)
            mm, ms = create_mono_mob_chain(
                f, clip_name, suffix, edit_rate,
                pcm, sample_rate, sample_width, num_frames)
            master_mobs.append(mm)
            master_slots.append(ms)

        # --- CompositionMob ---
        comp = f.create.CompositionMob()
        comp.name = os.path.splitext(os.path.basename(output_path))[0]
        comp['UsageCode'].value = 'Usage_TopLevel'
        f.content.mobs.append(comp)

        # Audio slot with _TRACK_FORMAT tag
        audio_slot = comp.create_timeline_slot(edit_rate=edit_rate)
        audio_slot['SlotName'].value = track_name

        tv = f.create.TaggedValue("_TRACK_FORMAT", track_format, 'aafInt32')
        audio_slot['TimelineMobAttributeList'].value = [tv]

        # Sequence: Filler + OperationGroup
        seq = f.create.Sequence(media_kind='sound')
        audio_slot.segment = seq

        filler = f.create.Filler(media_kind='sound', length=clip_offset)
        seq.components.append(filler)

        # --- OperationGroup (Audio Channel Combiner) ---
        op_group = f.create.OperationGroup(
            op_def, length=clip_length, media_kind='sound')

        # Tagged value on the OperationGroup
        tv2 = f.create.TaggedValue("_IGNORE_TRACKING", 0, 'aafInt32')
        op_group['ComponentAttributeList'].value = [tv2]

        # Parameters (same for all formats)
        op_group.parameters.append(
            f.create.ConstantValue(pd_byte_order, BYTE_ORDER_VALUE))
        op_group.parameters.append(
            f.create.ConstantValue(pd_effect_id, EFFECT_ID_BYTES))

        # One SourceClip input per channel, in channel order
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
        tc.start = 107892  # 01:00:00;00 DF
        tc.length = clip_offset + clip_length
        tc_slot.segment = tc

    return output_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Create a stereo example
    stereo_path = os.path.join(output_dir, 'stereo_example.aaf')
    create_multichannel_aaf(
        stereo_path,
        layout_name='stereo',
        clip_name='StereoTone',
        track_name='MX 1',
    )
    print("Created: %s (%d bytes)" % (stereo_path, os.path.getsize(stereo_path)))

    # Create a 5.1 surround example
    surround_path = os.path.join(output_dir, 'surround_51_example.aaf')
    create_multichannel_aaf(
        surround_path,
        layout_name='5.1',
        clip_name='SurroundTone',
        track_name='SFX 5.1',
    )
    print("Created: %s (%d bytes)" % (surround_path, os.path.getsize(surround_path)))

    print("\nDone. Import these AAFs into Pro Tools to verify multichannel tracks.")


if __name__ == '__main__':
    main()
