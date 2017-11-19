from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
import os
from .fractions import AAFFraction
from . import video
from . import audio

MediaContainerGUIDs = {
"Generic"        : (UUID("b22697a2-3442-44e8-bb8f-7a1cd290ebf1"),
    ('.3g2',   '.3gp',  '.aac', '.au',  '.avi', '.bmp', '.dv', '.gif',
     '.jfif',  '.jpeg', '.jpg', '.m4a', '.mid', '.moov', '.mov',
     '.movie', '.mp2',  '.mp3', '.mp4', '.mpa', '.mpe', '.mpeg',
     '.mpg',   '.png',  '.psd', '.qt',  '.tif', '.tiff',)),
"AVCHD"          : (UUID("f37d624b307d4ef59bebc539046cad54"),
    ('.mts', '.m2ts',)),
"ImageSequencer" : (UUID("4964178d-b3d5-485f-8e98-beb89d92a5f4"),
    ('.dpx',)),
"CanonRaw"       : (UUID("0f299461-ee19-459f-8ae6-93e65c76a892"),
    ('.rmf',)),
"WaveAiff"       : (UUID("3711d3cc-62d0-49d7-b0ae-c118101d1a16"),
    ('.wav', '.wave', '.bwf', '.aif', '.aiff', '.aifc', '.cdda',)),
"MXF"            : (UUID("60eb8921-2a02-4406-891c-d9b6a6ae0645"),
    ('.mxf',)),
"QuickTime"      : (UUID("781f84b7-b989-4534-8a07-c595cb9a6fb8"),
    ('.mov',  '.mp4',  '.m4v',   '.mpg',  '.mpe', '.mpeg', '.3gp', '.3g2',
     '.qt',   '.moov', '.movie', '.avi',  '.mp2', '.mp3',  '.m4a', '.wav',
     '.aiff', '.aif',  '.au',    '.aac',  '.mid', '.mpa',  '.gif', '.jpg',
     '.jpeg', '.jfif', '.tif',   '.tiff', '.png', '.bmp',  '.psd', '.dv')),
}

def pixel_sizes(pix_fmt):

    h_samp = 2
    v_samp = 2

    depth = 8
    if pix_fmt.count('420'):
        h_samp = 2
        v_samp = 2
    elif pix_fmt.count('444'):
        h_samp = 4
        v_samp = 4

    for i in [8, 10, 12, 16]:
        if pix_fmt.count("p%d" % i):
            depth = i
            break

    return (depth, h_samp, v_samp)

def get_avc_compression(meta):

    profile = meta.get('profile')
    key = 'CompressedPicture'
    if profile  == "Baseline":
        key = 'AVCBaselineUnconstrained'
    elif profile == "Constrained Baseline":
        key = 'AVCConstrainedBaselineUnconstrained'
    elif profile == "Main":
        key = 'AVCMainUnconstrained'
    elif profile == "Extended":
        key ='AVCExtendedUnconstrained'
    elif profile == "High":
        key = 'AVCHighUnconstrained'
    elif profile == "High 10":
        key = 'AVCHigh10Unconstrained'
    elif profile == "High 10 Intra":
        key = 'AVCHigh10IntraUnconstrained'
    elif profile == "High 4:2:2":
        key = 'AVCHigh422Unconstrained'
    elif profile == "High 4:2:2 Intra":
        key = 'AVCHigh422IntraUnconstrained'
    # elif profile == "High 4:4:4":
    #     key = 'AVCHigh444IntraUnconstrained'
    elif profile == "High 4:4:4 Predictive":
        key = 'AVCHigh444PredictiveUnconstrained'
    elif profile == "High 4:4:4 Intra":
        key = 'AVCHigh444IntraUnconstrained'
    elif profile == 'CAVLC 4:4:4':
        key = 'AVCCAVLC444IntraUnconstrained'

    return video.compression_ids[key]

def get_compression(meta):
    codec_name = meta.get('codec_name', None)
    if codec_name == 'mjpeg':
        return video.compression_ids['mjpeg']
    if codec_name == 'h264':
        return get_avc_compression(meta)

    return video.compression_ids['CompressedPicture']

def create_video_descriptor(f, meta):
    d = f.create.CDCIDescriptor()

    depth, h_samp, v_samp = pixel_sizes(meta['pix_fmt'])

    width = meta['width']
    height = meta['height']

    # aspect_ratio = meta.get('display_aspect_ratio', "").replace(":", '/')
    aspect_ratio = "%d/%d" % (width, height)

    d['ComponentWidth'].value = depth
    d['HorizontalSubsampling'].value = h_samp
    d['VerticalSubsampling'].value = v_samp
    d['FrameLayout'].value = 'FullFrame'

    d['VideoLineMap'].value = [0,0]
    d['ImageAspectRatio'].value = aspect_ratio

    d['StoredWidth'].value = width
    d['StoredHeight'].value = height
    d['SampleRate'].value =  meta['avg_frame_rate']
    # compression = meta.get('compression', None)
    # print(meta)
    # raise Exception()

    compression = get_compression(meta)

    d['Compression'].value = compression
    # d['Compression'].value = UUID('04010202-0000-0000-060e-2b3404010101')
    d['Length'].value = int(meta['nb_frames'])

    return d

def create_audio_descriptor(f, meta):

    d = f.create.PCMDescriptor()
    rate = meta['sample_rate']
    d['SampleRate'].value = rate
    d['AudioSamplingRate'].value = rate

    d['Channels'].value = meta['channels']
    d['AverageBPS'].value = int(meta['bit_rate'])

    bit_depth, block_align = audio.audio_format_sizes.get(meta['sample_fmt'], (0,0))

    d['QuantizationBits'].value = bit_depth
    d['BlockAlign'].value = block_align

    duration = float(meta['duration'])
    d['Length'].value = int(duration * float(rate))

    # CompressedPictureCoding smpte ul
    # d['Compression'].value = UUID('040102020000-0000-060e-2b3404010101')
    return d


def create_network_locator(f, path):
    n = f.create.NetworkLocator()
    n['URLString'].value = path
    return n


def guess_edit_rate(metadata):

    for st in metadata['streams']:
        codec_type = st['codec_type']
        if codec_type == 'video':
            return AAFFraction(st['avg_frame_rate'])

def guess_length(metadata, edit_rate):
    for st in metadata['streams']:
        codec_type = st['codec_type']
        if codec_type == 'video':
            return int(st['nb_frames'])


def create_ama_link(f, path, metadata, container="Generic"):

    container_guid, formats = MediaContainerGUIDs[container]
    edit_rate = guess_edit_rate(metadata)
    length = guess_length(metadata, edit_rate)
    tape_length = 4142016
    prefix ="file://"
    basename = os.path.basename(path)
    path = prefix + path

    master_mob = f.create.MasterMob()
    src_mob = f.create.SourceMob()
    tape_mob = f.create.SourceMob()

    master_mob.name = basename

    f.content.mobs.append(master_mob)
    f.content.mobs.append(src_mob)
    f.content.mobs.append(tape_mob)

    tape_mob.descriptor = f.create.ImportDescriptor()
    tape_mob.descriptor['MediaContainerGUID'].value = container_guid
    tape_mob.descriptor['Locator'].append(create_network_locator(f, path))

    t = tape_mob.create_empty_sequence_slot(edit_rate, media_kind='timecode')
    tc = f.create.Timecode(int(float(edit_rate)+0.5), drop=False)
    tc.length = tape_length
    tc.start = 0
    t.segment.length = tape_length
    t.segment.components.append(tc)

    descriptors = []

    for st in metadata['streams']:

        codec_type = st['codec_type']
        if codec_type == 'video':
            desc = create_video_descriptor(f, st)
            desc['Locator'].append(create_network_locator(f, path))
            desc['MediaContainerGUID'].value = container_guid
            descriptors.append(desc)

            tape_slot = tape_mob.create_empty_sequence_slot(edit_rate, media_kind='picture')
            tape_slot.segment.length = tape_length
            nul_ref = f.create.SourceClip(media_kind='picture')
            nul_ref.length = tape_length
            tape_slot.segment.components.append(nul_ref)

            tape_clip = tape_mob.create_source_clip(tape_slot.id)
            tape_clip.length = length
            tape_clip.media_kind = 'picture'

            src_slot = src_mob.create_empty_sequence_slot(edit_rate, media_kind='picture')
            src_slot.segment.length = length
            src_slot.segment.components.append(tape_clip)

            # src_slot = src_mob.create_empty_slot(edit_rate, media_kind='picture')
            # src_slot.segment.length = length

            clip = src_mob.create_source_clip(src_slot.id)
            clip.length = length
            clip.media_kind = 'picture'

            master_slot = master_mob.create_empty_sequence_slot(edit_rate, media_kind='picture')
            master_slot.segment.components.append(clip)
            master_slot.segment.length = length

        elif codec_type == 'audio':
            rate = st['sample_rate']
            desc = create_audio_descriptor(f, st)
            desc['Locator'].append(create_network_locator(f, path))
            desc['MediaContainerGUID'].value = container_guid
            descriptors.append(desc)
            for i in range(st['channels']):

                tape_slot = tape_mob.create_empty_sequence_slot(edit_rate, media_kind='sound')
                tape_slot.segment.length = tape_length
                nul_ref = f.create.SourceClip(media_kind='sound')
                nul_ref.length = tape_length
                tape_slot.segment.components.append(nul_ref)

                tape_clip = tape_mob.create_source_clip(tape_slot.id)
                tape_clip.length = length
                tape_clip.media_kind = 'sound'

                src_slot =  src_mob.create_empty_sequence_slot(edit_rate, media_kind='sound')
                src_slot.segment.length = length
                src_slot.segment.components.append(tape_clip)
                src_slot['PhysicalTrackNumber'].value = i+1

                # src_slot =  src_mob.create_empty_slot(edit_rate, media_kind='sound')
                # src_slot.segment.length = length

                clip = src_mob.create_source_clip(src_slot.id)
                clip.length = length
                clip.media_kind = 'sound'

                master_slot = master_mob.create_empty_sequence_slot(edit_rate, media_kind='sound')
                master_slot.segment.components.append(clip)
                master_slot.segment.length = length

                master_slot['PhysicalTrackNumber'].value = i+1

    if len(descriptors) > 1:
        desc = f.create.MultipleDescriptor()
        desc['Length'].value = 0
        desc['SampleRate'].value = edit_rate
        desc['MediaContainerGUID'].value = container_guid
        desc['Locator'].append(create_network_locator(f, path))
        desc['FileDescriptors'].value = descriptors
        src_mob.descriptor = desc
    else:
        src_mob.descriptor = descriptors[0]
