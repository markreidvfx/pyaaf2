
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from StringIO import StringIO
from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    )

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

class PropertyItem(object):
    def __init__(self, root, pid, format, version):
        self.root = root
        self.pid = pid
        self.format = format
        self.version = version

    def format_name(self):
        return str(property_formats[self.format].__name__)

    @property
    def propertydef(self):
        classdef = self.root.classdef
        if classdef is None:
            return

        for p in classdef.all_propertydefs():
            if p.pid == self.pid:
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

    @property
    def value(self):
        try:
            return self.typedef.decode(self.data)
        except:
            print("0x%x" % self.format)
            print(self)
            print(self.root.dir.path())
            raise


    def __repr__(self):
        return "0x%04X %s" % (self.pid, self.format_name())


class SFData(PropertyItem):
    def decode(self, data=None):
        self.data = data

    def __repr__(self):
        name = self.name
        if name:
            return "<%s %s>" % (name, str(self.typedef))
        else:
            return "<%s %d bytes>" % (self.__class__.__name__, len(self.data))

class SFStream(SFData):
    def decode(self, data=None):
        for i, c in enumerate(reversed(data)):
            if c != '\0':
                break

        self.stream_name = data[1:].decode("utf-16-le")

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.stream_name))

    @property
    def value(self):
        return self.root.dir.get(self.stream_name)


# abtract for refereneces
class SFObjectRef(SFData):
    pass

# abtract for referenece arrays
class SFObjectRefArray(SFObjectRef):
    pass

class SFStrongRef(SFObjectRef):
    def decode(self, data):
        #null terminated
        self.ref = data[:-2].decode("utf-16le")

    def __repr__(self):
        return "<%s %s to %s>" % (self.name, self.__class__.__name__, str(self.ref))

    @property
    def value(self):
        dir_entry = self.root.dir.get(self.ref)
        return self.root.root.read_object(dir_entry)

# abtract for referenece arrays
class SFStrongRefArray(SFObjectRefArray):
    pass

class SFStrongRefVector(SFStrongRefArray):
    def decode(self, data):
        self.references = []
        self.ref = None
        #null terminated
        self.ref = data[:-2].decode("utf-16le")
        self.objects = []

    # def read_index(self):
        if not self.ref:
            return

        index_name = self.ref + " index"
        index_dir = self.root.dir.get(index_name)
        if not index_dir:
            raise Exception()

        f = index_dir.open('r')
        count = read_u32le(f)
        next_free_key = read_u32le(f)
        last_free_key = read_u32le(f)

        for i in range(count):
            local_key = read_u32le(f)
            ref = "%s{%x}" % (self.ref, local_key)
            # print(i, count, ref)
            self.references.append(ref)

    @property
    def value(self):
        if self.objects:
            return self.objects

        references = []
        for ref in self.references:
            dir_entry = self.root.dir.get(ref)
            item = self.root.root.read_object(dir_entry)
            references.append(item)
        self.objects = references
        return references

    def __repr__(self):
        return "<%s %s to %s %d items>" % (self.name, self.__class__.__name__, str(self.ref), len(self.references))


class SFStrongRefSet(SFStrongRefArray):
    def decode(self, data):
        self.references = {}
        self.ref = None
        self.ref = data[:-2].decode("utf-16le")
        self.objects = {}

    # def read_index(self, dir_entry):
        if not self.ref:
            return

        index_name = self.ref + " index"
        index_dir = self.root.dir.get(index_name)
        if not index_dir:
            raise Exception()

        f = index_dir.open('r')
        count = read_u32le(f)
        next_free_key = read_u32le(f)
        last_free_key = read_u32le(f)
        pid = read_u16le(f)
        key_size = read_u8(f)

        # f = StringIO(f.read())

        for i in range(count):
            local_key = read_u32le(f)
            ref_count = read_u32le(f)

            key = f.read(key_size).encode("hex")
            ref = "%s{%x}" % (self.ref, local_key)

            # if ref_count > 1:
            # print("???", pid, ref_count, key, ref)

            self.references[key] = (ref, ref_count)

    def items(self):
        for key, (ref, ref_count) in self.references.items():
            dir_entry = self.root.dir.get(ref)
            yield (key, self.root.root.read_object(dir_entry))

    @property
    def value(self):

        if self.objects:
            return self.objects
        d = {}
        for key, ref in self.items():
            d[key] = ref
        self.objects = d
        return d

    def __repr__(self):
        return "<%s to %s %d items>" % (self.__class__.__name__, str(self.ref), len(self.references))

class SFWeakRef(SFObjectRef):
    def decode(self, data):

        f = StringIO(data)

        self.ref_index = read_u16le(f)
        self.ref_pid = read_u16le(f)
        self.id_size = id_size = read_u8(f)
        self.ref = f.read(self.id_size).encode("hex")

    def __repr__(self):
        return "<%s %s index %s %s>" % (self.name, self.__class__.__name__, self.ref_index, self.ref)

    @property
    def value(self):
        return self.root.root.resovle_weakref(self.ref_index, self.ref_pid, self.ref)

class SFWeakRefArray(SFObjectRefArray):
    def decode(self, data):
        self.references = []
        #null terminated
        self.ref = data[:-2].decode("utf-16le")

        index_name = self.ref + " index"
        index_dir = self.root.dir.get(index_name)
        if not index_dir:
            raise Exception()

        f = index_dir.open('r')
        count = read_u32le(f)
        self.ref_index = read_u16le(f)
        self.ref_pid = read_u16le(f)
        self.id_size = read_u8(f)
        # print(self.pid)
        for i in range(count):
            identification = f.read(self.id_size).encode("hex")
            # print("  ",self.ref_index, identification)
            self.references.append(identification)

    def __repr__(self):
        return "<%s %s to %d items>" % (self.name, self.__class__.__name__, len(self.references) )


    @property
    def value(self):
        items = []
        for ref in self.references:
            r = self.root.root.resovle_weakref(self.ref_index, self.ref_pid, ref)
            items.append(r)
        return items

class SFWeakRefVector(SFWeakRefArray):
    pass
class SFWeakRefSet(SFWeakRefArray):
    pass


# haven't see aaf files that contain these yet
class SFWeakRefId(SFWeakRef):
    pass

class SFUniqueId(SFData):
    pass

class SFOpaqueStream(SFData):
    pass

property_formats = {
SF_DATA                                    : SFData,
SF_DATA_STREAM                             : SFStream,
SF_STRONG_OBJECT_REFERENCE                 : SFStrongRef,
SF_STRONG_OBJECT_REFERENCE_VECTOR          : SFStrongRefVector,
SF_STRONG_OBJECT_REFERENCE_SET             : SFStrongRefSet,
SF_WEAK_OBJECT_REFERENCE                   : SFWeakRef,
SF_WEAK_OBJECT_REFERENCE_VECTOR            : SFWeakRefVector,
SF_WEAK_OBJECT_REFERENCE_SET               : SFWeakRefSet,
SF_WEAK_OBJECT_REFERENCE_STORED_OBJECT_ID  : SFWeakRefId,
SF_UNIQUE_OBJECT_ID                        : SFUniqueId,
SF_OPAQUE_STREAM                           : SFOpaqueStream
}
