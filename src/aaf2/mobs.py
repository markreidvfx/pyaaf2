from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from datetime import datetime
import io

from . import core
from . mobid import MobID
from . utils import register_class, rescale
from . misc import TaggedValueHelper
from . import essence
from . import video
from . import audio
from .rational import AAFRational
from .auid import AUID
from .components import SourceReference


@register_class
class Mob(core.AAFObject):
    """
    Base Class for All Mob Objects
    """

    class_id = AUID("0d010101-0101-3400-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, name=None):
        super(Mob, self).__init__()

        self.name = name or "Mob"
        self.mob_id = MobID.new()

        now = datetime.now()
        self['CreationTime'].value = now
        self['LastModified'].value = now

        self['Slots'].value = []

    @property
    def unique_key(self):
        return self.mob_id

    @property
    def name(self):
        return self['Name'].value

    @name.setter
    def name(self, value):
        self['Name'].value = value

    @property
    def mob_id(self):
        """
        The unique Mob ID associated with this mob. Get Returns :class:`aaf2.mobid.MobID` Object
        """
        return self['MobID'].value

    @mob_id.setter
    def mob_id(self, value):
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
            if slot.slot_id == slot_id:
                return slot
        raise IndexError("No SlotID: %s" % str(slot_id))

    def create_timeline_slot(self, edit_rate, slot_id=None):
        slots = [slot.slot_id for slot in self.slots]
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

    def create_empty_sequence_slot(self, edit_rate, slot_id=None,  media_kind=None):
        """
            Create an empty timeline slot and sets its segment to a new, empty
            `aaf2.components.Sequence` component. Timeline slots are for continuous,
            monotonically-changing media, like picture and sound.
        """
        slot = self.create_timeline_slot(edit_rate, slot_id)
        sequence = self.root.create.Sequence(media_kind=media_kind)
        sequence['Components'].value = []
        slot.segment = sequence
        return slot

    def create_picture_slot(self, edit_rate=25):
        """
            Create an empty timeline slot, with the 'picture' media kind, and sets
            its segment to a new, empty `aaf2.components.Sequence` component.
        """
        return self.create_empty_sequence_slot(edit_rate, media_kind="picture")

    def create_sound_slot(self, edit_rate=25):
        """
            Create an empty timeline slot, with the 'sound' media kind, and sets
            its segment to a new, empty `aaf2.components.Sequence` component.
        """
        return self.create_empty_sequence_slot(edit_rate, media_kind="sound")

    def create_source_clip(self, slot_id=None, start=None, length=None, media_kind=None):
        """
            Create a SourceClip of Mobs slot with `slot_id`. If no length given the default
            length will be the full length of slots segment minus `start`.
            Returns :class:`aaf2.components.SourceClip` Object
        """
        source_slot = self.slot_at(slot_id)
        if not media_kind:
            media_kind = source_slot.media_kind

        clip = self.root.create.SourceClip(media_kind=media_kind)
        clip.mob = self
        clip.slot = source_slot
        clip.start = start or 0
        clip.length = length or max(source_slot.length - clip.start, 0)
        return clip

    def dependant_mobs(self):
        """
            Yields all mobs that this mob is dependant on in depth first order.
        """

        visited = set()
        stack = [self]

        while stack:
            mob = stack[-1]
            children_processed = True

            for obj, _ in mob.walk_references(topdown=True):
                if isinstance(obj, SourceReference):
                    ref_mob = obj.mob
                    if not ref_mob:
                        continue
                    if ref_mob.mob_id not in visited:
                        stack.append(ref_mob)
                        children_processed = False

            if children_processed:
                stack.pop(-1)
                if mob.mob_id not in visited:
                    visited.add(mob.mob_id)
                    if mob is not self:
                        yield mob

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                       self.__class__.__name__)
        s += ' "%s" %s' % (self.name or "", str(self.mob_id))

        return '<%s at 0x%x>' % (s, id(self))


@register_class
class CompositionMob(Mob):
    class_id = AUID("0d010101-0101-3500-060e-2b3402060101")
    __slots__ = ()

@register_class
class MasterMob(Mob):
    class_id = AUID("0d010101-0101-3600-060e-2b3402060101")
    __slots__ = ()

    def import_dnxhd_essence(self, path, edit_rate, tape=None, length=None, offline=False):
        """
        Import video essence from raw DNxHD/DNxHR stream
        """

        # create sourceMob and essencedata
        source_mob = self.root.create.SourceMob("%s.PHYS" % self.name)
        self.root.content.mobs.append(source_mob)

        # import the essencedata
        source_slot = source_mob.import_dnxhd_essence(path, edit_rate, tape, length, offline)

        # create slot and clip that references source_mob slot
        slot = self.create_timeline_slot(edit_rate=edit_rate)
        slot.segment = source_mob.create_source_clip(source_slot.slot_id, media_kind='picture')

        # set clip length
        slot.segment.length = source_slot.segment.length
        return slot

    def import_audio_essence(self, path, edit_rate=None, tape=None, length=None, offline=False):
        """
        Import audio essence from wav file
        """

        # create sourceMob and essencedata
        source_mob = self.root.create.SourceMob("%s.PHYS" % self.name)
        self.root.content.mobs.append(source_mob)

        source_slot = source_mob.import_audio_essence(path, edit_rate, tape, length, offline)

        # create slot and clip that references source_mob slot
        edit_rate = edit_rate or source_slot.edit_rate
        slot = self.create_timeline_slot(edit_rate=edit_rate)
        slot.segment = source_mob.create_source_clip(source_slot.slot_id, media_kind='sound')

        # set clip length
        slot.segment.length = source_slot.segment.length
        return slot


@register_class
class SourceMob(Mob):
    class_id = AUID("0d010101-0101-3700-060e-2b3402060101")
    __slots__ = ()

    @property
    def descriptor(self):
        return self['EssenceDescription'].value

    @descriptor.setter
    def descriptor(self, value):
        self['EssenceDescription'].value = value

    def create_essence(self, edit_rate=None, media_kind='picture', slot_id=None, offline=False):
        # NOTE: appears like a SourceMob can only link to 1 essence and it must be slot 1
        slot = self.create_empty_slot(edit_rate=edit_rate, media_kind=media_kind, slot_id=1)
        if offline:
            return None, slot
        essencedata = self.root.create.EssenceData()
        essencedata.mob_id = self.mob_id
        self.root.content.essencedata.append(essencedata)
        return essencedata, slot

    def create_empty_slot(self, edit_rate=None, media_kind='picture', slot_id=None):
        slot = self.create_timeline_slot(edit_rate, slot_id)
        clip = self.root.create.SourceClip(media_kind=media_kind)
        slot.segment = clip

        return slot

    def create_timecode_slot(self, edit_rate, timecode_fps, drop_frame=False, length=None):
        timecode_slot = self.create_timeline_slot(edit_rate)
        timecode_slot.segment = self.root.create.Timecode(timecode_fps, drop=drop_frame, length=length)
        return timecode_slot

    def create_tape_slots(self, tape_name, edit_rate, timecode_fps, drop_frame=False, media_kind=None, length=None):
        self.name = tape_name
        self.descriptor = self.root.create.TapeDescriptor()

        slot = self.create_empty_slot(edit_rate, media_kind, slot_id=1)
        slot.segment.length = int(float(AAFRational(edit_rate)) * 60 * 60 * 12)  # 12 hours
        timecode_slot = self.create_timecode_slot(edit_rate, timecode_fps, drop_frame, length)

        return slot, timecode_slot

    def import_rawvideo_essence(self, path, edit_rate, width, height, pixel_layout, tape=None):
        essencedata, slot = self.create_essence(edit_rate, 'picture')

        if tape:
            slot.segment = tape

        # create essence descriptor
        descriptor = self.root.create.RGBADescriptor()
        self.descriptor = descriptor

        alignment = 8192

        # set minimal properties
        descriptor['SampleRate'].value = edit_rate
        descriptor['VideoLineMap'].value = [42, 0] # Not exactly sure what linemap is
        descriptor['ContainerFormat'].value = self.root.dictionary.lookup_containerdef("AAF")

        descriptor['StoredWidth'].value = width
        descriptor['StoredHeight'].value = height
        descriptor['ImageAlignmentFactor'].value = alignment
        descriptor['PixelLayout'].value = pixel_layout
        descriptor['FrameLayout'].value = "FullFrame"
        descriptor['ImageAspectRatio'].value = "%d/%d" % (width, height)

        raw_frame_size_bits = 0
        for layout in pixel_layout:
            raw_frame_size_bits += layout.get('Size', 0) * width * height

        raw_frame_size = (raw_frame_size_bits + 7) // 8
        frame_size = (raw_frame_size + (alignment-1)) // alignment * alignment

        descriptor['FrameSampleSize'].value = frame_size

        # open essence stream
        stream = essencedata.open('w')
        length = 0
        alignment_padding = bytearray(frame_size - raw_frame_size)

        with io.open(path, 'rb', buffering=io.DEFAULT_BUFFER_SIZE) as f:
            while True:
                data = f.read(raw_frame_size)
                if not data:
                    break
                stream.write(data)
                if alignment_padding:
                    stream.write(alignment_padding)
                length += 1

        descriptor['Length'].value = length
        descriptor['ImageSize'].value = length * frame_size
        slot.segment.length = length

        return slot

    def import_dnxhd_essence(self, path, edit_rate, tape=None, length=None, offline=False):
        """
        Import video essence from raw DNxHD/DNxHR stream
        """

        essencedata, slot = self.create_essence(edit_rate, 'picture', offline=offline)

        if tape:
            slot.segment = tape

        # create essence descriptor
        descriptor = self.root.create.CDCIDescriptor()
        self.descriptor = descriptor

        # set minimal properties
        descriptor['SampleRate'].value = edit_rate
        descriptor['VideoLineMap'].value = [42, 0] # Not exactly sure what linemap is
        descriptor['ContainerFormat'].value = self.root.dictionary.lookup_containerdef("AAF")
        dnxhd_codec_auid = AUID("8ef593f6-9521-4344-9ede-b84e8cfdc7da")
        descriptor['CodecDefinition'].value = self.root.dictionary.lookup_codecdef(dnxhd_codec_auid)

        stream = None
        if essencedata is not None:
            # open essence stream
            stream = essencedata.open('w')

        # open input file
        with io.open(path, 'rb', buffering=io.DEFAULT_BUFFER_SIZE) as f:

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
                    descriptor['Compression'].value = video.dnx_compression_auids[cid]
                    descriptor['HorizontalSubsampling'].value = 2

                if stream is not None:
                    stream.write(packet)
        # set descriptor and component lengths
        slot.segment.length = length or i
        descriptor.length = i

        return slot

    def import_audio_essence(self, path, edit_rate=None, tape=None, length=None, offline=False):
        """
        Import audio essence from wav file
        """

        # read the wav file header
        a = audio.WaveReader(path)
        sample_rate = a.getframerate()
        channels = a.getnchannels()
        sample_width = a.getsampwidth()
        block_align = a.getblockalign()
        frames = a.getnframes()

        edit_rate = edit_rate or sample_rate

        # create essencedata
        essencedata, slot = self.create_essence(edit_rate, 'sound', offline=offline)
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
        descriptor.length = frames
        slot.segment.length = length or int(rescale(frames, sample_rate, edit_rate))

        if essencedata is not None:
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
        return self.root.content.essencedata.get(self.mob_id, None)
