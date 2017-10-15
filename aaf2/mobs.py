from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
from datetime import datetime
import io

from . import core
from . mobid import MobID
from . utils import register_class, rescale
from . import essence
from . import video
from . import audio

class TaggedValueHelper(object):
    def __init__(self, poperty_vector):
        self.p = poperty_vector

    def get(self, key, default=None):
        for item in self.p:
            if item['Name'].value == key:
                return item
        return default

    def __contains__(self, key):
        return not self.get(key, None) is None

    def __getitem__(self, key):
        p = self.get(key, None)
        if p:
            return p['Value'].value

        raise IndexError(key)

    def items(self):
        for item in self.p:
            yield item['Name'].value, item["Value"].value

    def __setitem__(self, key, value):
        tag = self.get(key, None)
        if tag is None:
            tag = self.p.parent.root.create.TaggedValue()
            tag['Name'].value = key
            self.p.append(tag)

        tag['Value'].value = value

@register_class
class Mob(core.AAFObject):
    class_id = UUID("0d010101-0101-3400-060e-2b3402060101")

    def __init__(self, name=None):
        self.name = name or "Mob"
        self.id = MobID.new()

        now = datetime.now()
        self['CreationTime'].value = now
        self['LastModified'].value = now

        self['Slots'].value = []

    @property
    def unique_key(self):
        return self.id

    @property
    def name(self):
        return self['Name'].value

    @name.setter
    def name(self, value):
        self['Name'].value = value

    @property
    def id(self):
        return self['MobID'].value

    @id.setter
    def id(self, value):
        self['MobID'].value = value

    @property
    def usage(self):
        return self['UsageCode'].value
    @usage.setter
    def usage(self, value):
        self['UsageCode'].value = value

    @property
    def comments(self):
        return TaggedValueHelper(self['UserComments'])

    @property
    def slots(self):
        return self['Slots']

    def slot_at(self, slot_id):
        for slot in self.slots:
            if slot.id == slot_id:
                return slot
        raise IndexError("No SlotID: %s" % str(slot_id))

    def create_timeline_slot(self, edit_rate, slot_id=None):
        slots = [slot.id for slot in self.slots]
        slots.sort()
        if slot_id is None:
            start = 1
            if slots and slots[0] == 0:
                start = 0

            for i, e in enumerate(slots + [None], start):
                if i != e:
                    slot_id = i
        elif slot_id in slots:
            raise ValueError("slot id: %d already exists" % slot_id)

        slot = self.root.create.TimelineMobSlot(slot_id, edit_rate=edit_rate)
        self.slots.append(slot)
        return slot

    def create_source_clip(self, slot_id=None, start=None, length=None, media_kind=None):
        source_slot = self.slot_at(slot_id)
        if not media_kind:
            media_kind = source_slot.media_kind

        clip = self.root.create.SourceClip(media_kind=media_kind)
        clip.mob = self
        clip.slot = source_slot
        clip.start = start or 0
        clip.length = length or 0
        return clip

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                       self.__class__.__name__)
        s += ' "%s" %s' % (self.name or "", str(self.id))

        return '<%s at 0x%x>' % (s, id(self))

@register_class
class CompositionMob(Mob):
    class_id = UUID("0d010101-0101-3500-060e-2b3402060101")

@register_class
class MasterMob(Mob):
    class_id = UUID("0d010101-0101-3600-060e-2b3402060101")

    def import_dnxhd_essence(self, path, edit_rate, tape=None):

        # create sourceMob and essencedata
        source_mob = self.root.create.SourceMob("%s.PHYS" % self.name)
        self.root.content.mobs.append(source_mob)

        # import the essencedata
        source_slot = source_mob.import_dnxhd_essence(path, edit_rate, tape)

        # create slot and clip that references source_mob slot
        slot = self.create_timeline_slot(edit_rate=edit_rate)
        slot.segment = source_mob.create_source_clip(source_slot.id, media_kind='picture')

        # set clip length
        slot.segment.length = source_slot.segment.length
        return source_mob

    def import_audio_essence(self, path, edit_rate=None, tape=None):

        # create sourceMob and essencedata
        source_mob = self.root.create.SourceMob("%s.PHYS" % self.name)
        self.root.content.mobs.append(source_mob)

        source_slot = source_mob.import_audio_essence(path, edit_rate, tape)

        # create slot and clip that references source_mob slot
        edit_rate = edit_rate or source_slot.edit_rate
        slot = self.create_timeline_slot(edit_rate=edit_rate)
        slot.segment = source_mob.create_source_clip(source_slot.id, media_kind='sound')

        # set clip length
        slot.segment.length = source_slot.segment.length
        return source_mob

@register_class
class SourceMob(Mob):
    class_id = UUID("0d010101-0101-3700-060e-2b3402060101")

    @property
    def descriptor(self):
        return self['EssenceDescription'].value
    @descriptor.setter
    def descriptor(self, value):
        self['EssenceDescription'].value = value

    def create_essence(self, edit_rate=None, media_kind='picture', slot_id=None):
        # NOTE: appears like a SourceMob can only link to 1 essence and it must be slot 1
        slot = self.create_empty_slot(edit_rate=edit_rate, media_kind=media_kind, slot_id=1)
        essencedata = self.root.create.EssenceData()
        essencedata.id = self.id
        self.root.content.essencedata.append(essencedata)
        return essencedata, slot

    def create_empty_slot(self, edit_rate=None, media_kind='picture', slot_id=None):

        slot = self.create_timeline_slot(edit_rate, slot_id)
        clip = self.root.create.SourceClip(media_kind=media_kind)
        slot.segment = clip

        return slot

    def create_timecode_slot(self, edit_rate, timecode_fps, drop_frame=False):
        timecode_slot = self.create_timeline_slot(edit_rate)
        timecode_slot.segment = self.root.create.Timecode(timecode_fps, drop=drop_frame)
        return timecode_slot

    def create_tape_slots(self, tape_name, edit_rate, timecode_fps, drop_frame=False, media_kind=None):
        self.name = tape_name
        self.descriptor = self.root.create.TapeDescriptor()

        slot = self.create_empty_slot(edit_rate, media_kind, slot_id=1)
        slot.segment.length = int(float(edit_rate) * 60 *60 * 12) # 12 hours
        timecode_slot = self.create_timecode_slot(edit_rate, timecode_fps, drop_frame)

        return slot, timecode_slot

    def import_dnxhd_essence(self, path, edit_rate, tape=None):

        essencedata, slot = self.create_essence(edit_rate, 'picture')

        if tape:
            slot.segment = tape

        # create essence descriptor
        descriptor = self.root.create.CDCIDescriptor()
        self.descriptor = descriptor

        # set minimal properties
        descriptor['SampleRate'].value = edit_rate
        descriptor['VideoLineMap'].value = [42, 0] # Not exactly sure what linemap is
        descriptor['ContainerFormat'].value = self.root.dictionary.lookup_containerdef("AAF")
        dnxhd_codec_uuid = UUID("8ef593f6-9521-4344-9ede-b84e8cfdc7da")
        descriptor['CodecDefinition'].value = self.root.dictionary.lookup_codecdef(dnxhd_codec_uuid)

        # open essence stream
        stream = essencedata.open('w')

        # open input file
        with io.open(path, 'rb') as f:

            cid = None
            for i, packet in enumerate(video.iter_dnx_stream(f), 1):
                if cid is None:
                    (cid, width, height, bitdepth, interlaced) = video.read_dnx_frame_header(packet)
                    descriptor['StoredWidth'].value = width
                    descriptor['StoredHeight'].value = height
                    descriptor['ComponentWidth'].value = bitdepth
                    descriptor['FrameLayout'].value = 'SeparateFields' if interlaced else 'FullFrame'
                    descriptor['ImageAspectRatio'].value = "%d/%d" % (width, height)
                    descriptor['FrameSampleSize'].value = len(packet)
                    descriptor['Compression'].value = video.dnx_compression_uuids[cid]
                    descriptor['HorizontalSubsampling'].value = 2

                stream.write(packet)

            # set descriptor and component lengths
            descriptor.length = i
            slot.segment.length = i

        return slot

    def import_audio_essence(self, path, edit_rate=None, tape=None):
        """
        Import audio essence from wav file
        """

        # read the wav file header
        a = audio.WaveReader(path)
        sample_rate = a.getframerate()
        channels = a.getnchannels()
        sample_width = a.getsampwidth()
        block_align = a.getblockalign()
        length = a.getnframes()

        edit_rate = edit_rate or sample_rate

        # create essencedata
        essencedata, slot = self.create_essence(edit_rate, 'sound')
        if tape:
            slot.segment = tape

        # create essence descriptor
        descriptor = self.root.create.PCMDescriptor()
        self.descriptor = descriptor
        descriptor['Channels'].value = channels
        descriptor['BlockAlign'].value = block_align
        descriptor['SampleRate'].value = sample_rate
        descriptor['AverageBPS'].value = sample_rate * channels * sample_width
        descriptor['QuantizationBits'].value = sample_width * 8
        descriptor['AudioSamplingRate'].value = sample_rate

        # set lengths
        descriptor.length = length
        slot.segment.length = int(rescale(length, sample_rate, edit_rate))

        stream = essencedata.open('w')

        while True:
            data = a.readframes(sample_rate)
            if not data:
                break
            stream.write(data)

        return slot

    def export_audio(self, path):
        descriptor = self.descriptor
        assert isinstance(descriptor, essence.PCMDescriptor)

        a = audio.wave.Wave_write(path)
        try:

            channels = descriptor['Channels'].value
            sample_rate = int(float(descriptor['SampleRate'].value))
            sample_size = descriptor['QuantizationBits'].value // 8

            a.setnchannels(channels)
            a.setframerate(sample_rate)
            a.setsampwidth(sample_size)

            read_size = channels * int(float(sample_rate)) * sample_size
            stream = self.essence.open('r')
            while True:
                data = stream.read(read_size)
                if not data:
                    break
                a.writeframesraw(data)

        finally:
            a.close()

    @property
    def essence(self):
        return self.root.content.essencedata.get(self.id, None)
