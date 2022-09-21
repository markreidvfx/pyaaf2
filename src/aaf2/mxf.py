from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import sys
import struct
import datetime

from io import BytesIO
import io

from .utils import (read_u8, read_u16be,
                   read_u32be, read_s32be,
                   read_u64be, read_s64be,
                   int_from_bytes)
from .mobid import MobID
from .model import datadefs
from .auid import AUID

MXF_CLASSES = {}

def register_mxf_class(classobj):
    MXF_CLASSES[classobj.class_id] = classobj
    return classobj


class MXFRef(AUID):
    pass

class MXFRefArray(list):
    pass

def read_auid_be(f):
    data = f.read(16)
    if data:
        return AUID(bytes_be=data)

def read_strongref(f):
    data = f.read(16)
    if data:
        return MXFRef(bytes_be=data)


def decode_strong_ref_array(f):

    count = read_u32be(f)
    f.read(4)
    refs = MXFRefArray()
    for i in range(count):
        refs.append(read_strongref(f))
    return refs


def decode_utf16be(data):
    return data.decode('utf-16be').split(u'\x00')[0]

def decode_auid(data):
    return AUID(bytes_be=data)

def reverse_auid(data):
    new = data.hex[16:] + data.hex[:16]
    return AUID(new)

def decode_datadef(data):
    orig = AUID(bytes_be=data)
    datadef = reverse_auid(orig)
    name = datadefs.DataDefs.get(str(datadef), (None, None))[0]
    return name

def decode_strongref(data):
    return MXFRef(bytes_be=data)

def decode_indirect_value(data):
    data = bytearray(data)
    typedef = reverse_auid(decode_auid(data[:16]))
    if typedef == AUID("00060e2b-3401-0401-4c00-021001000000"):
        assert data[16] == 0x01 # byte order?
        return data[17:].decode('utf-16le').rstrip('\x00')
    elif typedef == AUID("00060e2b-3401-0401-4201-100200000000"):
        assert data[16] == 0x01# byte order?
        return data[17:].decode('utf-16be').rstrip('\x00')
    elif typedef == AUID("00060e2b-3401-0401-4c00-070101000000"):
        assert data[16] == 0x01# byte order?
        return struct.unpack(b"<i", data[17:])[0]
    else:
        # unhandled indirect type
        return

def decode_rational(f):
    num = read_u32be(f)
    den = read_u32be(f)

    return "%d/%d" % (num, den)

def decode_video_line_map(f):
    count = read_u32be(f)
    size = read_u32be(f)
    line_map = []
    if size == 4:
        if count > 0:
            line_map.append(read_s32be(f))
        else:
            line_map.append(0)
        if count > 1:
            line_map.append(read_s32be(f))
        else:
            line_map.append(0)
    return line_map

def decode_pixel_layout(f):
    layout = []
    for i in range(8):
        code = read_u8(f)
        depth = read_u8(f)
        if not code:
            break
        layout.append({'Code':code, 'Size':depth})
    return layout

def decode_timestamp(f):
    t = read_u64be(f)

    year = t >> 48
    month = t >> 40 & 0xFF
    day = t >> 32 & 0xFF
    hour = t >> 24 & 0xFF
    minute = t >> 16 & 0xFF
    sec = t >> 8  & 0xFF
    try:
        d = datetime.datetime(year, month, day, hour, minute, sec)
        return d
    except:
        return datetime.datetime.now()


def decode_mob_id(data):
    uid1 = AUID(bytes_be=data[:16])
    uid2 =  AUID(bytes_be=data[16:])
    m = MobID(str(uid1) + str(uid2))
    return m

def ama_path(path):
    prefix ="file://"
    return prefix + path

class MXFObject(object):
    def __init__(self):
        self.instance_id = None
        self.data = {}
        self.root = None

    def create_aaf_instance():
        pass

    def read_tag(self, tag, data):
        if tag == 0x3c0a:
            self.instance_id = decode_auid(data)

    def read_properties(self, f, length, local_tags):
        for tag, data in iter_tags(f, length):
            self.read_tag(tag, data)
            uid = local_tags.get(tag, None)
            with BytesIO(data) as f:

                if uid == AUID("a0240060-94eb-75cb-ce2a-ca5051ab11d3"):
                    self.data['FrameSampleSize'] = read_s32be(f)
                elif uid == AUID("a0240060-94eb-75cb-ce2a-ca4d51ab11d3"):
                    self.data['ResolutionID'] = read_s32be(f)
                elif uid == AUID("a0220060-94eb-75cb-96c4-69924f6211d3"):
                    self.data['AppCode'] = read_s32be(f)
                elif uid == AUID("060e2b34-0101-0109-0601-010406100000"):
                    self.data['SubDescriptors'] = decode_strong_ref_array(f)
                elif uid == AUID("a01c0004-ac96-9f50-6095-818347b111d4"):
                    self.data["MobAttributeList"] = decode_strong_ref_array(f)
                elif uid == AUID("a01c0004-ac96-9f50-6095-818547b111d4"):
                    self.data["TaggedValueAttributeList"] = decode_strong_ref_array(f)

    def resolve_ref(self, key):
        ref = self.data.get(key, None)
        if ref:
            obj = self.root.resolve(ref)
            if obj:
                return obj
        raise Exception("unable to resolve: %s %s %s" % (key,auid_to_str_list(ref, sep=' '), str(ref)) )

    def iter_strong_refs(self, key):
        for ref in self.data.get(key, []):
            # print(ref, auid_to_str_list(ref, sep=' '))
            yield self.root.resolve(ref)


    def __repr__(self):
        return str(self.data)

@register_mxf_class
class MXFPreface(MXFObject):
    class_id = AUID("060e2b34-0253-0101-0d01-010101012f00")
    def read_tag(self, tag, data):
        super(MXFPreface, self).read_tag(tag, data)

        if tag == 0x3b09:
            self.data['OperationalPattern'] = decode_auid(data)
        elif tag == 0x3b03:
            self.data['ContentStorage'] = decode_strongref(data)

@register_mxf_class
class MXFContentStorage(MXFObject):
    class_id = AUID("060e2b34-0253-0101-0d01-010101011800")
    def read_tag(self, tag, data):
        super(MXFContentStorage, self).read_tag(tag, data)
        with BytesIO(data) as f:
            if tag == 0x1902:
                self.data['EssenceContainerData'] = decode_strong_ref_array(f)
            elif tag == 0x1901:
                self.data['Packages'] = decode_strong_ref_array(f)


class MXFPackage(MXFObject):

    def read_tag(self, tag, data):
        super(MXFPackage, self).read_tag(tag, data)

        with BytesIO(data) as f:

            if tag == 0x4403:
                self.data['Slots'] = decode_strong_ref_array(f)
            elif tag == 0x4401:
                self.data['MobID'] = decode_mob_id(data)
            elif tag == 0x4402:
                self.data['Name'] = decode_utf16be(data)
            elif tag == 0x4701:
                self.data['Descriptor'] = decode_strongref(data)
            elif tag == 0x4404:
                self.data['LastModified'] = decode_timestamp(f)
            elif tag == 0x4405:
                self.data['CreationTime'] = decode_timestamp(f)
            elif tag == 0x4408:
                self.data['UsageCode'] = decode_auid(data) # doesn't appear reversed...
            elif tag == 0x4406:
                self.data['UserComments'] = decode_strong_ref_array(f)

    @property
    def mob_id(self):
        return self.data.get('MobID', None)

    def link(self):
        mob = self.create_aaf_instance()

        mob.mob_id = self.mob_id
        self.root.aaf.content.mobs.append(mob)

        name = self.data.get('Name', None)
        if name:
            mob.name = name

        for track in self.iter_strong_refs("Slots"):
            # print(type(track), track)

            if isinstance(track, (MXFStaticTrack, MXFEventTrack)):
                continue

            timeline = track.link()
            mob.slots.append(timeline)

        for key in ('LastModified', 'CreationTime', 'UsageCode', 'AppCode'):
            if key in self.data:
                mob[key].value = self.data[key]

        for item in self.iter_strong_refs('UserComments'):
            tag = item.link()
            if tag:
                mob['UserComments'].append(tag)

        for item in self.iter_strong_refs('MobAttributeList'):
            tag = item.link()
            if tag:
                mob['MobAttributeList'].append(tag)

        if 'Descriptor' in self.data:
            d = self.resolve_ref('Descriptor')
            mob.descriptor = d.link()

        return mob

@register_mxf_class
class MXFMaterialPackage(MXFPackage):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013600")
    def create_aaf_instance(self):
        return self.root.aaf.create.MasterMob()

@register_mxf_class
class MXFSourcePackage(MXFPackage):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013700")
    def create_aaf_instance(self):
        return self.root.aaf.create.SourceMob()

@register_mxf_class
class MXFTrack(MXFObject):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013b00")

    def create_aaf_instance(self):
        return self.root.aaf.create.TimelineMobSlot()

    def read_tag(self, tag, data):
        super(MXFTrack, self).read_tag(tag, data)
        with BytesIO(data) as f:
            if tag == 0x4b02:
                self.data['Origin'] = read_s64be(f)
            elif tag == 0x4b01:
                self.data['EditRate'] = decode_rational(f)
            elif tag == 0x4803:
                self.data['Segment'] = decode_strongref(data)
            elif tag == 0x4804:
                self.data['PhysicalTrackNumber'] = read_u32be(f)
            elif tag == 0x4801:
                self.data['SlotID'] = read_u32be(f)
            elif tag == 0x4802:
                self.data['SlotName'] = decode_utf16be(data)

    def link(self):
        timeline = self.create_aaf_instance()

        for key in ('SlotID', 'SlotName', 'EditRate', 'PhysicalTrackNumber', 'Origin'):
            if key in self.data:
                timeline[key].value = self.data[key]

        segment = self.resolve_ref('Segment')
        timeline.segment = segment.link()
        return timeline

@register_mxf_class
class MXFStaticTrack(MXFTrack):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013a00")

    def create_aaf_instance(self):
        return self.root.aaf.create.StaticMobSlot()

@register_mxf_class
class MXFEventTrack(MXFTrack):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013900")

    def create_aaf_instance(self):
        return self.root.aaf.create.EventMobSlot()

class MXFComponent(MXFObject):
    def read_tag(self, tag, data):
        super(MXFComponent, self).read_tag(tag, data)
        with BytesIO(data) as f:
            if tag == 0x1001:
                self.data['Components'] = decode_strong_ref_array(f)
            elif tag == 0x1201:
                self.data['StartTime'] = read_u64be(f)
            elif tag == 0x1102:
                self.data['SourceMobSlotID'] = read_u32be(f)
            elif tag == 0x1101:
                self.data['SourceID'] = decode_mob_id(data)
            elif tag == 0x0202:
                self.data['Length'] = read_u64be(f)
            elif tag == 0x0201:
                self.data['DataDef'] = decode_datadef(data)
            elif tag == 0x1503:
                self.data['Drop'] = read_u8(f) == 1
            elif tag == 0x1502:
                self.data['FPS'] = read_u16be(f)
            elif tag == 0x1501:
                self.data['Start'] = read_u64be(f)
            elif tag == 0x0501:
                self.data['Choices'] = decode_strong_ref_array(f)
            elif tag == 0x0502:
                self.data['StillFrame'] = decode_strongref(data)
            elif tag == 0x0d01:
                self.data['InputSegment'] = decode_strongref(data)
            elif tag == 0x0d02:
                self.data['PulldownKind'] = read_u8(f)
            elif tag == 0x0d03:
                self.data['PulldownDirection'] = read_u8(f)
            elif tag == 0x0d04:
                self.data['PhaseFrame'] = read_s32be(f)
            elif tag == 0x0e01:
                self.data['RelativeScope'] = read_s32be(f)
            elif tag == 0x0e02:
                self.data['RelativeSlot'] = read_s32be(f)

@register_mxf_class
class MXFSequence(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101010f00")

    def create_aaf_instance(self):
        return self.root.aaf.create.Sequence()

    def link(self):
        s = self.create_aaf_instance()

        s.media_kind = self.data['DataDef'] #or 'DataDef_Unknown'
        s.length = self.data.get('Length', 0)
        # for item in self.data['Components']:
        #     print(auid_to_str_list(item, sep=' '), item)
        for item in self.iter_strong_refs('Components'):
            s['Components'].append(item.link())
        return s

@register_mxf_class
class MXFSourceClip(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101011100")

    def create_aaf_instance(self):
        return self.root.aaf.create.SourceClip()

    def link(self):
        s = self.create_aaf_instance()
        s.media_kind = self.data['DataDef'] or 'DataDef_Unknown'
        for key in ('SourceID', 'SourceMobSlotID', 'StartTime', 'Length'):
            s[key].value = self.data.get(key, None)
        return s

@register_mxf_class
class MXFTimecode(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101011400")

    def create_aaf_instance(self):
        return self.root.aaf.create.Timecode()

    def link(self):

        s = self.create_aaf_instance()
        for key in ('FPS', 'Drop', 'Start'):
            s[key].value = self.data[key]

        s.media_kind = self.data['DataDef']
        s.length = self.data['Length']

        return s

@register_mxf_class
class MXFPulldown(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101010c00")

    def create_aaf_instance(self):
        return self.root.aaf.create.Pulldown()

    def link(self):

        p = self.create_aaf_instance()
        p.media_kind = self.data['DataDef']
        p.length = self.data['Length']

        p['InputSegment'].value = self.resolve_ref('InputSegment').link()

        for key in ('PhaseFrame', 'PulldownDirection', 'PulldownKind'):
            p[key].value = self.data[key]
        return p

@register_mxf_class
class MXFFiller(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101010900")

    def create_aaf_instance(self):
        return self.root.aaf.create.Filler()

    def link(self):
        c = self.create_aaf_instance()
        c.media_kind = self.data['DataDef']
        c.length = self.data['Length']
        return c

@register_mxf_class
class MXFScopeReference(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101010d00")

    def create_aaf_instance(self):
        return self.root.aaf.create.ScopeReference()

    def link(self):
        c = self.create_aaf_instance()
        c.media_kind = self.data['DataDef']
        c.length = self.data['Length']
        for key in ('RelativeSlot', 'RelativeScope'):
            c[key].value = self.data[key]

        return c

@register_mxf_class
class MXFEssenceGroup(MXFComponent):
    class_id = AUID("060e2b34-0253-0101-0d01-010101010500")

    def create_aaf_instance(self):
        return self.root.aaf.create.EssenceGroup()

    def link(self):

        e = self.create_aaf_instance()
        e.media_kind = self.data['DataDef']
        e.length = self.data['Length']
        e['Choices'].value = [item.link() for item in self.iter_strong_refs('Choices')]

        return e

class MXFDescriptor(MXFObject):

    def read_tag(self, tag, data):
        super(MXFDescriptor, self).read_tag(tag, data)
        with BytesIO(data) as f:
            if tag == 0x3f01:
                self.data['FileDescriptors'] = decode_strong_ref_array(f)
            elif tag == 0x3004:
                self.data['ContainerFormat'] = reverse_auid(decode_auid(data))
            elif tag == 0x3005:
                self.data['CodecDefinition'] = reverse_auid(decode_auid(data))
            elif tag == 0x3006:
                self.data['LinkedSlotID'] = read_u32be(f)
            elif tag == 0x3203:
                self.data['StoredWidth'] = read_u32be(f)
            elif tag == 0x3202:
                self.data['StoredHeight'] = read_u32be(f)
            elif tag == 0x3208: #this is display
                self.data['SampledHeight'] = read_u32be(f)
            elif tag == 0x3209: #this is display
                self.data['SampledWidth'] = read_u32be(f)
            elif tag == 0x320d:
                self.data['VideoLineMap'] = decode_video_line_map(f)
            elif tag == 0x3211:
                self.data['ImageAlignmentOffset'] = read_u32be(f)
            elif tag == 0x3002:
                self.data['Length'] = read_s64be(f)
            elif tag == 0x3001:
                self.data['SampleRate'] = decode_rational(f)
            elif tag == 0x3d03:
                self.data['AudioSamplingRate'] = decode_rational(f)
            elif tag == 0x3d0a:
                self.data['BlockAlign'] = read_u16be(f)
            elif tag == 0x3d01:
                self.data['QuantizationBits'] = read_u32be(f)
            elif tag == 0x3d07:
                self.data['Channels'] = read_u32be(f)
            elif tag == 0x3d09:
                self.data['AverageBPS'] = read_u32be(f)
            elif tag == 0x3d02:
                self.data['Locked'] = read_u8(f) == 1
            elif tag == 0x3301:
                self.data['ComponentWidth'] = read_u32be(f)
            elif tag == 0x320c:
                self.data['FrameLayout'] = read_u8(f)
            elif tag == 0x320e:
                self.data['ImageAspectRatio'] = decode_rational(f)
            elif tag == 0x3d06:
                self.data['SoundCompression'] =  reverse_auid(decode_auid(data))
            elif tag == 0x3201:
                self.data['Compression'] = reverse_auid(decode_auid(data))
            elif tag == 0x3302:
                self.data['HorizontalSubsampling'] = read_u32be(f)
            elif tag == 0x3308:
                self.data['VerticalSubsampling'] = read_u32be(f)
            elif tag == 0x2f01:
                self.data['Locator'] = decode_strong_ref_array(f)
            elif tag == 0x3401:
                self.data['PixelLayout'] = decode_pixel_layout(f)

@register_mxf_class
class MXFMultipleDescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101014400")

    def create_aaf_instance(self):
        return self.root.aaf.create.MultipleDescriptor()

    def link(self):
        d = self.create_aaf_instance()
        for item in self.iter_strong_refs("FileDescriptors"):
            # if isinstance(item, MXFAES3AudioDescriptor):
            #     continue
            d['FileDescriptors'].append(item.link())
        d['Length'].value = self.data.get('Length', 0)

        n = self.root.aaf.create.NetworkLocator()
        n['URLString'].value = ama_path(self.root.path)
        d['Locator'].append(n)

        d['SampleRate'].value = self.data['SampleRate']

        if self.root.ama:
            n = self.root.aaf.create.NetworkLocator()
            n['URLString'].value = ama_path(self.root.path)
            d['Locator'].append(n)
            d['MediaContainerGUID'].value = AUID("60eb8921-2a02-4406-891c-d9b6a6ae0645")

        return d

@register_mxf_class
class MXFCDCIDescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101012800")

    def create_aaf_instance(self):
        return self.root.aaf.create.CDCIDescriptor()

    def link(self):
        d = self.create_aaf_instance()

        # required
        for key in ('ComponentWidth', 'HorizontalSubsampling', 'ImageAspectRatio',
           'StoredWidth', 'VideoLineMap', 'StoredHeight', 'SampleRate', 'FrameLayout'):
           d[key].value = self.data[key]

        d['Length'].value = self.data.get('Length', 0)

        # optional
        for key in ('FrameSampleSize', 'ResolutionID', 'Compression', 'VerticalSubsampling',
                    'SampledWidth', 'SampledHeight', 'LinkedSlotID'):
            if key in self.data:
                d[key].value = self.data[key]

        for item in self.iter_strong_refs("Locator"):
            d['Locator'].append(item.link())
            n = self.root.aaf.create.NetworkLocator()
            n['URLString'].value = ama_path(self.root.path)
            d['Locator'].append(n)

        d['ContainerFormat'].value = self.root.aaf.dictionary.lookup_containerdef("AAFKLV")
        if self.root.ama:
            n = self.root.aaf.create.NetworkLocator()
            n['URLString'].value = ama_path(self.root.path)
            d['Locator'].append(n)
            d['MediaContainerGUID'].value = AUID("60eb8921-2a02-4406-891c-d9b6a6ae0645")

        return d

@register_mxf_class
class MXFRGBADescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101012900")

    def create_aaf_instance(self):
        return self.root.aaf.create.RGBADescriptor()

    def link(self):
        d = self.create_aaf_instance()

        for key in ('ImageAspectRatio', 'StoredWidth', 'FrameLayout', 'PixelLayout',
                    'VideoLineMap', 'StoredHeight', 'SampleRate', ):
            d[key].value = self.data[key]

        d['Length'].value = self.data.get('Length', 0)

        # optional
        for key in ('FrameSampleSize','SampledWidth', 'SampledHeight', 'Compression', 'LinkedSlotID'):
            if key in self.data:
                d[key].value = self.data[key]

        d['ContainerFormat'].value = self.root.aaf.dictionary.lookup_containerdef("AAFKLV")
        n = self.root.aaf.create.NetworkLocator()
        n['URLString'].value = ama_path(self.root.path)
        d['Locator'].append(n)
        if self.root.ama:
            n = self.root.aaf.create.NetworkLocator()
            n['URLString'].value = ama_path(self.root.path)
            d['Locator'].append(n)
            d['MediaContainerGUID'].value = AUID("60eb8921-2a02-4406-891c-d9b6a6ae0645")


        return d

@register_mxf_class
class MXFANCDataDescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101015c00")

    def create_aaf_instance(self):
        return self.root.aaf.create.ANCDataDescriptor()

    def link(self):
        d = self.create_aaf_instance()
        for key in ('SampleRate', ):
            d[key].value = self.data[key]

        d['Length'].value = self.data.get('Length', 0)

        # optional
        for key in ('LinkedSlotID', ):
            if key in self.data:
                d[key].value = self.data[key]

        return d

@register_mxf_class
class MXFMPEG2VideoDescriptor(MXFCDCIDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101015100")

    def link(self):
        # 060e2b34.04010103.04010202.01040300
        self.data['ResolutionID'] = 4076 #XDCAM HD 50Mbit

        d['Length'].value = self.data.get('Length', 0)

        # optional
        for key in ('LinkedSlotID', ):
            if key in self.data:
                d[key].value = self.data[key]

        return super(MXFMPEG2VideoDescriptor, self).link()

@register_mxf_class
class MXFPCMDescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101014800")

    def create_aaf_instance(self):
        return self.root.aaf.create.PCMDescriptor()

    def link(self):
        d = self.create_aaf_instance()
        # required
        for key in ('BlockAlign', 'AverageBPS', 'Channels',
            'QuantizationBits', 'AudioSamplingRate', 'SampleRate'):
            d[key].value = self.data[key]

        d['Length'].value = self.data.get('Length', 0)

        # optional
        for key in ('LinkedSlotID', ):
            if key in self.data:
                d[key].value = self.data[key]

        n = self.root.aaf.create.NetworkLocator()
        n['URLString'].value = ama_path(self.root.path)
        d['Locator'].append(n)
        if self.root.ama:
            n =  self.root.aaf.create.NetworkLocator()
            n['URLString'].value = ama_path(self.root.path)
            d['Locator'].append(n)
            d['MediaContainerGUID'].value = AUID("60eb8921-2a02-4406-891c-d9b6a6ae0645")

        return d

@register_mxf_class
class MXFAES3AudioDescriptor(MXFPCMDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101014700")

@register_mxf_class
class MXFSoundDescriptor(MXFPCMDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101014200")

@register_mxf_class
class MXFImportDescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101014a00")

    def create_aaf_instance(self):
        return self.root.aaf.create.ImportDescriptor()

    def link(self):
        d = self.create_aaf_instance()
        n = self.root.aaf.create.NetworkLocator()
        n['URLString'].value = ama_path(self.root.path)
        d['Locator'].append(n)

        return d

@register_mxf_class
class MXFTapeDescriptor(MXFDescriptor):
    class_id = AUID("060e2b34-0253-0101-0d01-010101012e00")

    def create_aaf_instance(self):
        return self.root.aaf.create.TapeDescriptor()

    def link(self):
        return self.create_aaf_instance()

class MXFLocator(MXFObject):

    def read_tag(self, tag, data):
        super(MXFLocator, self).read_tag(tag, data)

        if tag == 0x4001:
            self.data['URLString'] =  decode_utf16be(data)

@register_mxf_class
class MXFNetworkLocator(MXFLocator):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013200")

    def create_aaf_instance(self):
        return self.root.aaf.create.NetworkLocator()

    def link(self):
        n = self.create_aaf_instance()
        n['URLString'].value = self.data['URLString']
        return n

@register_mxf_class
class MXFEssenceData(MXFObject):
    class_id = AUID("060e2b34-0253-0101-0d01-010101012300")
    def read_tag(self, tag, data):
        super(MXFEssenceData, self).read_tag(tag, data)

        if tag == 0x2701:
            self.data['MobID'] = decode_mob_id(data)

@register_mxf_class
class MXFTaggedValue(MXFObject):
    class_id = AUID("060e2b34-0253-0101-0d01-010101013f00")

    def create_aaf_instance(self):
        return self.root.aaf.create.TaggedValue()

    def read_tag(self, tag, data):
        super(MXFTaggedValue, self).read_tag(tag, data)

        if tag == 0x5001:
            self.data['Name'] = decode_utf16be(data)
        elif tag == 0x5003:
            self.data['Value'] = decode_indirect_value(data)

    def link(self):
        v = self.data.get("Value", None)
        if v is None:
            return

        tag = self.create_aaf_instance()
        tag.name = self.data["Name"]
        tag.value = v

        for item in self.iter_strong_refs('TaggedValueAttributeList'):
            attr = item.link()
            if attr:
                tag['TaggedValueAttributeList'].append(attr)

        return tag

def ber_length(f):
    length = read_u8(f)
    if length > 127:
        data = bytearray(length - 128)
        bytes_read = f.readinto(data)
        assert bytes_read == len(data)
        length = int_from_bytes(data, byte_order='big')
    return length


def iter_kl(f):
    pos = f.tell()
    while True:
        # read the key
        f.seek(pos)
        key = read_auid_be(f)
        if not key:
            break
        # read the ber_length
        length = ber_length(f)

        pos = f.tell() + length
        yield key, length

def iter_tags(f, length):
    while length > 0:
        tag = read_u16be(f)
        size = read_u16be(f)
        # print("   tag 0x%04x %d" % (tag, size))
        if size:
            yield tag, f.read(size)
        length -= 4 + size

def auid_to_str_list(v, sep=',', prefix=""):
    return sep.join('%s%02x' % (prefix, i)  for i in bytearray(v.bytes_be))

class MXFFile(object):

    def __init__(self, path):
        self.objects = {}
        self.local_tags = {}
        self.preface = None
        self.header_operation_pattern = None
        self.header_partition_size = None
        self.path = path
        self.ama = False
        self.aaf = None
        with io.open(path, 'rb') as f:

            for key, length in iter_kl(f):

                # only read until the first body partition
                if not self.header_partition_size is None and f.tell() > self.header_partition_size:
                    break

                if key == AUID("060e2b34-0205-0101-0d01-020101050100"):
                    self.local_tags = self.read_primer(f, length)
                elif key == AUID("060e2b34-0205-0101-0d01-020101020400"):
                    self.read_header(f, length)
                else:
                    # print('{')
                    # print(key,  auid_to_str_list(key, sep='.'))
                    obj = self.read_object(f, key, length)
                    if obj:
                        # print(obj.__class__.__name__, obj.instance_id)
                        obj.root = self
                        self.objects[obj.instance_id] = obj

                    if isinstance(obj, MXFPreface):
                        self.preface = obj
                    # print('}')

    def resolve(self, ref):
        if isinstance(ref, MXFRef):
            return self.objects.get(ref)

    @property
    def content(self):
        return self.preface.resolve_ref("ContentStorage")

    def packages(self):
        if self.content:
            for package in self.content.iter_strong_refs("Packages"):
                yield package

    def material_packages(self):
        for package in self.packages():
            if isinstance(package, MXFMaterialPackage):
                yield package

    def link(self, f):
        self.aaf = f
        mobs = []
        for package in self.packages():
            if package.mob_id in f.content.mobs:
                continue

            mobs.append(package.link())

        return mobs

    def round_to_kag(self, pos, kag_size):
        ret = (pos // kag_size) * kag_size
        if ret == pos:
            return pos
        return pos + kag_size


    def read_header(self, f, length):
        major_version = read_u16be(f)
        minor_version = read_u16be(f)
        kag_size = read_u32be(f)
        this_partion = read_u64be(f)
        prev_partion = read_u64be(f)
        footer_partion = read_u64be(f)
        header_byte_count = read_u64be(f)
        index_byte_count = read_u64be(f)
        index_sid = read_u32be(f)
        body_offset = read_u64be(f)
        body_sid = read_u32be(f)
        self.header_operation_pattern = read_auid_be(f)

        self.header_partition_size = (self.round_to_kag(length, kag_size) +
                                      self.round_to_kag(header_byte_count, kag_size) +
                                      self.round_to_kag(index_byte_count, kag_size))

    def read_primer(self, f, length):

        item_num = read_u32be(f)
        item_len = read_u32be(f)
        if item_len != 18:
            return
        if item_num > 65536:
            return

        tags = {}
        for i in range(item_num):
            tag = read_u16be(f)
            uid = read_auid_be(f)
            # print("%04x" % tag, ':', uid)
            tags[tag] = uid

        return tags

    def read_object(self, f, key, length):

        b = bytearray(key.bytes_be)
        if not b[5] == 0x53:
            return

        obj_class = MXF_CLASSES.get(key, None)
        if obj_class:

            obj = obj_class()
            obj.root = self
            obj.read_properties(f, length, self.local_tags)
            return obj
        else:
            for tag, data in iter_tags(f, length):
                pass

    def dump_flat(self):
        for key,value in self.objects.items():
            print(value.__class__.__name__, key)
            for p, v in value.data.items():
                print("  ",p, v)

    def dump(self, obj=None, space=""):
        if obj is None:
            obj = self.preface

        print (space, obj.__class__.__name__, obj.instance_id)

        space += " "
        for key, value in sorted(obj.data.items()):
            if isinstance(value, MXFRef):
                c = self.objects.get(value, None)
                if c:
                    self.dump(c, space)
                else:
                    print(space, None)

            elif isinstance(value, MXFRefArray):
                print (space, key)
                for item in value:
                    c = self.objects.get(item, None)
                    if c:
                        self.dump(c, space + " ")
                    else:
                        print(space, None)
            else:
                print (space, key, value)

    @property
    def operation_pattern(self):

        if self.header_operation_pattern:
            op = self.header_operation_pattern
        else:
            op = self.preface.data.get('OperationalPattern', None)

        if not op:
            return

        op = bytearray(op.bytes_be)

        prefix1 = bytearray([0x06, 0x0e, 0x2b, 0x34, 0x04, 0x01, 0x01, 0x01, 0x0d, 0x01, 0x02, 0x01])
        prefix2 = bytearray([0x06, 0x0e, 0x2b, 0x34, 0x04, 0x01, 0x01, 0x02, 0x0d, 0x01, 0x02, 0x01])
        prefix3 = bytearray([0x06, 0x0e, 0x2b, 0x34, 0x04, 0x01, 0x01, 0x03, 0x0d, 0x01, 0x02, 0x01])

        prefix_valid = False
        for prefix in (prefix1, prefix2, prefix3):
            if op[:len(prefix)] == prefix:
                prefix_valid = True
                break

        if not prefix_valid:
            return

        complexity = op[12]

        if complexity >= 1 and complexity <= 3:
            package_complexity = op[13]
            letter = {1:'a', 2:'b', 3:'c'}.get(package_complexity, None)
            if letter:
                return 'OP%d%s' % (complexity, letter)

        elif complexity >= 0x10 and complexity <= 0x7f:
            if complexity == 0x10:
                return 'OPAtom'
