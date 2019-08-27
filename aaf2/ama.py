from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
)

import os
import sys
from .rational import AAFRational
from . import video, audio, mxf
from .auid import AUID

import struct

MediaContainerGUID = {
    "Generic": (AUID("b22697a2-3442-44e8-bb8f-7a1cd290ebf1"),
                ('.3g2', '.3gp', '.aac', '.au', '.avi', '.bmp', '.dv', '.gif',
                 '.jfif', '.jpeg', '.jpg', '.m4a', '.mid', '.moov', '.mov',
                 '.movie', '.mp2', '.mp3', '.mp4', '.mpa', '.mpe', '.mpeg',
                 '.mpg', '.png', '.psd', '.qt', '.tif', '.tiff',)),
    "AVCHD": (AUID("f37d624b307d4ef59bebc539046cad54"),
              ('.mts', '.m2ts',)),
    "ImageSequencer": (AUID("4964178d-b3d5-485f-8e98-beb89d92a5f4"),
                       ('.dpx',)),
    "CanonRaw": (AUID("0f299461-ee19-459f-8ae6-93e65c76a892"),
                 ('.rmf',)),
    "WaveAiff": (AUID("3711d3cc-62d0-49d7-b0ae-c118101d1a16"),
                 ('.wav', '.wave', '.bwf', '.aif', '.aiff', '.aifc', '.cdda',)),
    "MXF": (AUID("60eb8921-2a02-4406-891c-d9b6a6ae0645"),
            ('.mxf',)),
    "QuickTime": (AUID("781f84b7-b989-4534-8a07-c595cb9a6fb8"),
                  ('.mov', '.mp4', '.m4v', '.mpg', '.mpe', '.mpeg', '.3gp', '.3g2',
                   '.qt', '.moov', '.movie', '.avi', '.mp2', '.mp3', '.m4a', '.wav',
                   '.aiff', '.aif', '.au', '.aac', '.mid', '.mpa', '.gif', '.jpg',
                   '.jpeg', '.jfif', '.tif', '.tiff', '.png', '.bmp', '.psd', '.dv')),
}


def get_wave_fmt(path):
    """
    Returns a bytearray of the WAVE RIFF header and fmt
    chunk for a `WAVEDescriptor` `Summary`
    """
    with open(path, 'rb') as file:
        if file.read(4) != b"RIFF":
            return None
        data_size = file.read(4)  # container size
        if file.read(4) != b"WAVE":
            return None
        while True:
            chunkid = file.read(4)
            sizebuf = file.read(4)
            if len(sizebuf) < 4 or len(chunkid) < 4:
                return None
            size = struct.unpack(b'<L', sizebuf)[0]
            if chunkid[0:3] != b"fmt":
                if size % 2 == 1:
                    seek = size + 1
                else:
                    seek = size
                file.seek(seek, 1)
            else:
                return bytearray(b"RIFF" + data_size + b"WAVE" + chunkid + sizebuf + file.read(size))

def get_aifc_fmt(path):
    """
    Compute the AIFC header information for a `AIFCDescriptor` `Summary`

    :param path: file to read chunk from
    :return: a `bytearray`
    """
    with open(path, 'rb') as file:
        if file.read(4) != b"FORM":
            return None
        data_size = file.read(4)
        signature = file.read(4)
        if signature not in (b"AIFF", b"AIFC"):
            return None

        while True:
            chunkid = file.read(4)
            sizebuf = file.read(4)
            if len(sizebuf) < 4 or len(chunkid) < 4:
                return None
            size = struct.unpack(">L", sizebuf)[0]
            if chunkid != b"COMM":
                if size % 2 == 1:
                    seek = size + 1
                else:
                    seek = size
                file.seek(seek, 1)
            else:
                return bytearray(b"FORM" + data_size + signature + chunkid + sizebuf + file.read(size))


def create_network_locator(f, absolute_path):
    n = f.create.NetworkLocator()
    if sys.version_info[0] < 3:
        import urllib
        n['URLString'].value = 'file://' + urllib.pathname2url(absolute_path)
    else:
        import pathlib
        n['URLString'].value = pathlib.Path(absolute_path).as_uri()

    return n

class FormatInfo:
    """
    Provides convenient access to commonly-used datums
    """

    def __init__(self, metadata):
        self.metadata = metadata

    @property
    def streams(self):
        for stream in self.metadata['streams']:
            yield StreamInfo(stream)

    @property
    def first_sound_stream(self):
        return next((stream for stream in self.streams if stream.is_sound), None)


    @property
    def first_picture_stream(self):
        return next((stream for stream in self.streams if stream.is_picture), None)

    def create_descriptor(self, f, path):
        if self.metadata['format']['format_name'] in ('wav',):
            return self.create_wav_descriptor(f, path)

        if self.metadata['format']['format_name'] in ('aiff',):
            return self.create_aifc_descriptor(f,path)

        elif self.metadata['format']['format_long_name'] == 'QuickTime / MOV':
            return self.create_multistream_descriptor(f, path)
        else:
            return None

    @property
    def container_guid(self):
        if self.metadata['format']['format_name'] in ('wav',):
            return MediaContainerGUID['WaveAiff'][0]

        # if self.metadata['format']['format_long_name'] == 'QuickTime / MOV':
        #     return MediaContainerGUID['QuickTime'][0]

        # just using the generic appears to work
        return MediaContainerGUID['Generic'][0]

    @property
    def edit_rate(self):
        """
        :return: The edit rate of the first picture stream, or if there are none, the first sound stream.
        """
        pix = self.first_picture_stream
        if pix is None:
            return self.first_sound_stream.edit_rate
        else:
            return pix.edit_rate

    @property
    def length(self):
        """
        :return: The length of the first picture stream, or if there are none, the first sound stream.
        """
        pix = self.first_picture_stream
        if pix is None:
            return self.first_sound_stream.length
        else:
            return pix.length

    def create_wav_descriptor(self, f, path):
        d = f.create.WAVEDescriptor()
        stream = self.first_sound_stream
        d['SampleRate'].value = stream.edit_rate
        d['Summary'].value = get_wave_fmt(path)
        d['Length'].value = stream.length
        d['ContainerFormat'].value = f.dictionary.lookup_containerdef("AAF")
        d['Locator'].append(create_network_locator(f, path))
        return d

    def create_aifc_descriptor(self, f, path):
        d = f.create.AIFCDescriptor()
        stream = self.first_sound_stream
        d['SampleRate'].value = stream.edit_rate
        d['Summary'].value = get_aifc_fmt(path)
        d['Length'].value = stream.length
        d['ContainerFormat'].value = f.dictionary.lookup_containerdef("AAF")
        d['Locator'].append(create_network_locator(f, path))
        return d

    def coalesce_descriptors(self, f, descriptors, path):
        if len(descriptors) > 1:
            desc = f.create.MultipleDescriptor()
            desc['Length'].value = self.length
            desc['SampleRate'].value = self.edit_rate
            desc['MediaContainerGUID'].value = self.container_guid
            desc['Locator'].append(create_network_locator(f, path))
            desc['FileDescriptors'].value = descriptors
            return desc
        else:
            return descriptors[0]

    def create_multistream_descriptor(self, f, path):
        descriptor_list = []

        for stream in self.streams:
            if stream.is_picture:
                desc = stream.create_video_descriptor(f)
                descriptor_list.append(desc)
                desc['Locator'].append(create_network_locator(f, path))

            elif stream.is_sound:
                desc = stream.create_pcm_descriptor(f)
                descriptor_list.append(desc)
                desc['Locator'].append(create_network_locator(f, path))

        return self.coalesce_descriptors(f, descriptor_list, path)


class StreamInfo:
    def __init__(self, metadata):
        self.metadata = metadata

    @property
    def codec_type(self):
        return self.metadata['codec_type']

    @property
    def codec_name(self):
        return self.metadata['codec_name']

    @property
    def is_sound(self):
        return self.codec_type == 'audio'

    @property
    def is_picture(self):
        return self.codec_type == 'video'

    @property
    def edit_rate(self):
        if self.is_sound:
            return AAFRational(self.metadata['sample_rate'])
        elif self.is_picture:
            return AAFRational(self.metadata['avg_frame_rate'])

    @property
    def length(self):
        if self.is_sound:
            return int(self.metadata['duration_ts'])
        elif self.is_picture:
            return int(self.metadata['nb_frames'])

    @property
    def physical_track_count(self):
        if self.is_sound:
            return self.metadata['channels']

    def create_pcm_descriptor(self, f):
        if not self.is_sound:
            return None

        d = f.create.PCMDescriptor()
        d['SampleRate'].value = self.edit_rate
        d['AudioSamplingRate'].value = self.edit_rate

        d['Channels'].value = self.physical_track_count
        d['AverageBPS'].value = int(self.metadata['bit_rate'])

        bit_depth, block_align = audio.audio_format_sizes.get(self.metadata['sample_fmt'], (0, 0))

        d['QuantizationBits'].value = bit_depth
        d['BlockAlign'].value = block_align

        d['Length'].value = self.length

        d['Compression'].value = AUID('04020202-0000-0000-060e-2b3404010101')
        return d

    def pixel_sizes(self):
        if not self.is_picture:
            return None

        pix_fmt = self.metadata['pix_fmt']
        h_samp = 2
        v_samp = 2

        depth = 8
        if pix_fmt.count('420'):
            h_samp = 2
            v_samp = 2
        elif pix_fmt.count('422'):
            h_samp = 2
            v_samp = 1
        elif pix_fmt.count('444'):
            h_samp = 1
            v_samp = 1

        for i in [8, 10, 12, 16]:
            if pix_fmt.count("p%d" % i):
                depth = i
                break

        return (depth, h_samp, v_samp)

    def get_avc_compression(self):
        if not self.is_picture:
            return None

        profile = self.metadata.get('profile', None)
        key = 'CompressedPicture'
        if profile == "Baseline":
            key = 'AVCBaselineUnconstrained'
        elif profile == "Constrained Baseline":
            key = 'AVCConstrainedBaselineUnconstrained'
        elif profile == "Main":
            key = 'AVCMainUnconstrained'
        elif profile == "Extended":
            key = 'AVCExtendedUnconstrained'
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
        elif profile == "High 4:4:4":
            # key = 'AVCHigh444IntraUnconstrained'
            key = 'CompressedPicture'
        elif profile == "High 4:4:4 Predictive":
            # key = 'AVCHigh444PredictiveUnconstrained'
            key = 'CompressedPicture'
        elif profile == "High 4:4:4 Intra":
            # key = 'AVCHigh444IntraUnconstrained'
            key = 'CompressedPicture'
        elif profile == 'CAVLC 4:4:4':
            # key = 'AVCCAVLC444IntraUnconstrained'
            key = 'CompressedPicture'

        return video.compression_ids[key]

    def get_compression(self):
        if not self.is_picture:
            return None

        codec_name = self.metadata.get('codec_name', None)
        if codec_name == 'mjpeg':
            return video.compression_ids['mjpeg']
        if codec_name == 'h264':
            return self.get_avc_compression()

        return video.compression_ids['CompressedPicture']

    def create_video_descriptor(self, f):
        if not self.is_picture:
            return None

        d = f.create.CDCIDescriptor()

        depth, h_samp, v_samp = self.pixel_sizes()

        width = self.metadata['width']
        height = self.metadata['height']

        aspect_ratio = "%d/%d" % (width, height)

        d['ComponentWidth'].value = depth
        d['HorizontalSubsampling'].value = h_samp
        d['VerticalSubsampling'].value = v_samp
        d['FrameLayout'].value = 'FullFrame'

        d['VideoLineMap'].value = [0, 0]
        # d['VideoLineMap'].value = [42, 0]
        d['ImageAspectRatio'].value = aspect_ratio

        d['StoredWidth'].value = width
        d['StoredHeight'].value = height
        d['SampleRate'].value = self.metadata['avg_frame_rate']
        compression = self.get_compression()

        d['Compression'].value = compression

        # d['ResolutionID'].value =  2900
        d['Length'].value = int(self.length)

        return d


def create_media_link(f, path, metadata):
    """
    Create an essence linked to external media and all obligatory mobs and data structures required by
    the edit spec.

    The returned :class:`aaf.mobs.MasterMob` will have one slot for each video stream and each audio channel
    in the file at `path`.

    Example: The linked file is a Quicktime movie with picture and a stereo audio track. This function will create a
    SourceMob with three slots, one picture slot, and two sound slots, for audio channels one and two respectively.
    The function will also create a derivation SourceMob, linked to these slots.

    :param f: The :class:`aaf.File` to add this link to
    :param path: A path recognizable to `os.path`
    :param metadata: Pre-fetched media description (in the form of a dictionary)
        from "ffprobe -show_format -show_streams"
    :return: A `aaf.mobs.MasterMob` linked to the file at link.
    """

    def tape_mob_for_format(name, format_info):
        tape_mob = f.create.SourceMob()
        tape_mob.name = name
        picture = format_info.first_picture_stream
        if picture is not None:
            pix_slot = tape_mob.create_picture_slot(edit_rate=picture.edit_rate)
            pix_slot.segment.length = picture.length
            tape_source_clip = f.create.SourceClip(media_kind='picture')
            tape_source_clip.length = picture.length
            pix_slot.segment.components.append(tape_source_clip)

        sound = format_info.first_sound_stream
        if sound is not None:
            for channel in range(sound.physical_track_count):
                sound_slot = tape_mob.create_sound_slot(edit_rate=sound.edit_rate)
                sound_slot.segment.length = sound.length
                tape_source_clip = f.create.SourceClip(media_kind='sound')
                tape_source_clip.length = sound.length
                sound_slot.segment.components.append(tape_source_clip)
                # not setting PhysicalTrackNumber here because we didn't before

        f.content.mobs.append(tape_mob)
        tape_mob.descriptor = f.create.ImportDescriptor()

        return tape_mob

    def append_source_to_mob_as_new_slots(from_mob, to_mob):
        sound_physical_track = 1
        for from_slot in from_mob.slots:
            slot_kind = from_slot.media_kind
            if slot_kind in ("Picture", "Sound"):
                from_clip = from_mob.create_source_clip(slot_id=from_slot.slot_id, media_kind=slot_kind)
                to_slot = to_mob.create_empty_sequence_slot(edit_rate=from_slot.edit_rate,
                                                            media_kind=from_clip.media_kind)
                to_slot.segment.components.append(from_clip)

                if slot_kind == 'Sound':
                    to_slot['PhysicalTrackNumber'].value = sound_physical_track
                    sound_physical_track += 1

    def source_mob_from_tape_mob(name, tape_mob):
        source_mob = f.create.SourceMob()
        source_mob.name = name

        append_source_to_mob_as_new_slots(from_mob=tape_mob, to_mob=source_mob)
        f.content.mobs.append(source_mob)

        return source_mob

    def master_mob_from_source_mob(name, source_mob):
        master_mob = f.create.MasterMob()
        master_mob.name = name

        append_source_to_mob_as_new_slots(from_mob=source_mob, to_mob=master_mob)

        f.content.mobs.append(master_mob)

        return master_mob

    def create_mobs(name, format_info):
        tmob = tape_mob_for_format(name + ' <TAPE MOB>', format_info)
        smob = source_mob_from_tape_mob(name + ' <SOURCE MOB>', tmob)
        mmob = master_mob_from_source_mob(name, smob)

        if format_info.first_picture_stream is not None:
            # MC Quicktime plugin will error if this is not set
            smob.comments['Video'] = format_info.first_picture_stream.codec_name

        return mmob, smob, tmob

    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)

    if ext == '.mxf' or ext == '.MXF':
        m = mxf.MXFFile(path)
        m.ama = True
        m.dump()
        return m.link(f)

    format_info = FormatInfo(metadata)
    source_descriptor = format_info.create_descriptor(f, path)

    if source_descriptor is None:
        return None

    master_mob, source_mob, tape_mob = create_mobs(name, format_info)
    source_mob.descriptor = source_descriptor
    return master_mob, source_mob, tape_mob
