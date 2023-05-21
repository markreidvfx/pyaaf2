from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import sys
from uuid import UUID
from io import BytesIO

from . import core
from . import properties
from .mobid import MobID
from .rational import AAFRational
from .exceptions import AAFPropertyError
from .auid import AUID

import datetime
import logging

from struct import (unpack, pack)
from .utils import register_class, decode_utf16le, encode_utf16le, encode_utf16_array, encode_auid_array

if sys.version_info.major >= 3:
    unicode = str

PID_NAME      = 0x0006
PID_AUID      = 0x0005

@register_class
class TypeDef(core.AAFObject):
    class_id = AUID("0d010101-0203-0000-060e-2b3402060101")
    __slots__ = ('_auid')

    def __new__(cls, root=None, name=None, type_auid=None, *args, **kwargs):
        self = super(TypeDef, cls).__new__(cls)
        self.root = root
        self._auid = None
        if root:
            properties.add_string_property(self, PID_NAME, name)
            properties.add_auid_property(self, PID_AUID, type_auid)
        return self

    def copy(self, root=None):
        return self.__class__(root or self.root, self.name, self.auid)

    @property
    def unique_key(self):
        return self.auid

    @property
    def auid(self):
        if self._auid:
            return self._auid
        p = self.property_entries.get(PID_AUID)
        self._auid = AUID(bytes_le=p.data)
        return self._auid

    @property
    def uuid(self):
        return self.auid.uuid

    @property
    def type_name(self):
        data = self.property_entries[PID_NAME].data
        if data is not None:
            return decode_utf16le(data)

    @property
    def store_format(self):
        return properties.SF_DATA

    def __repr__(self):
        return "<%s %s>" % (self.type_name, self.__class__.__name__)

PID_INT_SIZE   = 0x000F
PID_INT_SIGNED = 0x0010

@register_class
class TypeDefInt(TypeDef):
    class_id = AUID("0d010101-0204-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, size=None, signed=None):
        self = super(TypeDefInt, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_u8_property(self, PID_INT_SIZE, size)
            properties.add_bool_property(self, PID_INT_SIGNED, signed)
        return self

    def copy(self, root=None):
        return TypeDefInt(root or self.root, self.name, self.auid, self.size, self.signed)

    @property
    def signed(self):
        return self.property_entries[PID_INT_SIGNED].data == b"\x01"

    @property
    def size(self):
        data  = self.property_entries[PID_INT_SIZE].data
        if data is not None:
            return unpack(b'B', data)[0]
        raise ValueError("%s No Size" % str(self.type_name))

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
            raise AAFPropertyError("unknown integer size: %d" % self.size)
        fmt = fmt % elements
        if self.signed:
            fmt = fmt.lower()

        return str(fmt)

    def decode(self, data):
        assert len(data) == self.size
        (result,) = unpack(self.pack_format(), data)
        return result

    def encode(self, value):
        return pack(self.pack_format(), value)


PID_STRONGREF_REF_TYPE = 0x0011

@register_class
class TypeDefStrongRef(TypeDef):
    class_id = AUID("0d010101-0205-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, classdef=None):
        self = super(TypeDefStrongRef, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_classdef_weakref_property(self, PID_STRONGREF_REF_TYPE, classdef)
        return self

    def copy(self, root=None):
        return TypeDefStrongRef(root or self.root, self.name, self.auid, self.ref_classdef.auid)

    @property
    def store_format(self):
        return properties.SF_STRONG_OBJECT_REFERENCE

    @property
    def ref_classdef(self):
        if PID_STRONGREF_REF_TYPE in self.property_entries:
             return self.root.metadict.lookup_classdef(self.property_entries[PID_STRONGREF_REF_TYPE].ref)

PID_WEAKREF_REF_TYPE   = 0x0012
PID_WEAKREF_TARGET_SET = 0x0013

@register_class
class TypeDefWeakRef(TypeDef):
    class_id = AUID("0d010101-0206-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, classdef=None, path=None):
        self = super(TypeDefWeakRef, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_classdef_weakref_property(self, PID_WEAKREF_REF_TYPE, classdef)
            properties.add_auid_array_propertry(self, PID_WEAKREF_TARGET_SET, path)

        return self

    def copy(self, root=None):
        return TypeDefWeakRef(root or self.root, self.name, self.auid, self.ref_classdef.auid, self.path)

    @property
    def store_format(self):
        return properties.SF_WEAK_OBJECT_REFERENCE

    @property
    def ref_classdef(self):
        if PID_WEAKREF_REF_TYPE in self.property_entries:
            return self.root.metadict.lookup_classdef(self.property_entries[PID_WEAKREF_REF_TYPE].ref)

    @property
    def path(self):
        return [p.name for c, p in self.propertydef_path]

    @property
    def pid_path(self):
        return [p.pid for c, p in self.propertydef_path]

    @property
    def target_set_path(self):
        return self['TargetSet'].value

    @property
    def propertydef_path(self):
        path = []
        classdef = self.root.metadict.lookup_classdef("Root")
        for p_auid in self.target_set_path:
            found = False
            for p in classdef.propertydefs:
                if p.auid == p_auid:
                    path.append((classdef, p))
                    classdef = p.typedef.ref_classdef
                    found = True
                    break
            if not found:
                raise AAFPropertyError("unable to resolve property path")

        return path

PID_ENUM_TYPE    = 0x0014
PID_ENUM_NAMES   = 0x0015
PID_ENUM_VALUES  = 0x0016

@register_class
class TypeDefEnum(TypeDef):
    class_id = AUID("0d010101-0207-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, typedef=None, elements=None):
        self = super(TypeDefEnum, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_typedef_weakref_property(self, PID_ENUM_TYPE, typedef)
            names = []
            values = []
            for val, name in elements.items():
                names.append(name)
                values.append(val)

            properties.add_utf16_array_property(self, PID_ENUM_NAMES, names)
            properties.add_s64le_array_property(self, PID_ENUM_VALUES, values)

        return self

    def copy(self, root=None):
        return TypeDefEnum(root or self.root, self.name, self.auid, self.element_typedef.auid, self.elements)

    @property
    def byte_size(self):
        return self.element_typedef.byte_size

    @property
    def elements(self):
        names = list(iter_utf16_array(self.property_entries[PID_ENUM_NAMES].data))
        element_count = len(names)
        fmt = b"<%dq" % element_count
        values = unpack(fmt, self.property_entries[PID_ENUM_VALUES].data)
        elements = dict(zip(values, names))
        return elements

    @property
    def element_typedef(self):
        if PID_ENUM_TYPE in self.property_entries:
            return self.root.metadict.lookup_typedef(self.property_entries[PID_ENUM_TYPE].ref)

    def register_element(self, element_name, element_value):
        names = []
        values = []
        for val, name in sorted(self.elements.items()):
            if val == element_value:
                return
            if name == element_name:
                return

            names.append(name)
            values.append(val)

        names.append(element_name)
        values.append(element_value)

        self.property_entries[PID_ENUM_NAMES].data = encode_utf16_array(names)
        fmt = b"<%dq" % len(values)
        self.property_entries[PID_ENUM_VALUES].data = pack(fmt, *values)

    def decode(self, data):

        # Boolean
        if self.auid == AUID("01040100-0000-0000-060e-2b3401040101"):
            return data == b'\x01'

        typedef = self.element_typedef
        index = typedef.decode(data)
        return self.elements[index]

    def encode(self, data):
        # Boolean
        if self.auid == AUID("01040100-0000-0000-060e-2b3401040101"):
            return b'\x01' if data else b'\x00'

        typedef = self.element_typedef
        for index, value in self.elements.items():
            if value == data:
                return typedef.encode(index)
            if index == data:
                return typedef.encode(index)

        raise AAFPropertyError("invalid enum: %s" % str(data))

def iter_utf16_array(data):
    start = 0
    data = bytearray(data)
    for i in range(0, len(data), 2):
        if data[i] == 0x00 and data[i+1] == 0x00:
            yield data[start:i].decode("utf-16le")
            start = i+2

PID_FIXED_TYPE  = 0x0017
PID_FIXED_COUNT = 0x0018

@register_class
class TypeDefFixedArray(TypeDef):
    class_id = AUID("0d010101-0208-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, typedef=None, size=None):
        self = super(TypeDefFixedArray, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_typedef_weakref_property(self, PID_FIXED_TYPE, typedef)
            properties.add_u32le_property(self, PID_FIXED_COUNT, size)
        return self

    def copy(self, root=None):
        return TypeDefFixedArray(root or self.root, self.name, self.auid, self.element_typedef.auid, self.size)

    @property
    def element_typedef(self):
        if PID_FIXED_TYPE in self.property_entries:
            return self.root.metadict.lookup_typedef(self.property_entries[PID_FIXED_TYPE].ref)

    @property
    def size(self):
        (result, ) = unpack(b'<I', self.property_entries[PID_FIXED_COUNT].data)
        return result

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

    def encode(self, data):
        element_typedef = self.element_typedef
        byte_size = element_typedef.byte_size
        element_count = self.size
        result = b""

        for i, item in enumerate(data):
            if i >= element_count:
                raise AAFPropertyError("too many elements for fixed array: expected %d elements" % element_count)
                break
            result += element_typedef.encode(item)

        # zero out remaining bytes
        if i < element_count:
            bytes_left = (element_count - i) * byte_size
            while bytes_left:
                result += b'\0'
                bytes_left -= 1

        return result

PID_VAR_TYPE = 0x0019

@register_class
class TypeDefVarArray(TypeDef):
    class_id = AUID("0d010101-0209-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, typedef=None):
        self = super(TypeDefVarArray, cls).__new__(cls, root, name, type_auid)

        if root:
            properties.add_typedef_weakref_property(self, PID_VAR_TYPE, typedef)
        return self

    def copy(self, root=None):
        return TypeDefVarArray(root or self.root, self.name, self.auid, self.element_typedef.auid)

    @property
    def store_format(self):
        if self.element_typedef.store_format == properties.SF_WEAK_OBJECT_REFERENCE:
            return properties.SF_WEAK_OBJECT_REFERENCE_VECTOR
        elif self.element_typedef.store_format == properties.SF_STRONG_OBJECT_REFERENCE:
            return properties.SF_STRONG_OBJECT_REFERENCE_VECTOR

        return super(TypeDefVarArray, self).store_format

    @property
    def element_typedef(self):
        if PID_VAR_TYPE in self.property_entries:
            return self.root.metadict.lookup_typedef(self.property_entries[PID_VAR_TYPE].ref)

    @property
    def ref_classdef(self):
        typedef = self.element_typedef
        return typedef.ref_classdef

    def decode(self, data):

        element_typedef = self.element_typedef

        #aafCharacter
        if element_typedef.auid == AUID("01100100-0000-0000-060e-2b3401040101"):
            return list(iter_utf16_array(data))


        if isinstance(element_typedef, TypeDefInt):
            size = element_typedef.size
            elements = len(data)//size
            fmt = element_typedef.pack_format(elements)
            return list(unpack(fmt, data))

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
            result += element_typedef.encode(item)

        return result

PID_SET_TYPE = 0x001A

@register_class
class TypeDefSet(TypeDef):
    class_id = AUID("0d010101-020a-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, typedef=None):
        self = super(TypeDefSet, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_typedef_weakref_property(self, PID_SET_TYPE, typedef)
        return self

    def copy(self, root=None):
        return TypeDefSet(root or self.root, self.name, self.auid, self.element_typedef)

    @property
    def element_typedef(self):
        if PID_SET_TYPE in self.property_entries:
            return self.root.metadict.lookup_typedef(self.property_entries[PID_SET_TYPE].ref)

    @property
    def ref_classdef(self):
        typedef = self.element_typedef
        return typedef.ref_classdef

    @property
    def store_format(self):
        if self.element_typedef.store_format == properties.SF_STRONG_OBJECT_REFERENCE:
            return properties.SF_STRONG_OBJECT_REFERENCE_SET
        elif self.element_typedef.store_format == properties.SF_WEAK_OBJECT_REFERENCE:
            return properties.SF_WEAK_OBJECT_REFERENCE_SET
        elif self.element_typedef.store_format == properties.SF_DATA:
            return properties.SF_DATA
        else:
            raise AAFPropertyError("unknown store format: 0x%x" % self.element_typedef.store_format)

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

    def encode(self, data):
        typedef = self.element_typedef

        set_data = set(data)
        result = b""
        for item in set_data:
            result += typedef.encode(item)

        return result

PID_STR_TYPE = 0x001B

@register_class
class TypeDefString(TypeDef):
    class_id = AUID("0d010101-020b-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, typedef=None):
        self = super(TypeDefString, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_typedef_weakref_property(self, PID_STR_TYPE, typedef)
        return self

    def copy(self, root=None):
        return TypeDefString(root or self.root, self.name, self.auid, self.element_typedef.auid)

    @property
    def element_typedef(self):
        if PID_STR_TYPE in self.property_entries:
            return self.root.metadict.lookup_typedef(self.property_entries[PID_STR_TYPE].ref)

    def decode(self, data):
        return decode_utf16le(data)

    def encode(self, data):
        return encode_utf16le(data)

@register_class
class TypeDefStream(TypeDef):
    class_id = AUID("0d010101-020c-0000-060e-2b3402060101")

    @property
    def store_format(self):
        return properties.SF_DATA_STREAM

PID_RECORD_TYPES = 0x001C
PID_RECORD_NAMES = 0x001D

MOBID_AUID      = AUID("01030200-0000-0000-060e-2b3401040101")
AUID_AUID       = AUID("01030100-0000-0000-060e-2b3401040101")
TIMESTRUCT_AUID = AUID("03010600-0000-0000-060e-2b3401040101")
DATESTRUCT_AUID = AUID("03010500-0000-0000-060e-2b3401040101")
TIMESTAMP_AUID  = AUID("03010700-0000-0000-060e-2b3401040101")
RATIONAL_AUID   = AUID("03010100-0000-0000-060e-2b3401040101")

@register_class
class TypeDefRecord(TypeDef):
    class_id = AUID("0d010101-020d-0000-060e-2b3402060101")
    __slots__ = ('_fields')

    def __new__(cls, root=None, name=None, type_auid=None, fields=None):
        self = super(TypeDefRecord, cls).__new__(cls, root, name, type_auid)
        if root:
            names = []
            types = []
            for name, val in fields:
                names.append(name)
                types.append(val)

            properties.add_utf16_array_property(self, PID_RECORD_NAMES, names)
            properties.add_typedef_weakref_vector_property(self, PID_RECORD_TYPES, 'MemberTypes', types)

        self._fields = None
        return self

    def copy(self, root=None):
        names = list(iter_utf16_array(self['MemberNames'].data))
        types = [typedef.auid for typedef in self['MemberTypes'].value]
        return TypeDefRecord(root or self.root, self.name, self.auid, zip(names, types))

    @property
    def member_names(self):
        return list(iter_utf16_array(self['MemberNames'].data))

    @property
    def member_types(self):
        return self['MemberTypes']

    @property
    def fields(self):
        if self._fields:
            return self._fields
        names = list(iter_utf16_array(self['MemberNames'].data))
        types = list(self['MemberTypes'].value)
        self._fields = list(zip(names, [t.type_name for t in types]))
        return self._fields

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
        if self.auid == MOBID_AUID:
            mobid = MobID(bytes_le=data)
            return mobid

        # AUID
        if self.auid == AUID_AUID:
            return AUID(bytes_le=data)

        start = 0
        result = {}

        for key, typedef_name in self.fields:
            typedef = self.root.metadict.lookup_typedef(typedef_name)

            end = start + typedef.byte_size
            result[key] = typedef.decode(data[start:end])
            start = end

        # NOTE: If datetime helpers raise exception record is returned as a dict

        # TimeStruct
        if self.auid == TIMESTRUCT_AUID:
            try:
                t = datetime.time(result['hour'],
                                result['minute'],
                                result['second'],
                                result['fraction'])
                return t
            except:
                logging.warning("unable to decode time: {}".format(result))

        # DateStruct
        if self.auid == DATESTRUCT_AUID:
            # aaf sdk struct says:
            # year   range -32,767 to +32767
            # month  range: 1-12, inclusive
            # day    range: 1-31, inclusive
            try:
                d = datetime.date(**result)
                return d
            except:
                logging.warning("unable to decode date: {}".format(result))

        # TimeStamp
        if self.auid == TIMESTAMP_AUID:
            if isinstance(result.get('date', {}), datetime.date):
                try:
                    d = datetime.datetime.combine(result['date'], result['time'])
                    return d
                except:
                    logging.warning("unable to decode timestamp: {}".format(result))

        # Rational
        if self.auid == RATIONAL_AUID:
            r = AAFRational(result['Numerator'], result['Denominator'])
            return r

        return result

    def encode(self, data):
        # MobID
        if self.auid == MOBID_AUID:
            return data.bytes_le

        # AUID
        if self.auid == AUID_AUID:
            return data.bytes_le

        result = b""
        # TimeStamp
        if self.auid == TIMESTAMP_AUID and isinstance(data, datetime.datetime):
            f = [self.root.metadict.lookup_typedef(t) for k, t in self.fields]
            #date
            result += f[0].encode(data.date())

            #time
            result += f[1].encode(data.time())
            return result


        # DateStruct
        if self.auid == DATESTRUCT_AUID and isinstance(data, datetime.date):
            d = {'year' : data.year,
                 'month' : data.month,
                 'day': data.day}
            # print (d)
            data = d

        # TimeStruct
        if self.auid == TIMESTRUCT_AUID and isinstance(data, datetime.time):
            t = {'hour' : data.hour,
                 'minute' : data.minute,
                 'second' : data.second,
                 'fraction' : 0 }
            # print(t)
            data = t

        # Rational
        if self.auid == RATIONAL_AUID:
            r = AAFRational(data)
            data = {'Numerator': r.numerator, 'Denominator':r.denominator }

        for key, typedef_name in self.fields:
            typedef = self.root.metadict.lookup_typedef(typedef_name)
            value = typedef.encode(data[key])
            result+=value

        return result

PID_RENAME_TYPE = 0x001E

@register_class
class TypeDefRename(TypeDef):
    class_id = AUID("0d010101-020e-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls,  root=None, name=None, type_auid=None, typedef=None):
        self = super(TypeDefRename, cls).__new__(cls, root, name, type_auid)
        if root:
            properties.add_typedef_weakref_property(self, PID_RENAME_TYPE, typedef)
        return self

    def copy(self, root=None):
        return TypeDefRename(root or self.root, self.name, self.auid, self.renamed_typedef.auid)

    @property
    def renamed_typedef(self):
        if PID_RENAME_TYPE in self.property_entries:
            return self.root.metadict.lookup_typedef(self.property_entries[PID_RENAME_TYPE].ref)

    def decode(self, data):
        return self.renamed_typedef.decode(data)

    def encode(self, data):
        return self.renamed_typedef.encode(data)

def iter_auid_array(data):
    with BytesIO(data) as f:
        result = []
        while True:
            d = f.read(16)
            if not d:
                break

            if len(d) == 16:
                yield AUID(bytes_le=d)
            else:
                raise Exception("auid length wrong: %d" % len(d))

PID_EXTENUM_NAMES  = 0x001f
PID_EXTENUM_VALUES = 0x0020

@register_class
class TypeDefExtEnum(TypeDef):
    class_id = AUID("0d010101-0220-0000-060e-2b3402060101")
    __slots__ = ()

    def __new__(cls, root=None, name=None, type_auid=None, elements=None):
        self = super(TypeDefExtEnum, cls).__new__(cls, root, name, type_auid)

        if root:
            names = []
            values = []
            for val, name in elements.items():
                values.append(val)
                names.append(name)

            properties.add_utf16_array_property(self, PID_EXTENUM_NAMES, names)
            properties.add_auid_array_propertry(self, PID_EXTENUM_VALUES, values)

        return self

    def copy(self, root=None):
        return TypeDefExtEnum(root or self.root, self.name, self.auid, self.elements)

    def register_element(self, element_name, element_auid):

        element_names = []
        element_values = []
        for val, name in self.elements.items():
            if val == element_auid:
                return
            if name == element_name:
                return

            element_values.append(val)
            element_names.append(name)

        element_names.append(element_name)
        element_values.append(element_auid)

        self.property_entries[PID_EXTENUM_NAMES].data = encode_utf16_array(element_names)
        self.property_entries[PID_EXTENUM_VALUES].data = encode_auid_array(element_values)

    @property
    def elements(self):
        element_names = list(iter_utf16_array(self.property_entries[PID_EXTENUM_NAMES].data))
        element_values = list(iter_auid_array(self.property_entries[PID_EXTENUM_VALUES].data))
        return dict(zip(element_values, element_names))

    def decode(self, data):
        if data is None:
            return None
        v = AUID(bytes_le=data)
        result = self.elements.get(v, None)
        if result is None:
            return v

        return result

    def encode(self, data):
        for key, value in self.elements.items():
            if isinstance(data, (AUID, UUID)):
                if data == key:
                    return key.bytes_le
            else:

                if value.lower() == data.lower():
                    return key.bytes_le

        raise ValueError("invalid ext enum value: %s" % str(data))

@register_class
class TypeDefIndirect(TypeDef):
    class_id = AUID("0d010101-0221-0000-060e-2b3402060101")
    __slots__ = ()

    def decode_typedef(self, data):
        byte_order = data[0:1]
        assert byte_order == b'\x4c' # little endian
        type_auid = AUID(bytes_le=data[1:17])
        return self.root.metadict.lookup_typedef(type_auid)

    def decode(self, data):
        typedef = self.decode_typedef(data)
        result = typedef.decode(data[17:])
        return result

    def encode(self, data, data_typedef=None):
        byte_order = b'\x4c'
        typedef = None
        if data_typedef is not None:
            typedef = self.root.metadict.lookup_typedef(data_typedef)
            if typedef is None:
                raise AAFPropertyError("unable to find typedef: %s" % (str(data_typedef)))
            type_auid = typedef.auid

        elif isinstance(data, (str, unicode)):
            # aafString
            type_auid = AUID("01100200-0000-0000-060e-2b3401040101")

        elif isinstance(data, AAFRational):
            # Rational
            type_auid = AUID("03010100-0000-0000-060e-2b3401040101")

        elif isinstance(data, int):
            # aafInt32
            type_auid = AUID("01010700-0000-0000-060e-2b3401040101")
        else:
            raise NotImplementedError("Indirect type for: %s", str(type(data)))

        if typedef is None:
            typedef = self.root.metadict.lookup_typedef(type_auid)
        result = byte_order
        result += type_auid.bytes_le
        result += typedef.encode(data)
        return result



@register_class
class TypeDefOpaque(TypeDefIndirect):
    class_id = AUID("0d010101-0222-0000-060e-2b3402060101")
    __slots__ = ()

@register_class
class TypeDefCharacter(TypeDef):
    class_id = AUID("0d010101-0223-0000-060e-2b3402060101")
    __slots__ = ()

@register_class
class TypeDefGenericCharacter(TypeDef):
    class_id = AUID("0e040101-0000-0000-060e-2b3402060101")
    def __new__(cls, root=None, name=None, type_auid=None, size=None):
        self = super(TypeDefGenericCharacter, cls).__new__(cls, root, name, type_auid)
        if root:
            # lookup pid
            classdef = root.metadict.lookup_classdef(AUID("0e040101-0000-0000-060e-2b3402060101"))

            dynamic_pid = None
            for pdef in classdef.all_propertydefs():
                if pdef.auid == AUID("0e040101-0101-0111-060e-2b3401010101"):
                    dynamic_pid = pdef.pid

            assert dynamic_pid
            # classdef
            properties.add_u8_property(self, dynamic_pid, size)

        return self

    def copy(self, root=None):
        return TypeDefGenericCharacter(root or self.root, self.name, self.auid, self.size)

    @property
    def size(self):
        classdef = self.root.metadict.lookup_classdef(self.class_id)
        dynamic_pid = None
        for pdef in classdef.all_propertydefs():
            if pdef.auid == AUID("0e040101-0101-0111-060e-2b3401010101"):
                dynamic_pid = pdef.pid

        assert dynamic_pid
        data = self.property_entries[dynamic_pid].data
        if data is not None:
            return unpack(b'B', data)[0]

        raise ValueError("%s No Size" % str(self.type_name))


categories = {
"ints"         : TypeDefInt,
"enums"        : TypeDefEnum,
"records"      : TypeDefRecord,
"fixed_arrays" : TypeDefFixedArray,
"var_arrays"   : TypeDefVarArray,
"renames"      : TypeDefRename,
"strings"      : TypeDefString,
"streams"      : TypeDefStream,
"opaques"      : TypeDefOpaque,
"extenums"     : TypeDefExtEnum,
"chars"        : TypeDefCharacter,
"generic_chars": TypeDefGenericCharacter,
"indirects"    : TypeDefIndirect,
"sets"         : TypeDefSet,
"strongrefs"   : TypeDefStrongRef,
"weakrefs"     : TypeDefWeakRef,
}
