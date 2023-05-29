from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from . import core
from . utils import register_class
from . mobid import MobID
from . dictionary import DataDef
from .auid import AUID


class Component(core.AAFObject):
    class_id = AUID("0d010101-0101-0200-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, media_kind=None, length=None):
        super(Component, self).__init__()
        self.media_kind = media_kind or 'picture'
        self.length = length or 0

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
    class_id = AUID("0d010101-0101-0300-060e-2b3402060101")
    __slots__ = ()

@register_class
class Transition(Component):
    class_id = AUID("0d010101-0101-1700-060e-2b3402060101")
    __slots__ = ()

    @property
    def cutpoint(self):
        return self['CutPoint'].value

    @cutpoint.setter
    def cutpoint(self, value):
        self['CutPoint'].value = value


@register_class
class Sequence(Segment):
    class_id = AUID("0d010101-0101-0f00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, media_kind=None, length=None):
        super(Sequence, self).__init__(media_kind, length)
        # initialize components to empty list
        self.components.value = []

    @property
    def components(self):
        return self['Components']

    def component_at_time(self, edit_unit):
        return self.components[self.index_at_time(edit_unit)]

    def index_at_time(self, edit_unit):
        last_component = None
        last_index = None

        if edit_unit <= 0:
            return 0

        # this needs to go past target index to handle Transitions
        for index, position, component in self.positions():

            if isinstance(component, Transition):
                if position <= edit_unit < position + component.length:
                    return index

            # gone past return previous
            if last_component and position >= edit_unit:
                return last_index

            last_component = component
            last_index = index

        return last_index

    def positions(self):
        length = 0
        for index, component in enumerate(self.components):

            if isinstance(component, Transition):
                length -= component.length
                yield (index, length, component)
            else:
                yield (index, length, component)
                length += component.length


@register_class
class NestedScope(Segment):
    class_id = AUID("0d010101-0101-0b00-060e-2b3402060101")
    __slots__ = ()

    @property
    def slots(self):
        return self['Slots']


class SourceReference(Segment):
    class_id = AUID("0d010101-0101-1000-060e-2b3402060101")
    __slots__ = ()

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
        self.mob_id = value.mob_id

    @property
    def slot(self):
        slot_id = self.slot_id
        mob = self.mob
        if mob is None or slot_id is None:
            return
        return mob.slot_at(slot_id)

    @slot.setter
    def slot(self, value):
        self.slot_id = value.slot_id


@register_class
class SourceClip(SourceReference):
    class_id = AUID("0d010101-0101-1100-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, start=None, length=None, mob_id=None, slot_id=None, media_kind=None):
        super(SourceClip, self).__init__(media_kind=media_kind, length=length)
        self.start = start or 0
        self.mob_id = mob_id or MobID()
        self.slot_id = slot_id or 0

    @property
    def start(self):
        return self['StartTime'].value

    @start.setter
    def start(self, value):
        self['StartTime'].value = value

    def walk(self):
        if not self.slot:
            return

        segment = self.slot.segment

        if isinstance(segment, SourceClip):
            yield segment
            for item in segment.walk():
                yield item

        elif isinstance(segment, Sequence):
            try:
                clip = segment.component_at_time(self.start)
            except AttributeError as e:
                print(e)
            else:
                if isinstance(clip, SourceClip):
                    yield clip
                    for item in clip.walk():
                        yield item
                else:
                    raise NotImplementedError("Sequence returned {} not "
                                              "implemented".format(
                                                  type(segment)))

        elif isinstance(segment, EssenceGroup):
            yield segment

        elif isinstance(segment, Filler):
            yield segment

        elif isinstance(segment, (OperationGroup, Pulldown)):
            yield segment

        else:
            raise NotImplementedError("Walking {} not implemented".format(
                                      type(segment)))


@register_class
class Filler(Segment):
    class_id = AUID("0d010101-0101-0900-060e-2b3402060101")
    __slots__ = ()

@register_class
class EssenceGroup(Segment):
    class_id = AUID("0d010101-0101-0500-060e-2b3402060101")
    __slots__ = ()

@register_class
class EdgeCode(Segment):
    class_id = AUID("0d010101-0101-0400-060e-2b3402060101")
    __slots__ = ()

@register_class
class Pulldown(Segment):
    class_id = AUID("0d010101-0101-0c00-060e-2b3402060101")
    __slots__ = ()

@register_class
class ScopeReference(Segment):
    class_id = AUID("0d010101-0101-0d00-060e-2b3402060101")
    __slots__ = ()

@register_class
class Selector(Segment):
    class_id = AUID("0d010101-0101-0e00-060e-2b3402060101")
    __slots__ = ()

@register_class
class Timecode(Segment):
    class_id = AUID("0d010101-0101-1400-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, fps=25, drop=False, length=None):
        length = length or fps * 60 * 60 * 12  # 12 hours
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


@register_class
class OperationGroup(Segment):
    class_id = AUID("0d010101-0101-0a00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, operationdef, length=None, media_kind=None):
        super(OperationGroup, self).__init__(media_kind=media_kind, length=length)
        self.operation = self.root.dictionary.lookup_operationdef(operationdef)

        if self.media_kind is None:
            self.media_kind = self.operation.media_kind

    @property
    def operation(self):
        return self['Operation'].value

    @operation.setter
    def operation(self, value):
        self['Operation'].value = value

    @property
    def parameters(self):
        return self['Parameters']

    @parameters.setter
    def parameters(self, value):
        self['Parameters'] = value

    @property
    def segments(self):
        return self['InputSegments']


class Event(Segment):
    class_id = AUID("0d010101-0101-0600-060e-2b3402060101")
    __slots__ = ()

    def __init__(self):
        super(Event, self).__init__(media_kind='DescriptiveMetadata')


@register_class
class CommentMarker(Event):
    class_id = AUID("0d010101-0101-0800-060e-2b3402060101")
    __slots__ = ()

@register_class
class DescriptiveMarker(CommentMarker):
    class_id = AUID("0d010101-0101-4100-060e-2b3402060101")
    __slots__ = ()
