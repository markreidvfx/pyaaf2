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
from . utils import register_class
from . import video

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
    def slots(self):
        return self['Slots']

    def slot_at(self, slot_id):
        for slot in self.slots:
            if slot.id == slot_id:
                return slot
        raise IndexError("No SlotID: %s" % str(slot_id))

    def _next_slot_id(self):
        slots = [slot.id for slot in self.slots]
        slots.sort()
        start = 1
        if slots and slots[0] == 0:
            start = 0

        for i, e in enumerate(slots + [None], start):
            if i != e:
                return i

    def createclip(self, slot_id=None, media_kind=None):
        clip = self.root.create.SourceClip(media_kind=media_kind)
        clip.mob = self
        clip.slot = self.slot_at(slot_id)
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

    def embbed_dnxhd_essence(self, path, edit_rate):
        sample_rate = edit_rate

        # create sourceMob and essencedata
        source_mob = self.root.create.SourceMob("%s.PHYS" % self.name)
        self.root.content.mobs.append(source_mob)
        essencedata, source_slot = source_mob.create_essence(edit_rate, 'picture')

        # create slot and clip that references source_mob slot
        slot_id = self._next_slot_id()
        slot = self.root.create.TimelineMobSlot(slot_id, edit_rate=edit_rate)
        slot.segment = source_mob.createclip(source_slot.id, 'picture')
        self.slots.append(slot)

        # create essence descriptor
        descriptor = self.root.create.CDCIDescriptor()
        source_mob.descriptor = descriptor

        descriptor['SampleRate'].value = sample_rate
        descriptor['VideoLineMap'].value = [42, 0] # ???

        descriptor['ContainerFormat'].value = self.root.dictionary.lookup_containerdef("AAF")
        dnxhd_codec_uuid = UUID("8ef593f6-9521-4344-9ede-b84e8cfdc7da")
        descriptor['CodecDefinition'].value = self.root.dictionary.lookup_codecdef(dnxhd_codec_uuid)

        # open essence stream
        stream = essencedata.open('w')

        # open input file
        f = io.open(path, 'rb')

        cid = None
        for i, packet in enumerate(video.iter_dnx_stream(f)):
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
        source_slot.segment.length = i

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
        if slot_id is None:
            slot_id = self._next_slot_id()
        # NOTE: not sure if SourceMob can only contain 1 essence
        assert slot_id == 1
        slot = self.create_null_slot(edit_rate=edit_rate, media_kind=media_kind, slot_id=slot_id)
        essencedata = self.root.create.EssenceData()
        essencedata.id = self.id
        self.root.content.essencedata.append(essencedata)
        return essencedata, slot

    def create_null_slot(self, edit_rate=None, media_kind='picture', slot_id=None):
        if slot_id is None:
            slot_id = self._next_slot_id()

        slot = self.root.create.TimelineMobSlot(slot_id, edit_rate=edit_rate)
        self.slots.append(slot)

        clip = self.root.create.SourceClip(media_kind=media_kind)
        slot.segment = clip

        return slot
