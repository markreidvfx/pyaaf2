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
from .utils import register_class

@register_class
class TypeDef(core.AAFObject):
    class_id = UUID("0d010101-0203-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None):
        super(TypeDef, self).__init__(root)
        self.root = root
        self.type_name = name
        self.auid = None

        if auid:
            self.auid = UUID(auid)
        self.format = properties.SF_DATA

    @property
    def unique_key(self):
        return self.auid

    @property
    def store_format(self):
        return self.format

    def __repr__(self):
        return "<%s %s>" % (self.type_name, self.__class__.__name__)

    def read_properties(self):
        super(TypeDef, self).read_properties()
        self.type_name = self['Name'].value
        self.auid = self['Identification'].value

    def setup_defaults(self):
        self['Name'].value = self.type_name
        self['Identification'].value = self.auid

@register_class
class TypeDefInt(TypeDef):
    class_id = UUID("0d010101-0204-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, size=None, signed=None):
        super(TypeDefInt, self).__init__(root, name, auid)
        self.size = size
        self.signed = signed

    def setup_defaults(self):
        super(TypeDefInt, self).setup_defaults()
        self['Size'].value = self.size
        self['IsSigned'].value = self.signed

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

    def encode(self, value):
        return pack(self.pack_format(), value)

@register_class
class TypeDefStrongRef(TypeDef):
    class_id = UUID("0d010101-0205-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, classdef=None):
        super(TypeDefStrongRef, self).__init__(root, name, auid)
        self.ref_classdef_name = classdef

    def setup_defaults(self):
        super(TypeDefStrongRef, self).setup_defaults()
        self['ReferencedType'].value = self.ref_classdef

    @property
    def store_format(self):
        return properties.SF_STRONG_OBJECT_REFERENCE

    @property
    def ref_classdef(self):
        if self.ref_classdef_name:
            return self.root.metadict.lookup_classdef(self.ref_classdef_name)

        return self['ReferencedType'].value

@register_class
class TypeDefWeakRef(TypeDef):
    class_id = UUID("0d010101-0206-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, classdef=None, path=None):
        super(TypeDefWeakRef, self).__init__(root, name, auid)
        self.ref_classdef_name = classdef
        self._path = path
        self.format = properties.SF_WEAK_OBJECT_REFERENCE

    def setup_defaults(self):
        super(TypeDefWeakRef, self).setup_defaults()
        self['TargetSet'].value = self.target_set_path
        self['ReferencedType'].value = self.ref_classdef

    @property
    def ref_classdef(self):
        if self.ref_classdef_name:
            return self.root.metadict.lookup_classdef(self.ref_classdef_name)

        return self.root.metadict.lookup_classdef(self['ReferencedType'].ref)

    @property
    def target_set_path(self):
        if self._path:
            result = []
            # root = self.root.root
            classdef = self.root.metadict.lookup_classdef("Root")

            for p_name in self._path:
                found = False
                for p_def in classdef.propertydefs:
                    if p_def.property_name == p_name:
                        if p_def.uuid:
                            result.append(p_def.uuid)
                        classdef = p_def.typedef.ref_classdef
                        found = True
                        break
                if not found:
                    raise Exception()
            return result

        return self['TargetSet'].value

    @property
    def path(self):
        path = []
        classdef = self.root.metadict.lookup_classdef("Root")
        for auid in self.target_set_path:
            found = False
            for p in classdef.propertydefs:
                # print(p, p.uuid)
                if p.uuid == auid:
                    path.append(p.property_name)
                    classdef = p.typedef.ref_classdef
                    found = True
                    break
            if not found:
                raise Exception()

        return path

    @property
    def pid_path(self):
        path = []
        classdef = self.root.metadict.lookup_classdef("Root")
        for auid in self.target_set_path:
            found = False
            for p in classdef.propertydefs:
                # print(p, p.uuid)
                if p.uuid == auid:
                    path.append(p.pid)
                    classdef = p.typedef.ref_classdef
                    found = True
                    break
            if not found:
                raise Exception()

        return path

@register_class
class TypeDefEnum(TypeDef):
    class_id = UUID("0d010101-0207-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, typedef=None, elements=None):
        super(TypeDefEnum, self).__init__(root, name, auid)
        self.element_typedef_name = typedef
        self._elements = elements

    @property
    def byte_size(self):
        return self.element_typedef.byte_size

    @property
    def elements(self):
        if not self._elements:
            names = list(iter_utf16_array(self['ElementNames'].data))
            self._elements = dict(zip(self['ElementValues'].value, names))

        return self._elements

    def setup_defaults(self):
        super(TypeDefEnum, self).setup_defaults()
        names = []
        values = []
        for value, name in sorted(self.elements.items()):
            names.append(name)
            values.append(value)

        self['ElementNames'].add_pid_entry()
        self['ElementNames'].data = encode_utf16_array(names)
        self['ElementValues'].value = values
        self['ElementType'].value = self.element_typedef

    def read_properties(self):
        super(TypeDefEnum, self).read_properties()


    @property
    def element_typedef(self):
        if self.element_typedef_name:
            return self.root.metadict.lookup_typedef(self.element_typedef_name)
        return self['ElementType'].value

    def decode(self, data):

        # Boolean
        if self.auid == UUID("01040100-0000-0000-060e-2b3401040101"):
            return data == b'\x01'

        typedef = self.element_typedef
        index = typedef.decode(data)
        return self.elements[index]

    def encode(self, data):
        # Boolean
        if self.auid == UUID("01040100-0000-0000-060e-2b3401040101"):
            return b'\x01' if data else b'\x00'

        typedef = self.element_typedef
        for index, value in self.elements.items():
            if value == data:
                return typedef.encode(index)

        raise Exception("invalid enum")

def iter_utf16_array(data):
    start = 0
    data = bytearray(data)
    for i in range(0, len(data), 2):
        if data[i] == 0x00 and data[i+1] == 0x00:
            yield data[start:i].decode("utf-16le")
            start = i+2

def encode_utf16_array(data):
    result = b""
    for item in data:
        result += item.encode("utf-16le") + b"\x00" + b"\x00"
    return result

@register_class
class TypeDefFixedArray(TypeDef):
    class_id = UUID("0d010101-0208-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, typedef=None, size=None):
        super(TypeDefFixedArray, self).__init__(root, name, auid)
        self.member_typedef_name = typedef
        self.size = size

    def setup_defaults(self):
        super(TypeDefFixedArray, self).setup_defaults()
        self['ElementCount'].value = self.size
        self['ElementType'].value = self.element_typedef

    @property
    def element_typedef(self):
        if not self.member_typedef_name:
            return self['ElementType'].value
        return self.root.metadict.lookup_typedef(self.member_typedef_name)

    @property
    def byte_size(self):
        return self.element_typedef.byte_size * self.size

    def decode(self, data):
        element_typedef = self.element_typedef

        if isinstance(element_typedef, TypeDefInt):
            size = element_typedef.size
            elements = len(data)//size
            fmt = element_typedef.pack_format(elements)
            return unpack(fmt, data)

        start = 0
        byte_size = element_typedef.byte_size
        result = []
        for i in range(self.size):
            end = start + byte_size
            result.append(element_typedef.decode(data[start:end]))
            start = end

        return result

    def read_properties(self):
        super(TypeDefFixedArray, self).read_properties()
        self.size = self['ElementCount'].value

@register_class
class TypeDefVarArray(TypeDef):
    class_id = UUID("0d010101-0209-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefVarArray, self).__init__(root, name, auid)
        self.element_typedef_name = typedef

    def setup_defaults(self):
        super(TypeDefVarArray, self).setup_defaults()
        self['ElementType'].value = self.element_typedef

    @property
    def store_format(self):
        if self.element_typedef.store_format == properties.SF_WEAK_OBJECT_REFERENCE:
            return properties.SF_WEAK_OBJECT_REFERENCE_VECTOR
        elif self.element_typedef.store_format == properties.SF_STRONG_OBJECT_REFERENCE:
            return properties.SF_STRONG_OBJECT_REFERENCE_VECTOR

        return super(TypeDefVarArray, self).store_format

    @property
    def element_typedef(self):
        if not self.element_typedef_name:
            return self['ElementType'].value
        return self.root.metadict.lookup_typedef(self.element_typedef_name)

    def decode(self, data):

        element_typedef = self.element_typedef

        if element_typedef.type_name == "Character":
            return list(iter_utf16_array(data))


        if isinstance(element_typedef, TypeDefInt):
            size = element_typedef.size
            elements = len(data)//size
            fmt = element_typedef.pack_format(elements)
            return unpack(fmt, data)

        byte_size = element_typedef.byte_size
        elements = len(data)//byte_size
        start = 0
        result = []
        for i in range(elements):
            end = start + byte_size
            result.append(element_typedef.decode(data[start:end]))
            start = end
        return result

    def encode(self, value):

        element_typedef = self.element_typedef

        if element_typedef.type_name == "Character":
            return encode_utf16_array(value)

        if isinstance(element_typedef, TypeDefInt):

            elements = len(value)
            fmt = element_typedef.pack_format(elements)
            return pack(fmt, *value)

        result = b''

        for item in value:
            # print(member_typedef)
            result += element_typedef.encode(item)

        return result
        # raise Exception()

    def read_properties(self):
        super(TypeDefVarArray, self).read_properties()

@register_class
class TypeDefSet(TypeDef):
    class_id = UUID("0d010101-020a-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefSet, self).__init__(root, name, auid)
        self.element_typedef_name = typedef

    def setup_defaults(self):
        super(TypeDefSet, self).setup_defaults()
        self['ElementType'].value = self.element_typedef

    @property
    def element_typedef(self):
        if self.element_typedef_name:
            return self.root.metadict.lookup_typedef(self.element_typedef_name)

        return self['ElementType'].value

    @property
    def ref_classdef(self):
        typedef = self.element_typedef
        return typedef.ref_classdef

    @property
    def store_format(self):
        if self.element_typedef.store_format == properties.SF_STRONG_OBJECT_REFERENCE:
            return properties.SF_STRONG_OBJECT_REFERENCE_SET

    def decode(self, data):

        typedef = self.element_typedef
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

@register_class
class TypeDefString(TypeDef):
    class_id = UUID("0d010101-020b-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefString, self).__init__(root, name, auid)
        self.element_typedef_name = typedef

    def setup_defaults(self):
        super(TypeDefString, self).setup_defaults()
        self['ElementType'].value = self.element_typedef

    @property
    def element_typedef(self):
        if self.element_typedef_name:
            return self.root.metadict.lookup_typedef(self.element_typedef_name)
        return self['ElementType'].value


    def decode(self, data):
        return data[:-2].decode("utf-16le")

    def encode(self, data):
        return data.encode("utf-16le") + b'\x00' + b'\x00'

@register_class
class TypeDefStream(TypeDef):
    class_id = UUID("0d010101-020c-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None):
        super(TypeDefStream, self).__init__(root, name, auid)
        self.format = properties.SF_DATA_STREAM

@register_class
class TypeDefRecord(TypeDef):
    class_id = UUID("0d010101-020d-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, fields=None):
        super(TypeDefRecord, self).__init__(root, name, auid)
        self._fields = fields

    @property
    def fields(self):
        if self._fields:
            return self._fields
        names = list(iter_utf16_array(self['MemberNames'].data))
        types = list(self['MemberTypes'].value)
        self._fields = list(zip(names, [t.type_name for t in types]))
        return self._fields

    def setup_defaults(self):
        super(TypeDefRecord, self).setup_defaults()
        member_names = []
        member_types = []
        for name, typedef_name in self.fields:
            typedef = self.root.metadict.typedefs_by_name[typedef_name]
            member_names.append(name)
            member_types.append(typedef)

        self['MemberNames'].add_pid_entry()
        self['MemberNames'].data = encode_utf16_array(member_names)
        self['MemberTypes'].value = member_types

    @property
    def byte_size(self):
        size = 0
        for key, typedef_name in self.fields:
            typedef = self.root.metadict.typedefs_by_name[typedef_name]
            size += typedef.byte_size
        if size == 0:
            print("!!", self['MemberTypes'].value, list(iter_utf16_array(self['MemberNames'].data)))

        assert size != 0

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

    def encode(self, data):
        # MobID
        if self.auid == UUID("01030200-0000-0000-060e-2b3401040101"):
            return data.bytes_le

        # AUID
        if self.auid == UUID("01030100-0000-0000-060e-2b3401040101"):
            return data.bytes_le

        result = b""
        # TimeStamp
        if self.auid == UUID("03010700-0000-0000-060e-2b3401040101"):
            assert isinstance(data, datetime.datetime)
            f = [self.root.metadict.lookup_typedef(t) for k, t in self.fields]
            #date
            result += f[0].encode(data.date())

            #time
            result += f[1].encode(data.time())
            return result


        # DateStruct
        if self.auid == UUID("03010500-0000-0000-060e-2b3401040101"):
            assert isinstance(data, datetime.date)
            d = {'year' : data.year,
                 'month' : data.month,
                 'day': data.day}
            # print (d)
            data = d

        # TimeStruct
        if self.auid == UUID("03010600-0000-0000-060e-2b3401040101"):
            assert isinstance(data, datetime.time)
            t = {'hour' : data.hour,
                 'minute' : data.minute,
                 'second' : data.second,
                 'fraction' : 0 }
            # print(t)
            data = t

        for key, typedef_name in self.fields:
            typedef = self.root.metadict.lookup_typedef(typedef_name)
            value = typedef.encode(data[key])
            result+=value

        return result

    def read_properties(self):
        super(TypeDefRecord, self).read_properties()

@register_class
class TypeDefRename(TypeDef):
    class_id = UUID("0d010101-020e-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, typedef=None):
        super(TypeDefRename, self).__init__(root, name, auid)
        self.typedef_name = typedef

    def setup_defaults(self):
        super(TypeDefRename, self).setup_defaults()
        self['RenamedType'].value = self.renamed_typedef

    @property
    def renamed_typedef(self):
        if self.typedef_name:
            return self.root.metadict.lookup_typedef(self.typedef_name)
        return self['RenamedType'].value

    def decode(self, data):
        return self.renamed_typedef.decode(data)

    def read_properties(self):
        super(TypeDefRename, self).read_properties()

@register_class
class TypeDefExtEnum(TypeDef):
    class_id = UUID("0d010101-0220-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None, elements=None):
        super(TypeDefExtEnum, self).__init__(root, name, auid)
        self._elements = {}
        if elements:
            for key,value in elements.items():
                self._elements[UUID(key)] = value

    def setup_defaults(self):
        super(TypeDefExtEnum, self).setup_defaults()

        names = []
        keys = []
        for key, name in self.elements.items():
            keys.append(key)
            names.append(name)

        self['ElementNames'].add_pid_entry()
        self['ElementNames'].data = encode_utf16_array(names)
        self['ElementValues'].value = keys


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

@register_class
class TypeDefIndirect(TypeDef):
    class_id = UUID("0d010101-0221-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None):
        super(TypeDefIndirect, self).__init__(root, name, auid)

    def decode(self, data):
        byte_order = data[0:1]
        assert byte_order == b'\x4c' # little endian
        type_uuid = UUID(bytes_le=data[1:17])
        typedef = self.root.metadict.lookup_typedef(type_uuid)
        result = typedef.decode(data[17:])
        return result


@register_class
class TypeDefOpaque(TypeDefIndirect):
    class_id = UUID("0d010101-0222-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None):
        super(TypeDefOpaque, self).__init__(root, name, auid)

@register_class
class TypeDefCharacter(TypeDef):
    class_id = UUID("0d010101-0223-0000-060e-2b3402060101")
    def __init__(self, root, name=None, auid=None):
        super(TypeDefCharacter, self).__init__(root, name, auid)
