from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from . import core
from . utils import register_class
from . mobid import MobID
from . dictionary import DataDef

class Component(core.AAFObject):
    class_id = UUID("0d010101-0101-0200-060e-2b3402060101")
    def __init__(self, length=None, media_kind=None):
        self.length = length or 0
        self.media_kind = media_kind or 'picture'

    @property
    def length(self):
        return self['Length'].value

    @length.setter
    def length(self, value):
        self['Length'].value = value

    @property
    def datadef(self):
        return self['DataDefinition'].value

    @datadef.setter
    def datadef(self, value):
        self['DataDefinition'].value = value

    @property
    def media_kind(self):
        datadef = self.datadef
        if datadef:
            return datadef.short_name

    @media_kind.setter
    def media_kind(self, value):
        self.datadef = self.root.dictionary.lookup_datadef(value)

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
        return self.root.content.mobs.get(mod_id, None)

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

    def __init__(self, start=None, length=None, mob_id=None, slot_id=None, media_kind=None):
        super(SourceClip, self).__init__(length, media_kind)
        self.start = start or 0
        self.mob_id = mob_id or MobID()
        self.slot_id = slot_id or 0

    @property
    def start(self):
        return self['StartTime'].value

    @start.setter
    def start(self, value):
        self['StartTime'].value = value

@register_class
class Timecode(Segment):
    class_id = UUID("0d010101-0101-1400-060e-2b3402060101")

    def __init__(self, fps=25, drop=False):
        length = fps * 60 * 60 * 12 # 12 hours
        super(Timecode, self).__init__(length=length, media_kind='Timecode')
        self.start = 0
        self.fps = fps
        self.drop = drop

    @property
    def start(self):
        return self['Start'].value

    @start.setter
    def start(self, value):
        self['Start'].value = value

    @property
    def fps(self):
        return self['FPS'].value

    @fps.setter
    def fps(self, value):
        self['FPS'].value = value

    @property
    def drop(self):
        return self['Drop'].value

    @drop.setter
    def drop(self, value):
        self['Drop'].value = value
