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
    """
    A :class:`aaf2.mobs.Mob` can have many `MobSlot`s, each one containing a 
    :class:`aaf2.components.Segment` (like a :class:`aaf2.components.SourceClip`
    or a :class:`aaf2.components.Sequence`).
    
    `MobSlot has three subclasses, pertaining to the relationship the segment
    has to time:

        * :class:`aaf2.mobslots.StaticMobSlot`: These contain a segment that is 
          static over time, like a still image.

        * :class:`aaf2.mobslots.TimelineMobSlot`: These contain a segment that
          changes continusously and periodically over time, like moving picture,
          audio, or compositions.

        * :class:`aaf2.mobslots.EventMobSlot`: These contain segments that 
          change intermittently and variably, like timed comments and GPI 
          triggers.
    """

    class_id = UUID("0d010101-0101-3800-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, slot_id=None, name=None, segment=None):
        super(MobSlot, self).__init__()
        self.slot_id = slot_id
        self.name = name
        if slot_id is not None and name is None:
            self.name = "Track-%03d" % slot_id
        self.segment = segment

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
    def datadef(self):
        segment = self.segment
        if segment:
            return segment.datadef

    @property
    def media_kind(self):
        segment = self.segment
        if segment:
            return segment.media_kind

    @property
    def slot_id(self):
        return self['SlotID'].value

    @slot_id.setter
    def slot_id(self, value):
        self['SlotID'].value = value

    def __repr__(self):
        name = self.name
        slot_id = self.slot_id
        s = "%s.%s" % (self.__class__.__module__,
                       self.__class__.__name__)

        if slot_id is not None:
            s += " %d" % slot_id
        if name:
            s += ' "%s"' % name

        return '<%s at 0x%x>' % (s, id(self))

@register_class
class EventMobSlot(MobSlot):
    class_id = UUID( "0d010101-0101-3900-060e-2b3402060101")
    __slots__ = ()

@register_class
class TimelineMobSlot(MobSlot):
    class_id = UUID("0d010101-0101-3b00-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, slot_id=None, name=None, segment=None, origin=None, edit_rate=None):
        super(TimelineMobSlot, self).__init__(slot_id, name, segment)
        self.origin = origin or 0
        self.edit_rate = edit_rate or 25

    @property
    def origin(self):
        return self['Origin'].value
    @origin.setter
    def origin(self, value):
        self['Origin'].value = value

    @property
    def edit_rate(self):
        return self['EditRate'].value

    @edit_rate.setter
    def edit_rate(self, value):
        self['EditRate'].value = value

@register_class
class StaticMobSlot(MobSlot):
    class_id = UUID("0d010101-0101-3a00-060e-2b3402060101")
    __slots__ = ()
