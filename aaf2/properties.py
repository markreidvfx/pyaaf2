
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import uuid
from uuid import UUID
from io import BytesIO
import weakref
from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    write_u8,
    write_u16le,
    write_u32le,
    mangle_name,
    )
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
SF_WEAK_OBJECT_REFERENCE_STORED_OBJECT_ID = 0x03
SF_UNIQUE_OBJECT_ID                       = 0x86
SF_OPAQUE_STREAM                          = 0x40

# not sure about these
SF_DATA_VECTOR                            = 0xD2
SF_DATA_SET                               = 0xDA

PROPERTY_VERSION=32

def writeonly(func):
    def func_wrapper(self, *args, **kwargs):
        if not self.writeable:
            raise AAFPropertyError("file readonly")
        result = func(self, *args, **kwargs)
        if self.attached:
            self.parent.root.manager.add_modified(self.parent)
        return result

    return func_wrapper

class Property(object):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        self.pid = pid
        self.format = format
        self.version = version
        self._data = None
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

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def decode(self):
        pass

    @property
    def propertydef(self):
        if self._propertydef:
            return self._propertydef

        classdef = self.parent.classdef
        if classdef is None:
            return

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

    def copy(self, parent):
        p = self.__class__(parent, self.pid, self.format, version=PROPERTY_VERSION)
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
        if self._data is not None and self.parent.dir and self.unique:
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
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StreamProperty, self).__init__(parent, pid, format, version)
        self.stream_name = None

    def copy(self, parent):
        p = super(StreamProperty, self).copy(parent)
        p.stream_name = self.stream_name

        a = self.open('r')
        b = p.open("w")

        byte_size = a.dir.byte_size
        read_size = self.parent.root.cfb.sector_size

        # copy stream data
        while byte_size > 0:
            d = a.read(read_size)
            b.write(d)
            byte_size -= read_size

        return p

    def decode(self):
        # first byte is endianess
        assert self.data[0:1] == b'\x55' # unspecified
        self.stream_name = self.data[1:-2].decode("utf-16-le")

    def encode(self, data):
        return  b'\x55' + data.encode("utf-16le") + b"\x00" + b"\x00"

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
            stream = self.parent.dir.get(self.stream_name)
            if not stream:
                raise AAFPropertyError("cannot find stream: %s" % index_name)
            return stream.open(mode)
        else:
            if not self.writeable:
                raise AAFPropertyError("file readonly")

            return self.parent.dir.touch(self.stream_name).open(mode)

    @property
    def value(self):
        return self.parent.dir.get(self.stream_name)

class StrongRefProperty(Property):
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

    def copy(self, parent):
        p = super(StrongRefProperty, self).copy(parent)
        p.ref = self.ref

        dir_entry = parent.dir.get(p.ref)
        if dir_entry is None:
            dir_entry = parent.dir.makedir(p.ref)

        p.object = self.value.copy(dir_entry)
        return p

    def decode(self):
        #null terminated
        self.ref = self.data[:-2].decode("utf-16le")

    def encode(self, data):
        return data.encode("utf-16le") + b"\x00" + b"\x00"

    def __repr__(self):
        return "<%s %s to %s>" % (self.name, self.__class__.__name__, str(self.ref))

    @property
    def value(self):
        if self.object:
            return self.object
        dir_entry = self.parent.dir.get(self.ref)
        obj = None
        if dir_entry:
            obj = self.parent.root.read_object(dir_entry)
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

        if self.ref is None:
            propdef = self.propertydef
            self.ref = mangle_name(propdef.property_name, self.pid, 32)
            self.data = self.encode(self.ref)

        # before asigning new object detach old
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

    def copy(self, parent):
        p = super(StrongRefVectorProperty, self).copy(parent)
        p.references = list(self.references)

        p.objects = {}
        p.index_name = self.index_name
        p.next_free_key = self.next_free_key
        p.last_free_key = self.last_free_key
        p.data = self.data

        for i, value in enumerate(self):
            ref = self.index_ref_name(self.references[i])
            dir_entry = parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = parent.dir.makedir(ref)
            c = value.copy(dir_entry)
            p.objects[i] = c

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
        return data.encode("utf-16le") + b"\x00" + b"\x00"

    def decode(self):
        self.index_name = self.data[:-2].decode("utf-16le")

    def read_index(self):
        index_name = self.index_name + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole index
        f = BytesIO(s.read())

        count = read_u32le(f)
        self.next_free_key = read_u32le(f)
        self.last_free_key = read_u32le(f)

        for i in range(count):
            local_key = read_u32le(f)
            self.references.append(local_key)

    @writeonly
    def write_index(self):
        s = self.parent.dir.touch(self.index_name + " index").open(mode='w')
        f = BytesIO()
        count = len(self.references)
        write_u32le(f, count)
        write_u32le(f, self.next_free_key)
        write_u32le(f, self.last_free_key)

        for local_key in self.references:
            write_u32le(f, local_key)

        s.write(f.getvalue())

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
        item = self.parent.root.read_object(dir_entry)

        self.objects[index] = item
        return item

    def __iter__(self):
        for i in range(len(self.references)):
            yield self.get(i)

    def __len__(self):
        return len(self.references)

    def __getitem__(self, index):
        item = self.get(index, None)
        if item is None:
            raise IndexError(index)
        return item

    @writeonly
    def __setitem__(self, index, value):
        if index < 0:
            index = max(0, len(self) + index)

        if index >= len(self):
            raise IndexError("StrongRefVectorProperty assignment index out of range")

        if value.dir:
            raise AAFAttachError("object already attached")

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
            if obj.dir:
                raise AAFAttachError("object already attached")

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

    def copy(self, parent):
        p = super(StrongRefSetProperty, self).copy(parent)

        p.references = dict(self.references)
        p.next_free_key = self.next_free_key
        p.last_free_key = self.last_free_key
        p.key_size = self.key_size
        p.index_name = self.index_name
        p.key_pid = self.key_pid

        for key, value in self.items():
            ref = self.index_ref_name(key)
            dir_entry = parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = parent.dir.makedir(ref)
            p.objects[key] = value.copy(dir_entry)

        return p

    def encode(self, data):
        return data.encode("utf-16le") + b"\x00" + b"\x00"

    def decode(self):
        self.index_name = self.data[:-2].decode("utf-16le")

    def read_index(self):
        index_name = self.index_name + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole of the index
        f = BytesIO(s.read())

        count = read_u32le(f)
        self.next_free_key = read_u32le(f)
        self.last_free_key = read_u32le(f)
        self.key_pid = read_u16le(f)
        self.key_size = read_u8(f)
        assert self.key_size in (16, 32)

        for i in range(count):
            local_key = read_u32le(f)
            ref_count = read_u32le(f)

            # not sure if ref count is actually used
            # doesn't apear to be
            assert ref_count == 1

            if self.key_size == 16:
                key = UUID(bytes_le=f.read(self.key_size))
            else:
                key = MobID(bytes_le=f.read(self.key_size))

            self.references[key] = local_key

    @writeonly
    def write_index(self):
        s = self.parent.dir.touch(self.index_name + " index").open(mode='w')
        f = BytesIO()
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

    def index_ref_name(self, key):
        return "%s{%x}" % (self.index_name, self.references[key])

    def read_object(self, key):

        obj = self.objects.get(key, None)
        if obj:
            return obj

        ref = self.index_ref_name(key)
        dir_entry = self.parent.dir.get(ref)
        obj = self.parent.root.read_object(dir_entry)
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
        result = self.get(key, default=None)
        if result is None:
            raise KeyError(key)
        return result

    @writeonly
    def extend(self, values):
        typedef = self.typedef
        classdef = typedef.ref_classdef

        # check values are the correct type
        for item in values:
            if not classdef.isinstance(item.classdef):
                raise TypeError("Invalid Value")
            if item.dir:
                raise AAFAttachError("object already attached")

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
            self.references[key] = self.next_free_key
            current = self.objects.get(key, None)
            if current:
                current.detach()

            if self.parent.dir:
                ref = self.index_ref_name(key)
                dir_entry = self.parent.dir.get(ref)
                if dir_entry is None:
                    dir_entry = self.parent.dir.makedir(ref)
                if item.dir != dir_entry:
                    item.attach(dir_entry)

            self.objects[key] = item
            self.next_free_key += 1

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
        return list(self.values())

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
    ref_class_id = p.ref_classdef.uuid

    # classdef
    if ref_class_id   == UUID("0d010101-0101-0100-060e-2b3402060101"):
        return p.parent.root.metadict.lookup_classdef(ref)
    # typedef
    elif ref_class_id == UUID("0d010101-0203-0000-060e-2b3402060101"):
        return p.parent.root.metadict.lookup_typedef(ref)
    else:
        return p.parent.root.resovle_weakref(p.weakref_index, p.key_pid, ref)

class WeakRefProperty(Property):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(WeakRefProperty, self).__init__(parent, pid, format, version)
        self.weakref_index = None
        self.key_pid = None
        self.key_size = None
        self.ref = None

    def copy(self, parent):
        p = super(WeakRefProperty, self).copy(parent)
        p.weakref_index = self.weakref_index
        p.key_pid = self.pid
        p.key_size = self.key_size
        p.ref = self.ref
        return p

    def decode(self):
        f = BytesIO(self.data)
        self.weakref_index = read_u16le(f)
        self.key_pid = read_u16le(f)
        self.key_size = read_u8(f)
        assert self.key_size in (16, 32)
        if self.key_size == 16:
            self.ref = UUID(bytes_le=f.read(self.key_size))
        else:
            self.ref = key = MobID(bytes_le=f.read(self.key_size))

    def encode(self):
        f = BytesIO()
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
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(WeakRefArrayProperty, self).__init__(parent, pid, format, version)
        self.references = []
        self.index_name = None
        self.weakref_index = None
        self.key_pid = None
        self.key_size = None

    def copy(self, parent):
        p = super(WeakRefArrayProperty, self).copy(parent)
        p.references = list(self.references)
        p.index_name = self.index_name
        p.weakref_index = self.weakref_index
        p.key_pid = self.key_pid
        p.key_size = self.key_size
        return p

    def encode(self, data):
        return data.encode("utf-16le") + b"\x00" + b"\x00"

    def decode(self):
        self.index_name = self.data[:-2].decode("utf-16le")

    def read_index(self):
        index_name = self.index_name + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole index
        f = BytesIO(s.read())

        count = read_u32le(f)
        self.weakref_index = read_u16le(f)
        self.key_pid = read_u16le(f)
        self.key_size = read_u8(f)
        assert self.key_size in (16, 32)

        for i in range(count):
            if self.key_size == 16:
                key = UUID(bytes_le=f.read(self.key_size))
            else:
                key = key = MobID(bytes_le=f.read(self.key_size))
            self.references.append(key)

    def encode(self):
        return self.index_name.encode("utf-16le") + b"\x00" + b"\x00"

    @writeonly
    def write_index(self):
        s = self.parent.dir.touch(self.index_name + " index").open(mode='w')
        f = BytesIO()
        count = len(self.references)
        write_u32le(f, count)
        write_u16le(f, self.weakref_index)
        write_u16le(f, self.key_pid)
        write_u8(f, self.key_size)

        for item in self.references:
            f.write(item.bytes_le)

        s.write(f.getvalue())

    def __repr__(self):
        return "<%s %s to %d items>" % (self.name, self.__class__.__name__, len(self.references) )

    @property
    def ref_classdef(self):
        return self.typedef.element_typedef.ref_classdef

    @property
    def pid_path(self):
        return self.typedef.element_typedef.pid_path

    def __len__(self):
        return len(self.references)

    def __iter__(self):
        for ref in self.references:
            r = resolve_weakref(self, ref)
            yield r

    @writeonly
    def extend(self, values):
        ref_classdef = self.ref_classdef

        # check values are the correct type
        for item in values:
            if not ref_classdef.isinstance(item.classdef):
                raise TypeError("Invalid Value")

        if self.index_name is None:
            propdef = self.propertydef
            self.index_name = mangle_name(propdef.property_name, self.pid, 32)
            self.data = self.encode()

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
        items = []
        for item in self:
            items.append(item)
        return items

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
