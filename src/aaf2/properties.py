from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from io import BytesIO
import weakref
import struct

from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    write_u8,
    write_u16le,
    write_u32le,
    decode_utf16le,
    encode_utf16le,
    encode_utf16_array,
    encode_auid_array,
    encode_u16le,
    encode_u32le,
    encode_u8,
    encode_s64le,
    mangle_name,
    )
from .auid import AUID
from .mobid import MobID
from .exceptions import AAFPropertyError, AAFAttachError

SF_DATA                                   = 0x82
SF_DATA_STREAM                            = 0x42
SF_STRONG_OBJECT_REFERENCE                = 0x22
SF_STRONG_OBJECT_REFERENCE_VECTOR         = 0x32
SF_STRONG_OBJECT_REFERENCE_SET            = 0x3A
SF_WEAK_OBJECT_REFERENCE                  = 0x02
SF_WEAK_OBJECT_REFERENCE_VECTOR           = 0x12
SF_WEAK_OBJECT_REFERENCE_SET              = 0x1A

# these formats are defined by spec but not used
SF_WEAK_OBJECT_REFERENCE_STORED_OBJECT_ID = 0x03
SF_UNIQUE_OBJECT_ID                       = 0x86
SF_OPAQUE_STREAM                          = 0x40
SF_DATA_VECTOR                            = 0xD2
SF_DATA_SET                               = 0xDA

CLASSDEF_AUID          = AUID("0d010101-0101-0100-060e-2b3402060101")
TYPEDEF_AUID           = AUID("0d010101-0203-0000-060e-2b3402060101")

MOB_MOBID_AUID         = AUID("01011510-0000-0000-060e-2b3401010101")
ESSENCEDATA_MOBID_AUID = AUID("06010106-0100-0000-060e-2b3401010102")

PROPERTY_VERSION=32
sentinel = object()


def writeonly(func):
    def func_wrapper(self, *args, **kwargs):
        if not self.writeable:
            raise AAFPropertyError("file readonly")
        result = func(self, *args, **kwargs)
        self.mark_modified()
        return result

    return func_wrapper


class Property(object):
    __slots__ = ('pid', 'format', 'version', 'data', 'parent', '_propertydef')
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        self.pid = pid
        self.format = format
        self.version = version
        self.data = None
        self._propertydef = None
        self.parent = parent

    def format_name(self):
        return str(property_formats[self.format].__name__)

    @property
    def attached(self):
        if self.parent.dir:
            return True
        return False

    @property
    def writeable(self):
        if self.parent.root.mode in ('rb', ):
            return False
        return True

    def decode(self):
        pass

    def mark_modified(self):
        if self.attached:
            self.parent.root.manager.add_modified(self.parent)

    @property
    def propertydef(self):
        if self._propertydef:
            return self._propertydef

        classdef = self.parent.classdef
        if classdef is None:
            return

        p = classdef.get_propertydef_from_pid(self.pid)
        if p:
            self._propertydef = p
            return p

        # fall back to slow method if early in the bootstraping process
        # seems to be on ClassDefinitions
        for p in classdef.all_propertydefs():
            if p.pid == self.pid:
                self._propertydef = p
                return p
    @property
    def unique(self):
        return self.propertydef.unique

    @property
    def name(self):
        propertydef = self.propertydef
        if propertydef:
            return propertydef.property_name

    @property
    def typedef(self):
        propertydef = self.propertydef
        if propertydef:
            return propertydef.typedef

    def copy(self, parent, pid, cache=None):
        p = self.__class__(parent, pid, self.format, version=PROPERTY_VERSION)
        p.data = bytes(self.data)
        return p

    @property
    def value(self):
        d = self.data
        if d is None:
            return None
        return self.typedef.decode(d)

    @value.setter
    @writeonly
    def value(self, value):
        if self.data is not None and self.parent.dir and self.unique:
            if self.propertydef.auid == MOB_MOBID_AUID:
                self.parent.root.content.mobs.swap_unique_key(self.value, value)
            elif self.propertydef.auid == ESSENCEDATA_MOBID_AUID:
                self.parent.root.content.essencedata.swap_unique_key(self.value, value)
            else:
                raise AAFPropertyError("cannot change unique property value of attached object")

        if value is None:
            self.remove_pid_entry()
            return

        self.data = self.typedef.encode(value)
        self.add_pid_entry()

    def add_pid_entry(self):
        if not self.pid in self.parent.property_entries:
            self.parent.property_entries[self.pid] = self
        return self

    def remove_pid_entry(self):
        if self.pid in self.parent.property_entries:
            del self.parent.property_entries[self.pid]

    def __repr__(self):
        name = self.name
        if name:
            return "<%s %s>" % (name, str(self.typedef))
        else:
            return "<%s %d bytes>" % (self.__class__.__name__, len(self.data))


class StreamProperty(Property):
    __slots__ = ('stream_name', 'dir')
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StreamProperty, self).__init__(parent, pid, format, version)
        self.stream_name = None
        self.dir = None

    def copy(self, parent, pid, cache):
        p = super(StreamProperty, self).copy(parent, pid)
        a = self.open('r')
        b = p.open("w")

        byte_size = a.dir.byte_size
        read_size = self.parent.root.cfb.sector_size

        # copy stream data
        while byte_size > 0:
            d = a.read(read_size)
            b.write(d)
            byte_size -= len(d)

        return p

    def decode(self):
        # first byte is endianness
        assert self.data[0:1] == b'\x55' # unspecified
        self.stream_name = decode_utf16le(self.data[1:])

    def encode(self, data):
        return  b'\x55' + encode_utf16le(data)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.stream_name))

    def setup_stream(self):
        if self.stream_name:
            return

        self.stream_name = mangle_name(self.propertydef.property_name, self.pid, 32)
        self.data = self.encode(self.stream_name)
        self.add_pid_entry()

    def open(self, mode='r'):
        self.setup_stream()

        if mode == 'r':
            if self.attached:
                stream = self.parent.dir.get(self.stream_name)
            else:
                stream = self.dir

            if not stream:
                raise AAFPropertyError("cannot find stream: %s" % self.stream_name)
            return stream.open(mode)
        else:
            if not self.writeable:
                raise AAFPropertyError("file readonly")

            if self.attached:
                return self.parent.dir.touch(self.stream_name).open(mode)
            else:
                if self.dir is None:
                    tmp_dir = self.parent.root.manager.create_temp_dir()
                    stream = tmp_dir.touch(self.stream_name).open(mode)
                    self.dir = stream.dir
                    return stream

                return self.dir.open(mode)

    def detach(self):
        if self.stream_name is None:
            raise AAFAttachError("stream has no name")

        stream = self.parent.dir.get(self.stream_name)
        if not stream:
            raise AAFAttachError("stream doesn't exists")

        stream_path = stream.path()
        tmp = self.parent.root.manager.create_temp_dir().path()
        self.dir = self.parent.root.cfb.move(stream_path, tmp + "/" + self.stream_name)

    def attach(self):
        if self.dir is None:
            return

        if self.parent.dir is None:
            raise AAFAttachError("stream parent not attached")

        if self.stream_name is None:
            raise AAFAttachError("stream has no name")

        stream = self.parent.dir.get(self.stream_name)
        if stream:
            raise AAFAttachError("dest stream already exists")

        stream_path = self.parent.dir.path() + "/" + self.stream_name
        self.parent.root.cfb.move(self.dir.path(), stream_path)

        self.dir = None

    @property
    def value(self):
        return self.parent.dir.get(self.stream_name)


class StrongRefProperty(Property):
    __slots__ = ('ref', 'objectref')
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StrongRefProperty, self).__init__(parent, pid, format, version)
        self.ref = None
        self.objectref = None

    @property
    def object(self):
        if self.objectref is None:
            return None
        elif isinstance(self.objectref, weakref.ref):
            return self.objectref()
        else:
            return self.objectref

    @object.setter
    def object(self, value):
        if value is None:
            self.objectref = None
        elif self.attached:
            self.objectref = weakref.ref(value)
        else:
            self.objectref = value

    def copy(self, parent, pid, cache):
        p = super(StrongRefProperty, self).copy(parent, pid)
        if parent.root is self.parent.root:
            p.ref = self.ref
            dir_entry = None
            if parent.dir:
                dir_entry = parent.dir.get(p.ref)
                if dir_entry is None:
                    dir_entry = parent.dir.makedir(p.ref)

            p.object = self.value.copy(dir_entry)
        else:
            p.value = self.value.copy(root=parent.root, classdef_cache=cache)
        return p

    def decode(self):
        self.ref = decode_utf16le(self.data)

    def encode(self, data):
        return encode_utf16le(data)

    def __repr__(self):
        return "<%s %s to %s>" % (self.name, self.__class__.__name__, str(self.ref))

    @property
    def value(self):
        if self.object:
            return self.object
        dir_entry = self.parent.dir.get(self.ref)
        obj = None
        if dir_entry:
            obj = self.parent.root.manager.read_object(dir_entry)
            self.object = obj
        return obj

    @value.setter
    @writeonly
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        typedef = self.typedef
        ref_classdef = typedef.ref_classdef

        if not ref_classdef.isinstance(value.classdef):
            raise TypeError("must be instance of: %s" % ref_classdef.class_name)

        if value.root is not self.parent.root:
            raise AAFAttachError("Object is from a different root")

        if self.ref is None:
            propdef = self.propertydef
            self.ref = mangle_name(propdef.property_name, self.pid, 32)
            self.data = self.encode(self.ref)

        # before assigning new object detach old
        if self.object:
            self.object.detach()
            self.object = None

        self.object = value
        if not self.pid in self.parent.property_entries:
            self.parent.property_entries[self.pid] = self

        self.attach()

    def detach(self):
        # convert to regular ref
        self.objectref = self.value

    def attach(self):

        obj = self.value

        if not self.object:
            return

        if not self.parent.dir:
            return

        dir_entry = self.parent.dir.get(self.ref)
        if dir_entry is None:
            dir_entry = self.parent.dir.makedir(self.ref)
        if self.object.dir != dir_entry:
            self.object.attach(dir_entry)

        # convert to weakref
        self.objectref = weakref.ref(obj)


class StrongRefVectorProperty(Property):
    __slots__ = ('references', 'next_free_key', 'last_free_key','objects', '_index_name')

    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StrongRefVectorProperty, self).__init__(parent, pid, format, version)
        self.references = []
        self._index_name = None

        # self.ref = None
        self.next_free_key = 0
        self.last_free_key = 0xFFFFFFFF

        if self.attached:
            self.objects = weakref.WeakValueDictionary()
        else:
            self.objects = {}

    def copy(self, parent, pid, cache):
        p = super(StrongRefVectorProperty, self).copy(parent, pid)

        if parent.root is self.parent.root:
            p.objects = {}
            p.references = list(self.references)
            p.index_name = p.index_name
            p.next_free_key = self.next_free_key
            p.last_free_key = self.last_free_key
            p.data = self.data

            for i, value in enumerate(self):
                ref = self.index_ref_name(self.references[i])
                dir_entry = None
                if parent.dir:
                    dir_entry = parent.dir.get(ref)
                    if dir_entry is None:
                        dir_entry = parent.dir.makedir(ref)

                c = value.copy(dir_entry)
                p.objects[i] = c
        else:
            for i, value in enumerate(self):
                c = value.copy(root=parent.root, classdef_cache=cache)
                p.append(c)

        return p

    @property
    def index_name(self):
        if self._index_name:
            return self._index_name

        propdef = self.propertydef
        name = mangle_name(propdef.property_name, self.pid, 32-10)
        self.data = self.encode(name)
        self._index_name = name
        return name

    @index_name.setter
    def index_name(self, value):
        self._index_name = value

    def encode(self, data):
        return encode_utf16le(data)

    def decode(self):
        self.index_name = decode_utf16le(self.data)

    def read_index(self):
        index_name = self.index_name + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole index
        with BytesIO(s.read()) as f:

            count = read_u32le(f)
            self.next_free_key = read_u32le(f)
            self.last_free_key = read_u32le(f)

            pack_fmt = str("<%dI" % count)
            self.references = list(struct.unpack(pack_fmt, f.read(4 * count)))

    @writeonly
    def write_index(self):
        s = self.parent.dir.touch(self.index_name + " index").open(mode='rw')
        with BytesIO() as f:
            count = len(self.references)
            write_u32le(f, count)
            write_u32le(f, self.next_free_key)
            write_u32le(f, self.last_free_key)

            for local_key in self.references:
                write_u32le(f, local_key)

            s.write(f.getvalue())
            s.truncate()

    @property
    def ref_classdef(self):
        return self.typedef.element_typedef.ref_classdef

    def index_ref_name(self, index):
        return "%s{%x}" % (self.index_name, self.references[index])

    def get(self, index, default=None):
        if index >= len(self.references):
            return default

        if index < 0:
            index = max(0, len(self.references) + index)

        item = self.objects.get(index, None)
        if item:
            return item
        ref = self.index_ref_name(index)
        dir_entry = self.parent.dir.get(ref)
        item = self.parent.root.manager.read_object(dir_entry)

        self.objects[index] = item
        return item

    def __iter__(self):
        for i in range(len(self.references)):
            yield self.get(i)

    def __len__(self):
        return len(self.references)

    def __getitem__(self, index):
        item = self.get(index, sentinel)
        if item is sentinel:
            raise IndexError(index)
        return item

    @writeonly
    def __setitem__(self, index, value):
        if index < 0:
            index = max(0, len(self) + index)

        if index >= len(self):
            raise IndexError("StrongRefVectorProperty assignment index out of range")

        if value.root is not self.parent.root:
            raise AAFAttachError("Object is from a different root")

        if value.dir:
            raise AAFAttachError("Object already attached")

        obj = self.get(index, None)
        if obj:
            obj.detach()

        self.objects[index] = value
        self.attach()

    @writeonly
    def clear(self):
        for obj in self:
            obj.detach()

        self.next_free_key = 0
        self.references = []

        if self.attached:
            self.objects = weakref.WeakValueDictionary()
        else:
            self.objects = {}

    @writeonly
    def pop(self, index):
        obj = self.get(index, None)
        if obj is None:
            raise IndexError(index)
        if index < 0:
            index = max(0, len(self) + index)

        self.references.pop(index)

        # decrement all cached object with > index -1
        objects = {}
        for key, value in self.objects.items():
            if key == index:
                item = value
            elif key > index:
                objects[key-1] = value
            else:
                objects[key] = value

        if self.attached:
            self.objects = weakref.WeakValueDictionary(objects)
        else:
            self.objects = objects

        assert obj is item

        obj.detach()
        return obj

    @writeonly
    def insert(self, index, value):
        assert self.ref_classdef.isinstance(value.classdef)

        self.references.insert(index, self.next_free_key)

        objects = {}
        objects[index] = value
        # increment all cached object with > indices +1
        for key, value in self.objects.items():
            if key >= index:
                objects[key+1] = value
            else:
                objects[key] = value

        self.next_free_key += 1
        if self.attached:
            self.objects = weakref.WeakValueDictionary(objects)
        else:
            self.objects = objects
        self.attach()

    @writeonly
    def extend(self, value):
        index_name = self.index_name # sets self.data
        ref_classdef = self.ref_classdef

        for obj in value:
            assert ref_classdef.isinstance(obj.classdef)

            if obj.root is not self.parent.root:
                raise AAFAttachError("Object is from a different root")

            if obj.dir:
                raise AAFAttachError("Object already attached")

        for obj in value:
            i = len(self.references)
            self.references.append(self.next_free_key)
            self.objects[i] = obj
            self.next_free_key += 1

        self.add_pid_entry()
        self.attach()

    def append(self, value):
        self.extend([value])

    @property
    def value(self):
        return [item for item in self]

    @value.setter
    @writeonly
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        self.clear()
        self.extend(value)

    def detach(self):
        objects = {}
        for i, obj in enumerate(self):
            objects[i] = obj
        self.objects = objects

    def attach(self):

        if not self.parent.dir:
            return

        for i, obj in enumerate(self):
            ref = self.index_ref_name(i)

            dir_entry = self.parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = self.parent.dir.makedir(ref)
            if obj.dir != dir_entry:
                obj.attach(dir_entry)


    def __repr__(self):
        return "<%s %s to %s %d items>" % (self.name, self.__class__.__name__, str(self.index_name), len(self.references))


class StrongRefSetProperty(Property):
    __slots__ = ('references', 'index_name', 'next_free_key', 'last_free_key', 'key_pid', 'key_size', 'objects')
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StrongRefSetProperty, self).__init__(parent, pid, format, version)

        self.references = {}

        self.index_name = None

        self.next_free_key = 0
        self.last_free_key = 0xFFFFFFFF

        # Pid of the referenced objects unique_key
        self.key_pid = None
        self.key_size = None

        if self.attached:
            self.objects = weakref.WeakValueDictionary()
        else:
            self.objects = {}

    def copy(self, parent, pid, cache):
        p = super(StrongRefSetProperty, self).copy(parent, pid)

        if parent.root is self.parent.root:
            p.references = dict(self.references)
            p.next_free_key = self.next_free_key
            p.last_free_key = self.last_free_key
            p.key_size = self.key_size
            p.index_name = self.index_name
            p.key_pid = self.key_pid

            for key, value in self.items():
                ref = self.index_ref_name(key)
                dir_entry = None
                if parent.dir:
                    dir_entry = parent.dir.get(ref)
                    if dir_entry is None:
                        dir_entry = parent.dir.makedir(ref)
                p.objects[key] = value.copy(dir_entry)
        else:
            for value in self.values():
                c = value.copy(root=parent.root, classdef_cache=cache)
                p.append(c)

        return p

    def encode(self, data):
        return encode_utf16le(data)

    def decode(self):
        self.index_name = decode_utf16le(self.data)

    def read_index(self):
        index_name = self.index_name + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole of the index
        with BytesIO(s.read()) as f:

            count = read_u32le(f)
            self.next_free_key = read_u32le(f)
            self.last_free_key = read_u32le(f)
            self.key_pid = read_u16le(f)
            self.key_size = read_u8(f)
            assert self.key_size in (16, 32)

            fmt = ''.join((
                'I', # local_key
                'I', # ref_count
                '%ds' % self.key_size))

            index_fmt  = struct.Struct(str('<' + fmt * count))
            index_data = index_fmt.unpack(f.read())

            for i in range(count):
                index = i * 3

                local_key = index_data[index + 0]
                ref_count = index_data[index + 1]
                key       = index_data[index + 2]

                # not sure if ref count is actually used
                # doesn't appear to be
                assert ref_count == 1

                if self.key_size == 16:
                    key = AUID(bytes_le=key)
                else:
                    key = MobID(bytes_le=key)

                self.references[key] = local_key

    @writeonly
    def write_index(self):
        s = self.parent.dir.touch(self.index_name + " index").open(mode='rw')
        with BytesIO() as f:
            count = len(self.references)
            write_u32le(f, count)
            write_u32le(f, self.next_free_key)
            write_u32le(f, self.last_free_key)

            write_u16le(f, self.key_pid)
            write_u8(f, self.key_size)

            for key, local_key in self.references.items():
                write_u32le(f, local_key)
                write_u32le(f, 1)
                f.write(key.bytes_le)

            s.write(f.getvalue())
            s.truncate()

    def index_ref_name(self, key):
        return "%s{%x}" % (self.index_name, self.references[key])

    def read_object(self, key):

        obj = self.objects.get(key, None)
        if obj:
            return obj

        ref = self.index_ref_name(key)
        dir_entry = self.parent.dir.get(ref)
        obj = self.parent.root.manager.read_object(dir_entry)
        self.objects[key] = obj
        return obj

    def __contains__(self, key):
        return key in self.references

    def items(self):
        for key in self.references:
            obj = self.read_object(key)
            yield (key, obj)

    def values(self):
        for key, obj in self.items():
            yield obj

    def __iter__(self):
        return self.values()

    def __len__(self):
        return len(self.references)

    def get(self, key, default=None):
        if key not in self:
            return default
        return self.read_object(key)

    def __getitem__(self, key):
        result = self.get(key, default=sentinel)
        if result is sentinel:
            raise KeyError(key)
        return result

    @writeonly
    def swap_unique_key(self, old_key, new_key):
        obj = self.get(old_key)

        if obj is None:
            raise ValueError("invalid key: %s" % str(old_key))

        # remove reference
        self.objects.pop(old_key)
        local_key = self.references.pop(old_key)

        self.references[new_key] = local_key
        self.objects[new_key] = obj

        obj.unique_property.data = new_key.bytes_le

    @writeonly
    def extend(self, values):
        typedef = self.typedef
        classdef = typedef.ref_classdef

        # check values are the correct type
        for item in values:
            if not classdef.isinstance(item.classdef):
                raise TypeError("Invalid Value, expected {}, got {}".format(classdef, item.classdef))
            if item.root is not self.parent.root:
                raise AAFAttachError("Object is from a different root")
            if item.dir:
                raise AAFAttachError("Object already attached")

        if self.key_pid is None:
            self.key_pid = classdef.unique_key_pid
        if self.key_size is None:
            self.key_size = classdef.unique_key_size

        if self.index_name is None:
            propdef = self.propertydef
            self.index_name = mangle_name(propdef.property_name, self.pid, 32-10)
            self.data = self.encode(self.index_name)

        for item in values:
            key = item.unique_key
            assert key is not None

            current = self.objects.get(key, None)
            current_local_key = self.references.get(key, None)

            if current and current is not item:
                current.detach()

            if current_local_key is None:
                self.references[key] = self.next_free_key
                self.next_free_key += 1

            self.objects[key] = item

            if self.parent.dir:
                ref = self.index_ref_name(key)
                dir_entry = self.parent.dir.get(ref)
                if dir_entry is None:
                    dir_entry = self.parent.dir.makedir(ref)
                if item.dir != dir_entry:
                    item.attach(dir_entry)

        self.add_pid_entry()

    def append(self, value):
        self.extend([value])

    @writeonly
    def clear(self):
        for item in self.values():
            item.detach()
        self.references = {}
        if self.attached:
            self.objects = weakref.WeakValueDictionary()
        else:
            self.objects = {}
        self.next_free_key = 0

    @writeonly
    def pop(self, key):
        obj = self.get(key)
        if obj is None:
            raise KeyError(key)

        self.references.pop(key)
        self.objects.pop(key)

        obj.detach()

        return obj

    @property
    def value(self):
        return [item for item in self]

    @value.setter
    @writeonly
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        self.clear()
        if isinstance(value, dict):
            value = value.values()

        self.extend(value)
        return

    def detach(self):
        objects = {}
        for key, value in self.items():
            objects[key] = value
        self.objects = objects

    def attach(self):

        if not self.parent.dir:
            return

        for key in self.references:
            obj = self.objects.get(key, None)
            if not obj:
                continue
            ref = self.index_ref_name(key)
            dir_entry = self.parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = self.parent.dir.makedir(ref)
            if obj.dir != dir_entry:
                obj.attach(dir_entry)


    def __repr__(self):
        return "<%s to %s %d items>" % (self.__class__.__name__, str(self.index_name), len(self.references))


def resolve_weakref(p, ref):
    ref_class_id = p.ref_classdef.auid
    if ref_class_id == CLASSDEF_AUID:
        return p.parent.root.metadict.lookup_classdef(ref)
    elif ref_class_id == TYPEDEF_AUID:
        return p.parent.root.metadict.lookup_typedef(ref)
    else:
        return p.parent.root.resovle_weakref(p.weakref_index, p.key_pid, ref)

class WeakRefProperty(Property):
    __slots__ = ('weakref_index', 'key_pid', 'key_size', 'ref')
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(WeakRefProperty, self).__init__(parent, pid, format, version)
        self.weakref_index = None
        self.key_pid = None
        self.key_size = None
        self.ref = None

    def copy(self, parent, pid, cache):
        p = super(WeakRefProperty, self).copy(parent, pid)

        if parent.root is self.parent.root:
            p.weakref_index = self.weakref_index
            p.key_pid = self.pid
            p.key_size = self.key_size
            p.ref = self.ref
        else:
            weakref_index = parent.root.weakref_index(p.pid_path)
            ref_parent, target_property = parent.root.weakref_prop(weakref_index)

            # add property value if not present
            if self.ref not in target_property:
                v = self.value
                if self.ref_classdef.auid == CLASSDEF_AUID:
                    parent.root.metadict.register_external_classdef(v)
                if self.ref_classdef.auid == TYPEDEF_AUID:
                    parent.root.metadict.register_external_typedef(v)
                else:
                    c = v.copy(root=parent.root, classdef_cache=cache)
                    target_property.append(c)

            p.value = target_property[self.ref]

        return p

    def decode(self):
        with BytesIO(self.data) as f:
            self.weakref_index = read_u16le(f)
            self.key_pid = read_u16le(f)
            self.key_size = read_u8(f)
            assert self.key_size in (16, 32)
            if self.key_size == 16:
                self.ref = AUID(bytes_le=f.read(self.key_size))
            else:
                self.ref = key = MobID(bytes_le=f.read(self.key_size))

    def encode(self):
        with BytesIO() as f:
            ref = self.ref.bytes_le
            key_size = len(ref)
            assert key_size in (16, 32)

            write_u16le(f, self.weakref_index)
            write_u16le(f, self.key_pid)
            write_u8(f, key_size)
            f.write(ref)
            return f.getvalue()

    def __repr__(self):
        return "<%s %s index %s %s>" % (self.name, self.__class__.__name__, self.weakref_index, self.ref)

    @property
    def ref_classdef(self):
        return self.typedef.ref_classdef

    @property
    def value(self):
        return resolve_weakref(self, self.ref)

    @property
    def pid_path(self):
        return self.typedef.pid_path

    @value.setter
    @writeonly
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        ref_classdef = self.ref_classdef
        assert ref_classdef.isinstance(value.classdef)

        if value.root is not self.parent.root:
            raise AAFAttachError("Object is from a different root")

        if self.key_pid is None:
            self.key_pid = ref_classdef.unique_key_pid
        if self.key_size is None:
            self.key_size = ref_classdef.unique_key_size
        if self.weakref_index is None:
            self.weakref_index = self.parent.root.weakref_index(self.pid_path)

        self.ref = value.unique_key
        self.data = self.encode()
        self.add_pid_entry()


class WeakRefArrayProperty(Property):
    __slots__ = ('references', 'index_name', 'weakref_index', 'key_pid', 'key_size')
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(WeakRefArrayProperty, self).__init__(parent, pid, format, version)
        self.references = []
        self.index_name = None
        self.weakref_index = None
        self.key_pid = None
        self.key_size = None

    def copy(self, parent, pid, cache):
        p = super(WeakRefArrayProperty, self).copy(parent, pid)
        if parent.root is self.parent.root:
            p.references = list(self.references)
            p.index_name = self.index_name
            p.weakref_index = self.weakref_index
            p.key_pid = self.key_pid
            p.key_size = self.key_size
        else:
            weakref_index = parent.root.weakref_index(p.pid_path)
            ref_parent, target_property = parent.root.weakref_prop(weakref_index)
            for ref in self.references:
                # copy property here if not present?
                assert ref in target_property
                p.append(target_property[ref])

        return p

    def encode(self, data):
        return encode_utf16le(data)

    def decode(self):
        self.index_name = decode_utf16le(self.data)

    def read_index(self):
        index_name = self.index_name + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole index
        with BytesIO(s.read()) as f:

            count = read_u32le(f)
            self.weakref_index = read_u16le(f)
            self.key_pid = read_u16le(f)
            self.key_size = read_u8(f)
            assert self.key_size in (16, 32)

            for i in range(count):
                if self.key_size == 16:
                    key = AUID(bytes_le=f.read(self.key_size))
                else:
                    key = key = MobID(bytes_le=f.read(self.key_size))
                self.references.append(key)

    @writeonly
    def write_index(self):
        s = self.parent.dir.touch(self.index_name + " index").open(mode='rw')
        with BytesIO() as f:
            count = len(self.references)
            write_u32le(f, count)
            write_u16le(f, self.weakref_index)
            write_u16le(f, self.key_pid)
            write_u8(f, self.key_size)

            for item in self.references:
                f.write(item.bytes_le)

            s.write(f.getvalue())
            s.truncate()

    def __repr__(self):
        return "<%s %s to %d items>" % (self.name, self.__class__.__name__, len(self.references) )

    @property
    def ref_classdef(self):
        return self.typedef.element_typedef.ref_classdef

    @property
    def pid_path(self):
        return self.typedef.element_typedef.pid_path

    def __contains__(self, key):
        return key in self.references

    def __len__(self):
        return len(self.references)

    def __iter__(self):
        for ref in self.references:
            r = resolve_weakref(self, ref)
            yield r

    def get(self, key, default=None):
        if key not in self:
            return default
        return resolve_weakref(self, key)

    def __getitem__(self, key):
        result = self.get(key, default=sentinel)
        if result is sentinel:
            raise KeyError(key)
        return result

    def items(self):
        for key in self.references:
            obj = resolve_weakref(self, key)
            yield (key, obj)

    @writeonly
    def extend(self, values):
        ref_classdef = self.ref_classdef

        # check values are the correct type
        for item in values:
            if not ref_classdef.isinstance(item.classdef):
                raise TypeError("Invalid Value")
            if item.root is not self.parent.root:
                raise AAFAttachError("Object is from a different root")

        if self.index_name is None:
            propdef = self.propertydef
            self.index_name = mangle_name(propdef.property_name, self.pid, 32-10)
            self.data = self.encode(self.index_name)

        if self.weakref_index is None:
            self.weakref_index = self.parent.root.weakref_index(self.pid_path)
        if self.key_pid is None:
            self.key_pid = ref_classdef.unique_key_pid
        if self.key_size is None:
            self.key_size = ref_classdef.unique_key_size

        for item in values:
            self.references.append(item.unique_key)

        self.add_pid_entry()

    def append(self, value):
        self.extend([value])

    @writeonly
    def clear(self):
        self.references = []

    @property
    def value(self):
        return [item for item in self]

    @value.setter
    @writeonly
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        self.clear()
        self.extend(value)


class WeakRefVectorProperty(WeakRefArrayProperty):
    pass


class WeakRefSetProperty(WeakRefArrayProperty):
    pass


# haven't see aaf files that contain these yet
class WeakRefPropertyId(WeakRefProperty):
    pass


class UniqueIdProperty(Property):
    pass


class OpaqueStreamProperty(Property):
    pass

property_formats = {
SF_DATA                                    : Property,
SF_DATA_STREAM                             : StreamProperty,
SF_STRONG_OBJECT_REFERENCE                 : StrongRefProperty,
SF_STRONG_OBJECT_REFERENCE_VECTOR          : StrongRefVectorProperty,
SF_STRONG_OBJECT_REFERENCE_SET             : StrongRefSetProperty,
SF_WEAK_OBJECT_REFERENCE                   : WeakRefProperty,
SF_WEAK_OBJECT_REFERENCE_VECTOR            : WeakRefVectorProperty,
SF_WEAK_OBJECT_REFERENCE_SET               : WeakRefSetProperty,
SF_WEAK_OBJECT_REFERENCE_STORED_OBJECT_ID  : WeakRefPropertyId,
SF_UNIQUE_OBJECT_ID                        : UniqueIdProperty,
SF_OPAQUE_STREAM                           : OpaqueStreamProperty
}

def add_string_property(parent, pid, value):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    if value:
        p.data = encode_utf16le(value)
    parent.property_entries[pid] = p
    return p

def add_bool_property(parent, pid, value):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    if value:
        p.data = b"\x01"
    else:
        p.data = b"\x00"
    parent.property_entries[pid] = p
    return p

def add_u32le_property(parent, pid, value):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    if value is not None:
        p.data = encode_u32le(value)
    parent.property_entries[pid] = p
    return p

def add_u16le_property(parent, pid, value):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    if value is not None:
        p.data = encode_u16le(value)
    parent.property_entries[pid] = p
    return p

def add_u8_property(parent, pid, value):

    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    if value is not None:
        p.data = encode_u8(value)
    parent.property_entries[pid] = p
    return p

def add_auid_property(parent, pid, value):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)

    if value is None:
        value = AUID(int=0)
    elif not isinstance(value, AUID):
        value = AUID(value)

    p.data = value.bytes_le
    parent.property_entries[pid] = p
    return p

def add_auid_array_propertry(parent, pid, values):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    p.data = encode_auid_array(values)
    parent.property_entries[pid] = p
    return p

def add_utf16_array_property(parent, pid, values):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    p.data = encode_utf16_array(values)
    parent.property_entries[pid] = p
    return p

def add_s64le_array_property(parent, pid, values):
    p = Property(parent, pid, SF_DATA, PROPERTY_VERSION)
    p.data = b''
    for i in values:
        p.data += encode_s64le(i)
    parent.property_entries[pid] = p
    return p

def add_weakref_property(parent, pid, pid_path, key_pid, value):
    p = WeakRefProperty(parent, pid, SF_WEAK_OBJECT_REFERENCE, PROPERTY_VERSION)
    p.weakref_index = parent.root.weakref_index(pid_path)
    p.key_pid = key_pid
    p.key_size = 16
    if not isinstance(value, AUID):
        value = AUID(value)
    p.ref = value
    p.data = p.encode()

    parent.property_entries[pid] = p

    return p

def add_classdef_weakref_property(parent, pid, value):
    pid_path = [0x0001,  0x0003]
    return add_weakref_property(parent, pid , pid_path, 0x0005, value)

def add_typedef_weakref_property(parent, pid, value):
    pid_path = [0x0001,  0x0004]
    return add_weakref_property(parent, pid , pid_path, 0x0005, value)

def add_strongref_set_property(parent, pid, property_name, unique_pid, key_size=16):

    p = StrongRefSetProperty(parent, pid, SF_STRONG_OBJECT_REFERENCE_SET, PROPERTY_VERSION)
    name = mangle_name(property_name, pid, 32-10)
    p.index_name = name
    p.data = p.encode(name)

    p.key_pid = unique_pid
    p.key_size = key_size
    parent.property_entries[pid] = p

    return p

def add2set(self, pid, key, value):
    """low level add to StrongRefSetProperty"""
    prop = self.property_entries[pid]

    current = prop.objects.get(key, None)
    current_local_key = prop.references.get(key, None)

    if current and current is not value:
        current.detach()

    if current_local_key is None:
        prop.references[key] = prop.next_free_key
        prop.next_free_key += 1

    prop.objects[key] = value

    if prop.parent.dir:
        ref = prop.index_ref_name(key)
        dir_entry = prop.parent.dir.get(ref)
        if dir_entry is None:
            dir_entry = prop.parent.dir.makedir(ref)
        if value.dir != dir_entry:
            value.attach(dir_entry)
        prop.mark_modified()

def add_typedef_weakref_vector_property(parent, pid, property_name, values):
    # kAAFTypeID_TypeDefinitionWeakReferenceVector
    pid_path = [0x0001,  0x0004]
    key_pid = 0x0005
    p = WeakRefVectorProperty(parent, pid, SF_WEAK_OBJECT_REFERENCE_VECTOR, PROPERTY_VERSION)

    p.weakref_index = parent.root.weakref_index(pid_path)
    p.key_pid = key_pid
    p.key_size = 16

    p.index_name = mangle_name(property_name, pid, 32)
    p.data = p.encode(p.index_name)

    p.references = [AUID(v) for v in values]

    parent.property_entries[pid] = p
    return p
