from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
from datetime import datetime

from . import core
from . mobid import MobID
from . utils import register_class

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

    def create_essence(self, media_kind, edit_rate, slot_id=None):
        if not slot_id:
            slot_id = max([s.id for s in self.slots] or [0]) + 1

        source_mob = self.root.create.SourceMob("%s.PHYS" % self.name)
        self.root.content.add_mob(source_mob)
        null_slot = source_mob.add_null_slot(media_kind=media_kind, edit_rate=edit_rate)

        slot = self.root.create.TimelineMobSlot(slot_id)
        slot.segment = source_mob.createclip(null_slot.id, media_kind)
        self.slots.append(slot)

        essencedata = self.root.create.EssenceData()
        essencedata.id = source_mob.id
        self.root.content.add_essencedata(essencedata)

        return source_mob, essencedata

    def import_dnxhd_essence(self, path, frame_rate):
        source_mob, essencedata = self.create_essence('picture', frame_rate)
        sample_rate = frame_rate

        descriptor = self.root.create.CDCIDescriptor()
        source_mob.descriptor = descriptor
        descriptor['ComponentWidth'].value = 8
        descriptor['ImageAspectRatio'].value = str('16/9')
        descriptor['HorizontalSubsampling'].value = 2
        descriptor['StoredWidth'].value = 1920
        descriptor['StoredHeight'].value = 1080
        descriptor['SampleRate'].value = sample_rate
        descriptor['Length'].value = 0
        descriptor['FrameLayout'].value = "FullFrame"
        descriptor['VideoLineMap'].value = [42, 0] #???

        f = open(path, 'rb')
        stream = essencedata.open('w')
        read_size = self.root.cfb.sector_size * 2
        while True:
            data = f.read(read_size)
            if data:
                stream.write(data)
            else:
                break

@register_class
class SourceMob(Mob):
    class_id = UUID("0d010101-0101-3700-060e-2b3402060101")

    @property
    def descriptor(self):
        return self['EssenceDescription'].value
    @descriptor.setter
    def descriptor(self, value):
        self['EssenceDescription'].value = value

    def add_null_slot(self, media_kind='picture', edit_rate=None, slot_id=None):
        if not slot_id:
            slot_id = max([s.id for s in self.slots] or [0]) + 1

        slot = self.root.create.TimelineMobSlot(slot_id, edit_rate=edit_rate)
        self.slots.append(slot)

        clip = self.createclip(slot_id, media_kind)
        slot.segment = clip

        return slot
