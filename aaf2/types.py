# import aafobject

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
from . import core
from . import properties
from .mobid import MobID
from .fractions import AAFFraction

import datetime

from struct import (unpack, pack)

class TypeDef(core.AAFObject):
    def __init__(self, root, name=None, auid=None):
        super(TypeDef, self).__init__(root)
        self.typedef_auid = UUID("0d010101-0203-0000-060e-2b3402060101")
        self.root = root
        self.type_name = name
        self.auid = None
        if auid:
            self.auid = UUID(auid)
        self.format = properties.SF_DATA

    def __repr__(self):
        return "<%s %s>" % (self.type_name, self.__class__.__name__)

    def read_properties(self):
        super(TypeDef, self).read_properties()
        self.type_name = self['Name'].value
        self.auid = self['Identification'].value

class TypeDefInt(TypeDef):
    def __init__(self, root, name=None, auid=None, size=None, signed=None):
        super(TypeDefInt, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0204-0000-060e-2b3402060101")
        self.size = size
        self.signed = signed
    def read_properties(self):
        super(TypeDefInt, self).read_properties()
        self.size = self['Size'].value
        self.signed = self['IsSigned'].value

    @property
    def byte_size(self):
        return self.size

    def pack_format(self, elements=1):
        fmt = ""
        if self.size == 1:
            fmt = '%dB'
        elif self.size == 2:
            fmt = "<%dH"
        elif self.size == 4:
            fmt = "<%dI"
        elif self.size == 8:
            fmt = "<%dQ"
        else:
            raise Exception("unkown size %d" % self.size)
        fmt = fmt % elements
        if self.signed:
            fmt = fmt.lower()

        return fmt

    def decode(self, data):
        assert len(data) == self.size
        return unpack(self.pack_format(), data)[0]


class TypeDefStrongRef(TypeDef):
    def __init__(self, root, name=None, auid=None, classdef=None):
        super(TypeDefStrongRef, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0205-0000-060e-2b3402060101")
        self.ref_classdef = classdef
        self.format = properties.SF_STRONG_OBJECT_REFERENCE

class TypeDefWeakRef(TypeDef):
    def __init__(self, root, name=None, auid=None, classdef=None, path=None):
        super(TypeDefWeakRef, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0206-0000-060e-2b3402060101")
        self.ref_classdef = classdef
        self.path = path
        self.format = properties.SF_WEAK_OBJECT_REFERENCE

class TypeDefEnum(TypeDef):
    def __init__(self, root, name=None, auid=None, typedef=None, elements=None):
        super(TypeDefEnum, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0207-0000-060e-2b3402060101")
        self.element_typedef_name = typedef
        self.elements = elements

    @property
    def byte_size(self):
        return self.element_typedef.byte_size

    def read_properties(self):
        super(TypeDefEnum, self).read_properties()
        names = list(iter_utf16_array(self['ElementNames'].data))
        self.elements = dict(zip(self['ElementValues'].value, names))

    @property
    def element_typedef(self):
        if self.element_typedef_name:
            return self.root.metadict.lookup_typedef(self.element_typedef_name)
        return self['ElementType'].value

    def decode(self, data):

        # Boolean
        if self.auid == UUID("01040100-0000-0000-060e-2b3401040101"):
            return data == '\x01'

        typedef = self.element_typedef
        index = typedef.decode(data)
        return self.elements[index]

def iter_utf16_array(data):
    start = 0
    for i in range(0, len(data), 2):
        if data[i] == "\x00" and data[i+1] == "\x00":
            yield data[start:i].decode("utf-16le")
            start = i+2

class TypeDefFixedArray(TypeDef):
    def __init__(self, root, name=None, auid=None, typedef=None, size=None):
        super(TypeDefFixedArray, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0208-0000-060e-2b3402060101")
        self.member_typedef_name = typedef
        self.size = size

    @property
    def member_typedef(self):
        if not self.member_typedef_name:
            return self['ElementType'].value
        return self.root.metadict.lookup_typedef(self.member_typedef_name)

    @property
    def byte_size(self):
        return self.member_typedef.byte_size * self.size

    def decode(self, data):
        member_typedef = self.member_typedef

        if isinstance(member_typedef, TypeDefInt):
            size = member_typedef.size
            elements = len(data)//size
            fmt = member_typedef.pack_format(elements)
            return unpack(fmt, data)

        start = 0
        byte_size = member_typedef.byte_size
        result = []
        for i in range(self.size):
            end = start + byte_size
            result.append(member_typedef.decode(data[start:end]))
            start = end

        return result

    def read_properties(self):
        super(TypeDefFixedArray, self).read_properties()
        self.size = self['ElementCount'].value


class TypeDefVarArray(TypeDef):
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefVarArray, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0209-0000-060e-2b3402060101")
        self.member_typedef_name = typedef

    @property
    def member_typedef(self):
        if not self.member_typedef_name:
            return self['ElementType'].value
        return self.root.metadict.lookup_typedef(self.member_typedef_name)

    def decode(self, data):
        if self.member_typedef_name == "Character":
            return list(iter_utf16_array(data))

        member_typedef = self.member_typedef
        if isinstance(member_typedef, TypeDefInt):
            size = member_typedef.size
            elements = len(data)//size
            fmt = member_typedef.pack_format(elements)
            return unpack(fmt, data)

        byte_size = member_typedef.byte_size
        elements = len(data)//byte_size
        start = 0
        result = []
        for i in range(elements):
            end = start + byte_size
            result.append(member_typedef.decode(data[start:end]))
            start = end
        return result

    def read_properties(self):
        super(TypeDefVarArray, self).read_properties()

class TypeDefSet(TypeDef):
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefSet, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-020a-0000-060e-2b3402060101")
        self.member_typedef_name = typedef

    @property
    def member_typedef(self):
        if self.member_typedef_name:
            return self.root.metadict.lookup_typedef(self.member_typedef_name)

        return self['ElementType'].value

    def decode(self, data):

        typedef = self.member_typedef
        byte_size = typedef.byte_size
        count = len(data) // byte_size
        start = 0
        result = set()
        for i in range(count):
            end = start + byte_size
            v = typedef.decode(data[start:end])
            result.add(v)
            start = end

        return result

    def read_properties(self):
        super(TypeDefSet, self).read_properties()

class TypeDefString(TypeDef):
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefString, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-020b-0000-060e-2b3402060101")
        self.member_typedef_name = typedef

    def decode(self, data):
        return data[:-2].decode("utf-16le")

class TypeDefStream(TypeDef):

    def __init__(self, root, name=None, auid=None):
        super(TypeDefStream, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-020c-0000-060e-2b3402060101")
        self.format = properties.SF_DATA_STREAM

class TypeDefRecord(TypeDef):
    def __init__(self, root, name=None, auid=None, fields=None):
        super(TypeDefRecord, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-020d-0000-060e-2b3402060101")
        self._fields = fields

    @property
    def fields(self):
        if self._fields:
            return self._fields
        names = list(iter_utf16_array(self['MemberNames'].data))
        types = list(self['MemberTypes'].value)

        return zip(names, [t.type_name for t in types])

    @property
    def byte_size(self):

        size = 0
        for key, typedef_name in self.fields:
            typedef = self.root.metadict.typedefs_by_name[typedef_name]
            size += typedef.byte_size

        return size

    def decode(self, data):

        # MobID
        if self.auid == UUID("01030200-0000-0000-060e-2b3401040101"):
            mobid = MobID(bytes_le=data)
            assert str(mobid) == str(MobID(str(mobid)))
            return mobid

        # AUID
        if self.auid == UUID("01030100-0000-0000-060e-2b3401040101"):
            return UUID(bytes_le=data)

        start = 0
        result = {}

        for key, typedef_name in self.fields:
            typedef = self.root.metadict.lookup_typedef(typedef_name)

            end = start + typedef.byte_size
            result[key] = typedef.decode(data[start:end])
            start = end


        # TimeStruct
        if self.auid == UUID("03010600-0000-0000-060e-2b3401040101"):
            t = datetime.time(result['hour'],
                              result['minute'],
                              result['second'],
                              result['fraction'])
            return t

        # DateStruct
        if self.auid == UUID("03010500-0000-0000-060e-2b3401040101"):
            d = datetime.date(**result)
            return d

        # TimeStamp
        if self.auid == UUID("03010700-0000-0000-060e-2b3401040101"):
            d = datetime.datetime.combine(result['date'], result['time'])
            return d

        # Rational
        if self.auid == UUID("03010100-0000-0000-060e-2b3401040101"):
            r = AAFFraction(result['Numerator'], result['Denominator'])
            return r

        return result

    def read_properties(self):
        super(TypeDefRecord, self).read_properties()

class TypeDefRename(TypeDef):
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefRename, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-020e-0000-060e-2b3402060101")
        self.typedef_name = typedef

    @property
    def renamed_typedef(self):
        if self.typedef_name:
            return  self.root.metadict.lookup_typedef(typedef_name)
        return self['RenamedType'].value

    def decode(self, data):
        return self.renamed_typedef.decode(data)

    def read_properties(self):
        super(TypeDefRename, self).read_properties()


class TypeDefExtEnum(TypeDef):
    def __init__(self, root, name=None, auid=None, elements=None):
        super(TypeDefExtEnum, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0220-0000-060e-2b3402060101")
        self._elements = {}
        if elements:
            for key,value in elements.items():
                self._elements[UUID(key)] = value
    @property
    def elements(self):
        if self._elements:
            return self._elements

        names = list(iter_utf16_array(self['ElementNames'].data))
        keys = list(self['ElementValues'].value)
        return dict(zip(keys, names))


    def decode(self, data):
        v = UUID(bytes_le=data)
        return self.elements[v]

class TypeDefIndirect(TypeDef):
    def __init__(self, root, name=None, auid=None):
        super(TypeDefIndirect, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0221-0000-060e-2b3402060101")

    def decode(self, data):
        byte_order = data[0]
        assert byte_order == "\x4c" # little endian
        type_uuid = UUID(bytes_le=data[1:17])
        typedef = self.root.metadict.lookup_typedef(type_uuid)
        result = typedef.decode(data[17:])
        return result


class TypeDefOpaque(TypeDefIndirect):
    def __init__(self, root, name=None, auid=None):
        super(TypeDefOpaque, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0222-0000-060e-2b3402060101")

class TypeDefCharacter(TypeDef):
    def __init__(self, root, name=None, auid=None):
        super(TypeDefCharacter, self).__init__(root, name, auid)
        self.base_auid = UUID("0d010101-0223-0000-060e-2b3402060101")
