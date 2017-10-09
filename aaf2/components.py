from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from . import core
from .utils import register_class

class Component(core.AAFObject):
    class_id = UUID("0d010101-0101-0200-060e-2b3402060101")

    @property
    def length(self):
        return self['Length'].value

    @length.setter
    def length(self, value):
        self['Length'].value = value


class Segment(Component):
    class_id = UUID("0d010101-0101-0300-060e-2b3402060101")

@register_class
class Sequence(Segment):
    class_id = UUID("0d010101-0101-0f00-060e-2b3402060101")

@register_class
class NestedScope(Segment):
    class_id = UUID("0d010101-0101-0b00-060e-2b3402060101")

class SourceReference(Segment):
    class_id = UUID("0d010101-0101-1000-060e-2b3402060101")

    @property
    def mob_id(self):
        return self['SourceID'].value

    @mob_id.setter
    def mob_id(self, value):
        self['SourceID'].value = value

    @property
    def slot_id(self):
        return self['SourceMobSlotID'].value

    @slot_id.setter
    def slot_id(self, value):
        self['SourceMobSlotID'].value = value

    @property
    def mob(self):
        mod_id = self.mob_id
        if mod_id is None or mod_id.int == 0:
            return None
        return self.root.content.lookup_mob(mod_id)

    @mob.setter
    def mob(self, value):
        self.mob_id = value.id

    @property
    def slot(self):
        slot_id = self.slot_id
        mob = self.mob
        if mob is None or slot_id is None:
            return
        return mob.slot_at(slot_id)

    @slot.setter
    def slot(self, value):
        self.slot_id = value.id

@register_class
class SourceClip(SourceReference):
    class_id = UUID("0d010101-0101-1100-060e-2b3402060101")

    @property
    def start(self):
        return self['StartTime'].value

    @start.setter
    def start(self, value):
        self['StartTime'].value = value
