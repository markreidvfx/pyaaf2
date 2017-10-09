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

    def createclip(self, slot_id):
        clip = self.root.create.SourceClip()
        clip.mob = self
        clip.slot_id = slot_id
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

    def create_essence(self, slot_id, media_kind, codec, edit_rate, sample_rate):
        datadef = self.root.dictionary.lookup_datadef(media_kind)
        slot = self.root.create.TimelineMobSlot(slot_id, "Track-%03d" % slot_id)
        mob = self.root.create.SourceMob("%s.PHYS" % self.name)

        slot.segment = mob.createclip(0)

        print(slot.segment)
        print(mob)

    def import_dnxhd_essence(self, path, frame_rate):
        slot = 1
        essence = self.create_essence(slot, 'picture', 'DNxHD', frame_rate, frame_rate)

@register_class
class SourceMob(Mob):
    class_id = UUID("0d010101-0101-3700-060e-2b3402060101")
