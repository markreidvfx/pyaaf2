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
    """
    The :obj:`Component` class represents an essence element.
    The :obj:`Component` class is an abstract class.

    Note on `length` property:
        If a Component is in a `TimelineMobSlot`, then it shall have a Length 
        property. If a Component is in a `StaticMobSlot`, then it shall not 
        have a Length property. If a Component is in an `EventMobSlot`, then 
        it may have a Length property.
        
        If a Component in an EventMobSlot does not have a Length property, then
        the Component describes an instantaneous event that does not have a 
        duration.

    """

    class_id = UUID("0d010101-0101-0200-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, media_kind=None, length=None):
        self.media_kind = media_kind or 'picture'
        self.length = length or 0

    @property
    def length(self):
        """
        Length of this component in edit units of this component.
        """
        return self['Length'].value

    @length.setter
    def length(self, value):
        self['Length'].value = value

    @property
    def datadef(self):
        """
        The DataDefinition for this component.
        """
        return self['DataDefinition'].value

    @datadef.setter
    def datadef(self, value):
        self['DataDefinition'].value = value

    @property
    def media_kind(self):
        """
        Return the short name of the datadef: 'sound', 'picture' etc.
        """
        datadef = self.datadef
        if datadef:
            return datadef.short_name

    @media_kind.setter
    def media_kind(self, value):
        self.datadef = self.root.dictionary.lookup_datadef(value)

class Segment(Component):
    """
    The Segment class represents a Component that is independent of any surrounding object. 
    The Segment class is an abstract class.
    """
    class_id = UUID("0d010101-0101-0300-060e-2b3402060101")
    __slots__ = ()

@register_class
class Transition(Component):
    """
    
    A `Transition` can occur in a `Sequence` between two `Segment`s. The 
    Transition causes the preceding and following Segments to overlap in time. 
    The Transition specifies an effect that is used to combine the overlapping 
    Segments. Figure 24 below illustrates the Sequence containment showing 
    Transition, which itself has an `Effect`. A Transition object shall be in a
    `Sequence` within a `CompositionMob`.
    """

    class_id = UUID("0d010101-0101-1700-060e-2b3402060101")
    __slots__ = ()

@register_class
class Sequence(Segment):
    """
    The `Sequence` object combines a series of timeline `Components` in 
    sequential order. If the `Sequence` has only `Segments`, each `Segment` is 
    played sequentially after the `Segment` that precedes it. The time in the 
    Composition Mob that a `Segment` starts is determined by the Components 
    that  precede it in the Sequence.

    To calculate the duration of a Sequence with Transitions, you add the 
    durations of the Segments and then subtract the duration of the 
    Transitions. In the example in the above Figure, the duration of the 
    Sequence is 125 + 100 + 80 - 75, which equals 230.
          
    """
    class_id = UUID("0d010101-0101-0f00-060e-2b3402060101")
    __slots__ = ()

    @property
    def components(self):
        return self['Components']

@register_class
class NestedScope(Segment):
    """
    Defines a scope of slots that can reference each other. The Nested Scope 
    object produces the values of the last slot within it. Typically, Nested 
    Scopes are used to enable layering or to allow a component to be shared.

    """
    class_id = UUID("0d010101-0101-0b00-060e-2b3402060101")
    __slots__ = ()

    @property
    def slots(self):
        return self['Slots']

class SourceReference(Segment):
    """
    The `SourceReference` class represents the essence or other data described 
    by a `MobSlot` in a `Mob`. The SourceReference class is an abstract class.

    A `SourceReference` object in a `Mob` refers to a MobSlot in another Mob by 
    specifying the second Mob's `MobID` and the `SlotID` of the MobSlot owned 
    by it.
    
    To reference a single channel of a multi-channel track from a mono track, 
    the `SourceReference::ChannelIDs` property is used with a single element in 
    the array. To reference multiple channels of a multi-channel track from a 
    multi-channel track, the `SourceReference::ChannelIDs` property is used with 
    multiple elements in the array.

    Toreference multiple mono tracks from a multi-channel track, the 
    `SourceReference::MonoSourceSlotIDs` is used with multiple elements in the 
    array.
    
    """
    class_id = UUID("0d010101-0101-1000-060e-2b3402060101")
    __slots__ = ()

    @property
    def mob_id(self):
        """
        The `MobID` of the source MOB this object references.
        """

        return self['SourceID'].value

    @mob_id.setter
    def mob_id(self, value):
        self['SourceID'].value = value

    @property
    def slot_id(self):
        """
        The `SlotID` of this source MOB this object references.
        """
        return self['SourceMobSlotID'].value

    @slot_id.setter
    def slot_id(self, value):
        self['SourceMobSlotID'].value = value

    @property
    def mob(self):
        """
        Look up the `MobID` in the root's `ContentStorage` and get the referred 
        `Mob`.
        """
        mod_id = self.mob_id
        if mod_id is None or mod_id.int == 0:
            return None
        return self.root.content.mobs.get(mod_id, None)

    @mob.setter
    def mob(self, value):
        self.mob_id = value.mob_id

    @property
    def slot(self):
        """
        Look up the `MobID` in the root's `ContentStorage` and get the slot 
        for`slot_id`.
        """

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
    """
    A `Mob` can reference another Mob to indicate the source or derivation of 
    the essence. A Mob refers to another Mob by having a `SourceClip` object. A 
    `SourceClip` object has a weak reference to a Mob using its identifying 
    MobID value; shall identify a `MobSlot` within the referenced Mob with a 
    `SlotID` value; and when referencing a `TimelineMobSlot` shall specify an 
    offset in time within the referenced TimelineMobSlot.

    SourceClips in `CompositionMobs` specify the MobID of the MasterMob, and 
    are used to represent pieces of digital essence data. The MasterMob provides 
    a level of indirection between the digital essence data and the objects that 
    refer to them.
    
    SourceClips in `File` SourceMobs specify the MobID of a Physical SourceMob. 
    For example, a video File SourceMob has a SourceClip that specifies the 
    Physical SourceMob describing a videotape used to generate the digital video 
    data.

    SourceClips in Physical SourceMobs identify the MobID of a previous physical 
    source of physical media. For example, a videotape SourceMob has a SourceClip 
    that specifies the Physical SourceMob describing the film that was used to 
    generate the videotape.
    """
    class_id = UUID("0d010101-0101-1100-060e-2b3402060101")
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
        else:
            raise NotImplementedError("Walking {} not implemented".format(
                                      type(segment)))

@register_class
class Filler(Segment):
    """
    The Filler class represents an unspecified value for the duration of the 
    object.

    Typically, a Filler object is used in a Sequence to allow positioning of a 
    `Segment` when not all of the preceding material has been specified. 
    Another typical use of Filler objects is to fill time in `MobSlot`s and 
    `NestedScope` tracks that are not referenced or played.
    
    If a `Filler` object is played, applications can choose any appropriate 
    blank essence to play. Typically, a video Filler object would be played as 
    a black section, and an audio Filler object would be played as a silent 
    section.
    """

    class_id = UUID("0d010101-0101-0900-060e-2b3402060101")
    __slots__ = ()

@register_class
class EssenceGroup(Segment):
    class_id = UUID("0d010101-0101-0500-060e-2b3402060101")
    __slots__ = ()

@register_class
class EdgeCode(Segment):
    """
    The Edgecode class stores film edge code information.

    An Edgecode object shall have an Edgecode data definition.
    """
    class_id = UUID("0d010101-0101-0400-060e-2b3402060101")
    __slots__ = ()

@register_class
class Pulldown(Segment):
    """
    The Pulldown class is a sub-class of the Segment class.
    
    Pulldown objects are typically used in file `SourceMobs` and physical 
    `SourceMobs`.

    A Pulldown object provides a mechanism to convert from essence between 
    video and film rates and describes the mechanism that was used to convert 
    the essence.

    """
    class_id = UUID("0d010101-0101-0c00-060e-2b3402060101")
    __slots__ = ()

@register_class
class ScopeReference(Segment):
    """
    Refers to a section in a Nested Scope slot.
    """
    class_id = UUID("0d010101-0101-0d00-060e-2b3402060101")
    __slots__ = ()

@register_class
class Selector(Segment):
    """
    Specifies a selected `Segment` and preserves references to some 
    alternative Segments that were available during the editing session. The 
    alternative Segments can be ignored while playing a Composition Mob because 
    they do not effect the value of the Selector object and cannot be 
    referenced from outside of it. The alternative Segments can be presented to 
    the user when the Composition Mob is being edited. Typically, a Selector 
    object is used to present alternative presentations of the same content, 
    such as alternate camera angles of the same scene.
    """
    class_id = UUID("0d010101-0101-0e00-060e-2b3402060101")
    __slots__ = ()

@register_class
class Timecode(Segment):
    """
    The Timecode class stores videotape or audio tape timecode information. A 
    Timecode object shall have a Timecode `DataDefinition`.

    A Timecode object can typically appear in either a `SourceMob` or in a 
    `Composition Mob`. In a `SourceMob`, it typically appears in a `MobSlot` in 
    a `SourceMob` that describes a videotape or audio tape. In this context, it 
    describes the timecode that exists on the tape. In a Composition Mob, it 
    represents the timecode associated with the virtual media represented by 
    the Composition Mob. If the Composition Mob is rendered to a videotape, the 
    Timecode should be used to generate the timecode on the videotape.


    """
    class_id = UUID("0d010101-0101-1400-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, fps=25, drop=False):
        length = fps * 60 * 60 * 12 # 12 hours
        super(Timecode, self).__init__(length=length, media_kind='Timecode')
        self.start = 0
        self.fps = fps
        self.drop = drop

    @property
    def start(self):
        """
        Specifies the timecode at the beginning of the segment.
        """
        return self['Start'].value

    @start.setter
    def start(self, value):
        self['Start'].value = value

    @property
    def fps(self):
        """
        Frames per second of the videotape or audio tape.
        """
        return self['FPS'].value

    @fps.setter
    def fps(self, value):
        self['FPS'].value = value

    @property
    def drop(self):
        """
        Indicates whether the timecode is drop (True value) or nondrop (False value)
        """
        return self['Drop'].value

    @drop.setter
    def drop(self, value):
        self['Drop'].value = value

@register_class
class OperationGroup(Segment):
    """
    The `OperationGroup` class contains an ordered set of `Segments` and an 
    operation that is performed on these Segments.
    
    """
    class_id = UUID("0d010101-0101-0a00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, operationdef, length=None):
        super(OperationGroup, self).__init__(length=length)
        self.operation = operationdef
        self.media_kind = self.operation.media_kind

    @property
    def operation(self):
        """
        The `OperationDefiniton`.
        """
        return self['Operation'].value

    @operation.setter
    def operation(self, value):
        self['Operation'].value = value

    @property
    def parameters(self):
        """
        The list of parameters.
        """
        return self['Parameters']

    @property
    def segments(self):
        """
        The list of input segments.
        """
        return self['InputSegments']

class Event(Segment):
    class_id = UUID("0d010101-0101-0600-060e-2b3402060101")
    __slots__ = ()

    def __init__(self):
        super(Event, self).__init__(media_kind='DescriptiveMetadata')


@register_class
class CommentMarker(Event):
    """
    The `CommentMarker` class specifies a user comment that is associated with 
    a point in time.
    
    To correlate `CommentMarker`s with a `MobSlot` to which they may refer, the 
    `EventMobSlot` may be given the same data definition and the same 
    `PhysicalTrackNumber` as the target `MobSlot`.
    """
    class_id = UUID("0d010101-0101-0800-060e-2b3402060101")
    __slots__ = ()


@register_class
class DescriptiveMarker(CommentMarker):
    class_id = UUID("0d010101-0101-4100-060e-2b3402060101")
    __slots__ = ()
