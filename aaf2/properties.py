
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import uuid
from uuid import UUID
from io import BytesIO
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
from .exceptions import AAFPropertyError

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

class BaseProperty(object):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        self.parent = parent
        self.pid = pid
        self.format = format
        self.version = version
        self._data = None
        self._propertydef = None

    def format_name(self):
        return str(property_formats[self.format].__name__)

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
    def value(self, value):
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
        return "0x%04X %s" % (self.pid, self.format_name())


class Property(BaseProperty):
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
            return self.parent.dir.touch(self.stream_name).open(mode)

    @property
    def value(self):
        return self.parent.dir.get(self.stream_name)


# abtract for refereneces
class ObjectRefProperty(Property):
    pass

# abtract for referenece arrays
class ObjectRefArrayProperty(ObjectRefProperty):
    pass

class StrongRefProperty(ObjectRefProperty):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StrongRefProperty, self).__init__(parent, pid, format, version)
        self.ref = None
        self.object = None

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
        if dir_entry:
            self.object = self.parent.root.read_object(dir_entry)
        return self.object


    @value.setter
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

        self.object = value
        if not self.pid in self.parent.property_entries:
            self.parent.property_entries[self.pid] = self

        self.attach()

    def attach(self):
        if not self.object:
            return

        if not self.parent.dir:
            return

        dir_entry = self.parent.dir.get(self.ref)
        if dir_entry is None:
            dir_entry = self.parent.dir.makedir(self.ref)

        self.object.attach(dir_entry)


# abtract for referenece arrays
class StrongRefArrayProperty(ObjectRefArrayProperty):
    def encode(self, data):
        return data.encode("utf-16le") + b"\x00" + b"\x00"


class StrongRefVectorProperty(StrongRefArrayProperty):

    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StrongRefVectorProperty, self).__init__(parent, pid, format, version)
        self.references = []
        self._objects = []
        self.objects = []
        self.ref = None
        self.next_free_key = 0
        self.last_free_key = 0xFFFFFFFF
        self.local_map = {}

    def copy(self, parent):
        p = super(StrongRefVectorProperty, self).copy(parent)
        p.references = list(self.references)
        p.references = list(self.references)
        p.local_map =  dict(self.local_map)

        p.objects = []
        p.ref = self.ref
        p.next_free_key = self.next_free_key
        p.last_free_key = self.last_free_key

        for i, value in enumerate(self):
            ref = self.references[i]
            dir_entry = parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = parent.dir.makedir(ref)
            c = value.copy(dir_entry)
            p.objects.append(c)

        return p

    @property
    def objects(self):
        return self._objects

    @objects.setter
    def objects(self, value):
        assert isinstance(value, list)
        self._objects = value

    def decode(self):
        self.references = []
        self.ref = None
        #null terminated
        self.ref = self.data[:-2].decode("utf-16le")
        self.objects = []

        if not self.ref:
            return

    def read_index(self):
        index_name = self.ref + " index"
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
            ref = "%s{%x}" % (self.ref, local_key)
            # print(i, count, ref)
            self.local_map[ref] = local_key
            self.references.append(ref)

    def write_index(self):
        s = self.parent.dir.touch(self.ref + " index").open(mode='w')
        f = BytesIO()
        count = len(self.references)
        write_u32le(f, count)
        write_u32le(f, self.next_free_key)
        write_u32le(f, self.last_free_key)

        for ref in self.references:
            local_key = self.local_map[ref]
            write_u32le(f, local_key)

        s.write(f.getvalue())

    @property
    def ref_classdef(self):
        return self.typedef.element_typedef.ref_classdef

    def __iter__(self):
        for i, ref in enumerate(self.references):
            dir_entry = self.parent.dir.get(ref)
            item = self.parent.root.read_object(dir_entry)
            yield item

    def clear(self):
        for obj in self.objects:
            obj.detach()

        self.next_free_key = 0
        self.objects = []
        self.references = []
        self.local_map = {}


    def insert(self, index, value):
        # read all the objects inserting extending
        if len(self.objects) != len(self.references):
            self.objects = [item for item in self]

        ref_classdef = self.ref_classdef
        assert ref_classdef.isinstance(value.classdef)

        ref = "%s{%x}" % (self.ref, self.next_free_key)
        self.local_map[ref] = self.next_free_key
        self.references.insert(index, ref)
        self.objects.insert(index, value)
        self.next_free_key += 1

    def extend(self, value):
        # read all the objects before extending
        if len(self.objects) != len(self.references):
            self.objects = [item for item in self]

        ref_classdef = self.ref_classdef

        for obj in value:
            assert ref_classdef.isinstance(obj.classdef)

        if self.ref is None:
            propdef = self.propertydef
            self.ref = mangle_name(propdef.property_name, self.pid, 32-10)
            self.data = self.encode(self.ref)

        for obj in value:
            ref = "%s{%x}" % (self.ref, self.next_free_key)
            self.local_map[ref] = self.next_free_key
            self.references.append(ref)
            self.objects.append(obj)
            self.next_free_key += 1

        self.add_pid_entry()
        self.attach()

    def append(self, value):
        self.extend([value])

    @property
    def value(self):
        if len(self.objects) == len(self.references):
            return self.objects

        self.objects = [item for item in self]
        return self.objects

    @value.setter
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        self.clear()
        self.extend(value)

    def attach(self):
        # print("set attach")
        if not self.parent.dir:
            return

        for i, ref in enumerate(self.references):

            obj = self.objects[i]
            # print(ref)
            dir_entry = self.parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = self.parent.dir.makedir(ref)
            obj.attach(dir_entry)


    def __repr__(self):
        return "<%s %s to %s %d items>" % (self.name, self.__class__.__name__, str(self.ref), len(self.references))


class StrongRefSetProperty(StrongRefArrayProperty):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(StrongRefSetProperty, self).__init__(parent, pid, format, version)
        self.references = {}
        self.ref = None
        self.objects = {}
        self.local_map = {}
        self.next_free_key = 0
        self.last_free_key = 0xFFFFFFFF
        self.key_size = 16
        # this pid match the ref_pid on the weak ref
        self.index_pid = None

    def copy(self, parent):
        p = super(StrongRefSetProperty, self).copy(parent)

        p.local_map = dict(self.local_map)
        p.references = dict(self.references)
        p.next_free_key = self.next_free_key
        p.last_free_key = self.last_free_key
        p.key_size = self.key_size
        p.ref = self.ref
        p.objects = {}
        p.index_pid = self.index_pid

        for key, value in self.items():
            ref = self.references[key]
            dir_entry = parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = parent.dir.makedir(ref)
            p.objects[ref] = value.copy(dir_entry)

        return p

    def decode(self):
        self.references = {}
        self.ref = None
        self.ref = self.data[:-2].decode("utf-16le")
        self.objects = {}
        self.local_map = {}

    def read_index(self):
        index_name = self.ref + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole of the index
        f = BytesIO(s.read())

        count = read_u32le(f)
        self.next_free_key = read_u32le(f)
        self.last_free_key = read_u32le(f)
        self.index_pid = read_u16le(f)
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

            ref = "%s{%x}" % (self.ref, local_key)
            self.local_map[key] = local_key
            self.references[key] = ref

    def write_index(self):
        s = self.parent.dir.touch(self.ref + " index").open(mode='w')
        f = BytesIO()
        count = len(self.references)
        write_u32le(f, count)
        write_u32le(f, self.next_free_key)
        write_u32le(f, self.last_free_key)

        write_u16le(f, self.index_pid)
        write_u8(f, self.key_size)

        for key, value in self.references.items():
            local_key = self.local_map[key]
            write_u32le(f, local_key)
            write_u32le(f, 1)
            f.write(key.bytes_le)

        s.write(f.getvalue())

    def read_object(self, key):

        obj = self.objects.get(key, None)
        if not obj is None:
            return obj

        ref = self.references[key]

        dir_entry = self.parent.dir.get(ref)
        obj = self.parent.root.read_object(dir_entry)
        self.objects[key] = obj
        return obj

    def __contains__(self, item):
        return item in self.references

    def items(self):

        for key, ref in self.references.items():
            obj = self.read_object(key)
            yield (key, obj)

    def values(self):
        for key, obj in self.items():
            yield obj

    def __iter__(self):
        return self.values()

    def extend(self, values):
        typedef = self.typedef
        classdef = typedef.ref_classdef

        # check values are the correct type
        for item in values:
            if not classdef.isinstance(item.classdef):
                raise TypeError("Invalid Value")

        (self.index_pid, self.key_size) = self.parent.root.metadict.weakref_pid(self.parent.classdef, self.propertydef)

        if self.ref is None:
            propdef = self.propertydef
            self.ref = mangle_name(propdef.property_name, self.pid, 32-10)
            self.data = self.encode(self.ref)

        local_key = self.next_free_key

        for item in values:
            ref = "%s{%x}" % (self.ref, local_key)
            key = item.unique_key
            self.local_map[key] = local_key
            self.references[key] = ref
            self.objects[key] = item
            local_key += 1

        self.next_free_key = local_key

        self.add_pid_entry()
        self.attach()

    def append(self, value):
        self.extend([value])

    def clear(self):
        for item in self.objects.values():
            item.detach()
        self.references = {}
        self.objects = {}
        self.local_map = {}
        self.next_free_key = 0

    @property
    def value(self):

        if len(self.objects) == len(self.references):
            return self.objects
        d = {}
        for key, ref in self.items():
            d[key] = ref
        self.objects = d
        return d

    @value.setter
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        self.clear()
        if isinstance(value, dict):
            value = value.values()

        self.extend(value)
        return

    def attach(self):

        if not self.parent.dir:
            return

        for key, ref in self.references.items():
            obj = self.objects[key]
            dir_entry = self.parent.dir.get(ref)
            if dir_entry is None:
                dir_entry = self.parent.dir.makedir(ref)
            obj.attach(dir_entry)


    def __repr__(self):
        return "<%s to %s %d items>" % (self.__class__.__name__, str(self.ref), len(self.references))

def resolve_weakref(p, ref):
    ref_class_id = p.ref_classdef.uuid

    # classdef
    if ref_class_id   == UUID("0d010101-0101-0100-060e-2b3402060101"):
        return p.parent.root.metadict.lookup_classdef(ref)
    # typedef
    elif ref_class_id == UUID("0d010101-0203-0000-060e-2b3402060101"):
        return p.parent.root.metadict.lookup_typedef(ref)
    else:
        return p.parent.root.resovle_weakref(p.ref_index, p.ref_pid, p.ref)

class WeakRefProperty(ObjectRefProperty):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(WeakRefProperty, self).__init__(parent, pid, format, version)
        self.ref_index = None
        self.ref_pid = None
        self.id_size = None
        self.ref = None

    def copy(self, parent):
        p = super(WeakRefProperty, self).copy(parent)
        p.ref_index = self.ref_index
        p.ref_pid = self.pid
        p.id_size = self.id_size
        p.ref = self.id_size
        return p

    def decode(self):
        f = BytesIO(self.data)
        self.ref_index = read_u16le(f)
        self.ref_pid = read_u16le(f)
        self.id_size = read_u8(f)
        assert self.id_size in (16, 32)
        if self.id_size == 16:
            self.ref = UUID(bytes_le=f.read(self.id_size))
        else:
            self.ref = key = MobID(bytes_le=f.read(self.id_size))

    def encode(self):
        f = BytesIO()
        ref = self.ref.bytes_le
        id_size = len(ref)
        assert id_size in (16, 32)

        write_u16le(f, self.ref_index)
        write_u16le(f, self.ref_pid)
        write_u8(f, id_size)
        f.write(ref)
        return f.getvalue()

    def __repr__(self):
        return "<%s %s index %s %s>" % (self.name, self.__class__.__name__, self.ref_index, self.ref)

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
    def value(self, value):
        if value is None:
            self.remove_pid_entry()
            return

        ref_classdef = self.ref_classdef
        assert ref_classdef.isinstance(value.classdef)

        (self.ref_index, self.ref_pid, self.ref)  = self.parent.root.create_weakref(value, self.pid_path)

        self.data = self.encode()
        self.add_pid_entry()

class WeakRefArrayProperty(ObjectRefArrayProperty):
    def __init__(self, parent, pid, format, version=PROPERTY_VERSION):
        super(WeakRefArrayProperty, self).__init__(parent, pid, format, version)
        self.references = []
        self.ref = None
        self.ref_index = None
        self.ref_pid = None
        self.id_size = None

    def copy(self, parent):
        p = super(WeakRefArrayProperty, self).copy(parent)
        p.references = list(self.references)
        p.ref = self.ref
        p.ref_index = self.ref_index
        p.ref_pid = self.ref_pid
        p.id_size = self.id_size
        return p

    def decode(self):
        self.references = []
        #null terminated
        self.ref = self.data[:-2].decode("utf-16le")

    def read_index(self):
        index_name = self.ref + " index"
        index_dir = self.parent.dir.get(index_name)
        if not index_dir:
            raise AAFPropertyError("cannot find index stream: %s" % index_name)

        s = index_dir.open('r')
        # read the whole index
        f = BytesIO(s.read())

        count = read_u32le(f)
        self.ref_index = read_u16le(f)
        self.ref_pid = read_u16le(f)
        self.id_size = read_u8(f)
        assert self.id_size in (16, 32)

        for i in range(count):
            if self.id_size == 16:
                identification = UUID(bytes_le=f.read(self.id_size))
            else:
                identification = key = MobID(bytes_le=f.read(self.id_size))
            # print("  ",self.ref_index, identification)
            self.references.append(identification)

    def encode(self):
        return self.ref.encode("utf-16le") + b"\x00" + b"\x00"

    def write_index(self):
        s = self.parent.dir.touch(self.ref + " index").open(mode='w')
        f = BytesIO()
        count = len(self.references)
        write_u32le(f, count)
        write_u16le(f, self.ref_index)
        write_u16le(f, self.ref_pid)
        write_u8(f, self.id_size)

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

    @property
    def value(self):
        items = []
        for ref in self.references:
            r = resolve_weakref(self, ref)
            items.append(r)
        return items

    def extend(self, values):
        ref_classdef = self.ref_classdef

        # check values are the correct type
        for item in values:
            if not ref_classdef.isinstance(item.classdef):
                raise TypeError("Invalid Value")

        pid_path = self.pid_path

        if self.ref is None:
            propdef = self.propertydef
            self.ref = mangle_name(propdef.property_name, self.pid, 32)
            self.data = self.encode()

        for item in values:
            (ref_index, ref_pid, ref)  = self.parent.root.create_weakref(item, pid_path)
            if self.ref_index is None:
                self.ref_index = ref_index
            if self.ref_pid is None:
                self.ref_pid = ref_pid
            if self.id_size is None:
                self.id_size = len(ref.bytes_le)

            self.references.append(ref)

        self.add_pid_entry()

    def append(self, value):
        self.extend([value])

    def clear(self):
        self.references = []

    @value.setter
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
