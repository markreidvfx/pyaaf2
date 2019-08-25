from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import struct
import io
from .utils import (read_u8, read_u16be, read_s16be,
                    read_u32be, read_s32be,
                    read_u64be, read_s64be)
import os

def read_double_be(f):
    (result, ) = struct.unpack(b'>d', f.read(8))
    return result

INT64_MAX=0x7FFFFFFFFFFFFFFF

MOV_CLASSES = {}
video_tags =[
    b'raw ',
    b'yuv2',
    b'2vuy',
    b'yuvs',
    b'L555',
    b'L565',
    b'B565',
    b'24BG',
    b'BGRA',
    b'RGBA',
    b'ABGR',
    b'b16g',
    b'b48r',
    b'b64a',
    b'bxbg',
    b'bxrg',
    b'bxyv',
    b'NO16',
    b'DVOO',
    b'R420',
    b'R411',
    b'R10k',
    b'R10g',
    b'r210',
    b'AVUI',
    b'AVrp',
    b'SUDS',
    b'v210',
    b'bxy2',
    b'v308',
    b'v408',
    b'v410',
    b'Y41P',
    b'yuv4',
    b'Y216',
    b'jpeg',
    b'mjpa',
    b'AVDJ',
    b'dmb1',
    b'mjpb',
    b'SVQ1',
    b'svq1',
    b'svqi',
    b'SVQ3',
    b'mp4v',
    b'DIVX',
    b'XVID',
    b'3IV2',
    b'h263',
    b's263',
    b'dvcp',
    b'dvc ',
    b'dvpp',
    b'dv5p',
    b'dv5n',
    b'AVdv',
    b'AVd1',
    b'dvhq',
    b'dvhp',
    b'dvh1',
    b'dvh2',
    b'dvh4',
    b'dvh5',
    b'dvh6',
    b'dvh3',
    b'VP31',
    b'rpza',
    b'cvid',
    b'8BPS',
    b'smc ',
    b'rle ',
    b'rle1',
    b'WRLE',
    b'qdrw',
    b'WRAW',
    b'hev1',
    b'hvc1',
    b'dvhe',
    b'avc1',
    b'avc2',
    b'avc3',
    b'avc4',
    b'ai5p',
    b'ai5q',
    b'ai52',
    b'ai53',
    b'ai55',
    b'ai56',
    b'ai1p',
    b'ai1q',
    b'ai12',
    b'ai13',
    b'ai15',
    b'ai16',
    b'AVin',
    b'aivx',
    b'rv64',
    b'xalg',
    b'avlg',
    b'dva1',
    b'dvav',
    b'vp08',
    b'vp09',
    b'av01',
    b'm1v ',
    b'm1v1',
    b'mpeg',
    b'mp1v',
    b'm2v1',
    b'hdv1',
    b'hdv2',
    b'hdv3',
    b'hdv4',
    b'hdv5',
    b'hdv6',
    b'hdv7',
    b'hdv8',
    b'hdv9',
    b'hdva',
    b'mx5n',
    b'mx5p',
    b'mx4n',
    b'mx4p',
    b'mx3n',
    b'mx3p',
    b'xd51',
    b'xd54',
    b'xd55',
    b'xd59',
    b'xd5a',
    b'xd5b',
    b'xd5c',
    b'xd5d',
    b'xd5e',
    b'xd5f',
    b'xdv1',
    b'xdv2',
    b'xdv3',
    b'xdv4',
    b'xdv5',
    b'xdv6',
    b'xdv7',
    b'xdv8',
    b'xdv9',
    b'xdva',
    b'xdvb',
    b'xdvc',
    b'xdvd',
    b'xdve',
    b'xdvf',
    b'xdhd',
    b'xdh2',
    b'AVmp',
    b'mp2v',
    b'mjp2',
    b'tga ',
    b'tiff',
    b'gif ',
    b'png ',
    b'MNG ',
    b'vc-1',
    b'avs2',
    b'drac',
    b'AVdn',
    b'AVdh',
    b'H263',
    b'3IVD',
    b'AV1x',
    b'AVup',
    b'sgi ',
    b'dpx ',
    b'exr ',
    b'apch',
    b'apcn',
    b'apcs',
    b'apco',
    b'ap4h',
    b'ap4x',
    b'flic',
    b'icod',
    b'Hap1',
    b'Hap5',
    b'HapY',
    b'HapA',
    b'HapM',
    b'DXD3',
    b'DXDI',
    b'M0R0',
    b'M0RA',
    b'M0RG',
    b'M0Y2',
    b'M8RG',
    b'M8RA',
    b'M8G0',
    b'M8Y0',
    b'M8Y2',
    b'M8Y4',
    b'M8YA',
    b'M2RA',
    b'M2RG',
    b'Shr0',
    b'Shr1',
    b'Shr2',
    b'Shr3',
    b'Shr4',
    b'Shr5',
    b'Shr6',
    b'Shr7',
    b'pxlt',
]

sound_tags = [
    b'mp4a',
    b'ac-3',
    b'sac3',
    b'ima4',
    b'alac',
    b'samr',
    b'sawb',
    b'dtsc',
    b'dtsh',
    b'dtsl',
    b'dtse',
    b'DTS ',
    b'ec-3',
    b'vdva',
    b'dvca',
    b'agsm',
    b'ilbc',
    b'MAC3',
    b'MAC6',
    b'.mp1',
    b'.mp2',
    b'.mp3',
    b'nmos',
    b'NELL',
    b'alaw',
    b'fl32',
    b'fl32',
    b'fl64',
    b'fl64',
    b'ulaw',
    b'twos',
    b'sowt',
    b'lpcm',
    b'lpcm',
    b'in24',
    b'in24',
    b'in32',
    b'in32',
    b'sowt',
    b'raw ',
    b'NONE',
    b'Qclp',
    b'Qclq',
    b'sqcp',
    b'QDM2',
    b'QDMC',
    b'spex',
    b'SPXN',
    b'sevc',
    b'ssmv',
    b'fLaC',
    b'Opus',
]

def register_mov_class(classobj):
    if isinstance(classobj.class_id, list):
        for class_id in classobj.class_id:
            MOV_CLASSES[class_id] = classobj
    else:
        MOV_CLASSES[classobj.class_id] = classobj
    return classobj



class Atom(object):
    def __init__(self):
        self.pos = 0
        self.class_id = b''
        self.size = 0
        self.children = []

    def __repr__(self):

        return '<{} class_id: {} pos: {} size: {}>'.format(self.__class__.__name__, repr(self.class_id), self.pos, self.size)

    def dump(self, space=''):
        print("{}{}".format(space, self))
        for c in self.children:
            c.dump(space + '  ')

class Root(object):
    class_id = b'root'
    def __init__(self, f=None, atom=None):
        self.pos = 0
        self.size = 0
        self.data = {}
        self.children = []
        if atom:
            self.pos = atom.pos
            self.size = atom.size

    def __repr__(self):
        return '<{} class_id: {} pos: {} size: {}>'.format(self.__class__.__name__, repr(self.class_id), self.pos, self.size)

    def read(self, f):
        pass

    def dump(self, space=''):
        print('{}{}'.format(space, self))

        for key,value in sorted(self.data.items()):
            if isinstance(value, (bytearray, bytes)):
                value = repr(value)

            print("{}{}: {}".format(space + ' ', key, value))

        for c in self.children:
            c.dump(space + '  ')

@register_mov_class
class Wide(Root):
    class_id = b'wide'

@register_mov_class
class Mov(Root):
    class_id = b'moov'
    def read(self, f):
        read_default(f, self)

    @property
    def header(self):
        for item in self.children:
            if isinstance(item, MovieHeader):
                return item

    @property
    def tracks(self):
        for item in self.children:
            if isinstance(item, Track):
                yield item

@register_mov_class
class Track(Root):
    class_id = b'trak'
    def read(self, f):
        read_default(f, self)

    @property
    def header(self):
        for item in self.children:
            if isinstance(item, TrackHeader):
                return item
    @property
    def media(self):
        for item in self.children:
            if isinstance(item, MediaAtom):
                return item

    @property
    def info(self):
        return self.media.info

    @property
    def descriptor(self):
        for item in self.info.sample_table.descriptors:
            return item

    @property
    def media_kind(self):
        return self.media.handler.data.get('component_name', None)

@register_mov_class
class MediaAtom(Root):
    class_id = b'mdia'
    def read(self, f):
        read_default(f, self)

    @property
    def header(self):
        for item in self.children:
            if isinstance(item, MediaHeader):
                return item

    @property
    def handler(self):
        for item in self.children:
            if isinstance(item, MediaHandler):
                return item
    @property
    def info(self):
        for item in self.children:
            if isinstance(item, MediaInfo):
                return item

@register_mov_class
class MediaInfo(Root):
    class_id = b'minf'
    def read(self, f):
        read_default(f, self)

    @property
    def handler(self):
        for item in self.children:
            if isinstance(item, MediaHandler):
                return item

    @property
    def sample_table(self):
        for item in self.children:
            if isinstance(item, SampleTable):
                return item

@register_mov_class
class DataInfo(Root):
    class_id = b'dinf'
    def read(self, f):
        read_default(f, self)

@register_mov_class
class SampleTable(Root):
    class_id = b'stbl'
    def read(self, f):
        read_default(f, self)

    @property
    def descriptors(self):
        for item in self.children:
            if isinstance(item, SampleDescriptors):
                for d in item.children:
                    yield d
    @property
    def chunks(self, f):
        pass

@register_mov_class
class FileType(Root):
    class_id = b'ftyp'

    def read(self, f):
        self.data['major_brand'] = f.read(4)
        self.data['minor_version'] = read_s32be(f)
        compatible_brand_count = (self.size - 8) // 4
        compatible_brands = []
        for i in range(compatible_brand_count):
            v = f.read(4)
            if v == b'\x00\x00\x00\x00':
                continue
            compatible_brands.append(v)

        self.data['compatible_brands'] = compatible_brands


@register_mov_class
class MovieHeader(Root):
    class_id = b'mvhd'
    def __init__(self, f, atom):
        super(MovieHeader, self).__init__(f, atom)

    def read(self, f):
        start = f.tell()
        version = read_u8(f)
        flags = f.read(3)

        self.data['version'] = version

        if version == 1:
            creation_time = read_u64be(f)
            mod_time = read_u64be(f)
        else:
            creation_time = read_u32be(f)
            mod_time = read_u32be(f)

        self.data['time_scale'] = read_s32be(f)

        if version == 1:
            duration = read_u64be(f)
        else:
            duration = read_u32be(f)

        self.data['duration'] = duration

        prefer_scale = read_u32be(f)
        prefer_volume = read_u16be(f)

        # reserved
        f.read(10)

        display_matrix = []
        for i in range(3):
            display_matrix.append([])
            display_matrix[i].append(read_s32be(f))
            display_matrix[i].append(read_s32be(f))
            display_matrix[i].append(read_s32be(f))

        # print(display_matrix)

        preview_time = read_s32be(f)
        preview_duration = read_s32be(f)
        poster_time = read_s32be(f)
        selection_time = read_s32be(f)
        selection_duration = read_s32be(f)
        current_time = read_s32be(f)
        next_track_id = read_s32be(f)

        assert self.size == f.tell()- start

@register_mov_class
class TrackHeader(Root):
    class_id = b'tkhd'

    def read(self, f):
        start = f.tell()
        version = read_u8(f)
        flags = f.read(3)
        self.data['version'] = version

        if version == 1:
            creation_time = read_u64be(f)
            mod_time = read_u64be(f)
        else:
            creation_time = read_u32be(f)
            mod_time = read_u32be(f)

        self.data['track_id'] = read_u32be(f)

        # reserved
        read_u32be(f)

        if version == 1:
            duration = read_u64be(f)
        else:
            duration = read_u32be(f)

        self.data['duration'] = duration

        # reserved
        read_u32be(f)
        read_u32be(f)

        layer = read_u16be(f)
        alternate_group = read_u16be(f)
        volume = read_u16be(f)

        # reserved
        read_u16be(f)

        display_matrix = []
        for i in range(3):
            display_matrix.append([])
            display_matrix[i].append(read_s32be(f))
            display_matrix[i].append(read_s32be(f))
            display_matrix[i].append(read_s32be(f))

        width = read_u32be(f)
        height = read_u32be(f)
        self.data['width'] = width >> 16
        self.data['height'] = height >> 16

        assert self.size == f.tell() - start

@register_mov_class
class MediaHeader(Root):
    class_id = b'mdhd'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)
        self.data['version'] = version

        if version == 1:
            creation_time = read_u64be(f)
            mod_time = read_u64be(f)
        else:
            creation_time = read_u32be(f)
            mod_time = read_u32be(f)

        self.data['time_scale'] = read_s32be(f)
        if version == 1:
            duration = read_u64be(f)
        else:
            duration = read_u32be(f)

        self.data['duration'] = duration
        language = read_u16be(f)
        quality = read_u16be(f)

@register_mov_class
class MediaHandler(Root):
    class_id = b'hdlr'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        component_type = bytearray(f.read(4))
        component_subtype = bytearray(f.read(4))
        self.data['component_type'] = component_type
        self.data['component_subtype'] = component_subtype

        # Component manufacturer
        read_u32be(f)
        # Component flags
        read_u32be(f)
        # Component flags mask
        read_u32be(f)

        title_size = self.size - 24
        if title_size:
            title = f.read(title_size)
            b = io.BytesIO(title)
            length = read_u8(b)

            # remove length char if present
            if length == title_size - 1:
                title = title[1:]

            # strip off null terminator
            i = len(title)
            for i,c in enumerate(bytearray(title)):
                if c == 0:
                    break
            title = title[:i]
            self.data['component_name'] = title.decode('macroman')

@register_mov_class
class VideoMediaHeader(Root):
    class_id = b'vmhd'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        graphics_mode = read_u16be(f)
        self.data['graphics_mode'] = graphics_mode
        r = read_u16be(f)
        g = read_u16be(f)
        b = read_u16be(f)
        self.data['op_color'] = [r,g,b]

@register_mov_class
class SoundMediaHeader(Root):
    class_id = b'smhd'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        self.data['balance'] = read_s16be(f)

        #reserved
        read_s16be(f)

@register_mov_class
class DataRef(Root):
    class_id = b'dref'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        entries = read_u32be(f)
        for i in range(entries):
            size = read_u32be(f)
            next = f.tell() + size -4
            type = f.read(4)
            version = read_u8(f)
            flags = f.read(3)
            f.seek(next)

@register_mov_class
class SampleDescriptors(Root):
    class_id = b'stsd'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        entries = read_u32be(f)
        if self.pos == 85416:
            print('over', entries, self)
        for i in range(entries):
            size = read_u32be(f)
            if self.pos == 85416:
                print("over entry size", size)
            f.seek(-4, os.SEEK_CUR)
            atom = Atom()
            atom.size = size
            data = f.read(size)
            # print(data.encode("hex"))
            b = io.BytesIO(data)
            read_default(b, atom)
            self.children.extend(atom.children)

def read_sample_descriptor_header(f):
    # reseverd
    f.read(6)
    index = read_s16be(f)
    return index


class VideoSampleDescriptor(Root):

    def __init__(self, f=None, atom=None):
        super(VideoSampleDescriptor, self).__init__(f, atom)
        self.class_id = atom.class_id
        self.data['class_id'] = atom.class_id

    def read(self, f):
        start = f.tell()
        self.data['index'] = read_sample_descriptor_header(f)

        version = read_u16be(f)
        revision = read_u16be(f)

        self.data['vendor'] = bytearray(f.read(4))
        temporal_quality = read_s32be(f)
        spatial_quality = read_s32be(f)
        self.data['width'] = read_s16be(f)
        self.data['height'] = read_s16be(f)
        horizontal_resolution = read_s32be(f)
        vertical_resolution = read_s32be(f)
        data_size = read_s32be(f)
        frames_per_sample = read_s16be(f)

        name_size = read_u8(f)
        self.data['codec_name'] = f.read(min(name_size, 31)).decode('macroman')
        if name_size < 31:
            f.read(31-name_size)

        self.data['depth'] =  read_s16be(f)
        self.data['color_table_id'] = read_s16be(f)

        left = self.size - (f.tell() - start)
        if left > 0:
            remaining = f.read(left)
            atom = Atom()
            atom.size = left
            read_default(io.BytesIO(remaining), atom)
            self.children.extend(atom.children)

for tag in video_tags:
    MOV_CLASSES[tag] = VideoSampleDescriptor

class SoundSampleDescriptor(Root):

    def __init__(self, f=None, atom=None):
        super(SoundSampleDescriptor, self).__init__(f, atom)
        self.class_id = atom.class_id
        self.data['class_id'] = atom.class_id

    def read(self, f):
        start = f.tell()
        self.data['index'] = read_sample_descriptor_header(f)

        version = read_u16be(f)
        revision = read_u16be(f)
        self.data['version'] = version
        self.data['vendor'] = bytearray(f.read(4))
        self.data['channels'] = read_s16be(f)
        self.data['sample_byte_size'] = read_s16be(f)
        self.data['compression_id'] = read_s16be(f)
        self.data['packet_size'] = read_s16be(f)
        self.data['sample_rate'] = read_u32be(f) >> 16

        if version == 1:
            self.data['samples_per_frame'] = read_u32be(f)
            self.data['bytes_per_packet'] = read_u32be(f)
            self.data['bytes_per_frame'] = read_u32be(f)
            self.data['bytes_per_sample'] = read_u32be(f)
        elif version == 2:
            struct_size = read_u32be(f)
            self.data['sample_rate'] = read_double_be(f)
            self.data['channels'] = read_u32be(f)
            self.data['sample_byte_size'] = read_u32be(f)
            self.data['flags'] == read_u32be(f)

            elf.data['bytes_per_frame']   = read_u32be(f)
            elf.data['samples_per_frame'] = read_u32be(f)

            raise Exception()

        left = self.size - (f.tell() - start)
        if left > 0:
            remaining = f.read(left)
            atom = Atom()
            atom.size = left
            read_default(io.BytesIO(remaining), atom)
            self.children.extend(atom.children)


for tag in sound_tags:
    MOV_CLASSES[tag] = SoundSampleDescriptor

@register_mov_class
class SampleToChunk(Root):
    class_id = b'stsc'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        entry_count = read_u32be(f)
        entries = []
        for i in range(entry_count):
            entries.append([read_u32be(f), read_u32be(f) ,read_u32be(f)])

        self.data['entries'] = entries

@register_mov_class
class SampleSizes(Root):
    class_id = b'stsz'

    def read(self, f):
        start = f.tell()
        version = read_u8(f)
        flags = f.read(3)
        sample_size =  read_u32be(f)
        self.data['sample_size'] = sample_size

        sample_count = read_u32be(f)
        entries = []

        self.data['sample_count'] = sample_count
        if sample_size > 0:
            return

        for i in range(sample_count):
            v = read_u32be(f)
            # print(v, f.tell())
            entries.append(v)
        self.data['entries'] = entries

@register_mov_class
class SampleChunkOffset32(Root):
    class_id = b'stco'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        entry_count = read_u32be(f)
        entries = []
        for i in range(entry_count):
            entries.append(read_u32be(f))

        self.data['entries'] = entries

@register_mov_class
class SampleChunkOffset64(Root):
    class_id = b'co64'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        entry_count = read_u32be(f)
        entries = []
        for i in range(entry_count):
            entries.append(read_u64be(f))

        self.data['entries'] = entries

@register_mov_class
class TimeToSample(Root):
    class_id = b'stts'

    def read(self, f):
        version = read_u8(f)
        flags = f.read(3)

        entry_count = read_u32be(f)
        entries = []
        for i in range(entry_count):
            sample_count = read_u32be(f)
            sample_duration =  read_u32be(f)
            entries.append([sample_count, sample_duration])
        self.data['entries'] = entries

@register_mov_class
class Timecode(Root):
    class_id = b'tmcd'

    def read(self, f):
        start = f.tell()
        self.data['index'] = read_sample_descriptor_header(f)
        # reserved
        r = read_s32be(f)
        print('reserved:', r)

        flags = read_u32be(f)
        print("flags 0x%04x" % flags)
        num = read_u32be(f)
        den = read_u32be(f)
        self.data['rate'] = [num, den]
        fps = read_u8(f)
        self.data['fps'] = fps
        # reserved
        f.read(1)

        # read reel name
        if self.size - (f.tell() - start) > 8:
            size = read_s32be(f)
            if size > 0:
                user_type = f.read(4)
                if user_type == b'name':
                    str_size = read_s16be(f)
                    if str_size > 0:
                        langcode = read_s16be(f)
                        reel_name = f.read(str_size)
                        assert len(reel_name) == str_size
                        self.data['reel_name'] = reel_name.decode('utf8')

def read_default(f, atom):

    total_size = 0

    while total_size <= atom.size - 8:
        a = Atom()
        a.size = atom.size
        if atom.size >= 8:
            a.pos = f.tell()
            try:
                #TODO: do somthing better then this
                a.size = read_s32be(f)
            except:
                break
            a.class_id = f.read(4)
            # print(a.class_id)
            total_size += 8

            # 64 bit extended size
            if a.size == 1:
                a.size = read_s64be(f) - 8
                total_size += 8

        a.size -= 8;
        if a.size < 0:
            break

        classobj = MOV_CLASSES.get(a.class_id, None)
        if classobj:
            start = f.tell()
            a = classobj(f, a)
            a.read(f)
            left = a.size - f.tell() + start
            if left > 0:
                print("underread", left, a)
                f.seek(left, os.SEEK_CUR)
            elif left < 0:
                print("overread", left, a)
                f.seek(left, os.SEEK_CUR)

        else:
            f.seek(a.size, os.SEEK_CUR)

        total_size += a.size
        atom.children.append(a)


class MOVFile(object):
    def __init__(self, path):

        self.root = Root()
        self.root.size = INT64_MAX
        self.root.type = b'root'
        with io.open(path, 'rb') as f:
            read_default(f, self.root)

    @property
    def content(self):
        for item in self.root.children:
            if isinstance(item, Mov):
                return item

    @property
    def tracks(self):
        for item in self.content.tracks:
            yield item

    def dump(self):
        self.root.dump()
