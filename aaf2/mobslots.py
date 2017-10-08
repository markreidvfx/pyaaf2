from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
from . import core
from .utils import register_class

@register_class
class MobSlot(core.AAFObject):
    class_id = UUID("0d010101-0101-3800-060e-2b3402060101")

    @property
    def segment(self):
        return self['Segment'].value

    @segment.setter
    def segment(self, value):
        self['Segment'].value = value

    @property
    def name(self):
        return self['SlotName'].value

    @name.setter
    def name(self, value):
        self['SlotName'].value = value

    @property
    def id(self):
        return self['SlotID'].value

    @id.setter
    def id(self, value):
        self['SlotID'].value = value


@register_class
class EventMobSlot(MobSlot):
    class_id = UUID( "0d010101-0101-3900-060e-2b3402060101")

@register_class
class TimelineMobSlot(MobSlot):
    class_id = UUID("0d010101-0101-3b00-060e-2b3402060101")
