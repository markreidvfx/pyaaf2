from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import traceback
from io import BytesIO
from .exceptions import AAFPropertyError
from . import types
from .model import classdefs
from .model import typedefs as base_typedefs
from . import properties

from . import core
from .utils import (register_class, read_u16le, decode_utf16le,
                    encode_utf16le, encode_u16le, str2uuid,
                    AAFClaseID_dict, AAFClassName_dict)

import uuid
from uuid import UUID

PID_NAME      = 0x0006
PID_UUID      = 0x0005
PID_TYPE      = 0x000B
PID_OPTIONAL  = 0x000C
PID_PID       = 0x000D
PID_UNIQUE    = 0x000E

PID_PARENT     = 0x0008
PID_PROPERTIES = 0x0009
PID_CONCRETE   = 0x000A

sentinel = object()

@register_class
class PropertyDef(core.AAFObject):
    class_id = UUID("0d010101-0202-0000-060e-2b3402060101")
    __slots__ = ('_typedef_id', '_uuid', '_property_name')

    def __new__(cls, root=None, name=None, uuid=None, pid=None, typedef=None, optional=None, unique=None):
        self = super(PropertyDef, cls).__new__(cls)
        self.root = root
        self._typedef_id = None
        self._uuid = None
        self._property_name = name
        if root:
            properties.add_string_property(self, PID_NAME, name)
            properties.add_bool_property(self, PID_OPTIONAL, optional)
            properties.add_bool_property(self, PID_UNIQUE, unique)
            properties.add_u16le_property(self, PID_PID, pid)
            properties.add_uuid_property(self, PID_UUID, uuid)
            properties.add_uuid_property(self, PID_TYPE, typedef)

        return self

    @property
    def property_name(self):
        if self._property_name:
            return self._property_name

        p = self.property_entries.get(PID_NAME)
        self._property_name = decode_utf16le(p.data)
        return self._property_name

    @property_name.setter
    def property_name(self, value):
       self.property_entries[PID_NAME].data = encode_utf16le(value)
       self._property_name = value

    @property
    def unique_key(self):
        return self.uuid

    @property
    def unique(self):
        if PID_UNIQUE in self.property_entries:
            return self.property_entries[PID_UNIQUE].data == b"\x01"
        return False

    @property
    def pid(self):
        return read_u16le(BytesIO(self.property_entries[PID_PID].data))

    @pid.setter
    def pid(self, value):
        self.property_entries[PID_PID].data = encode_u16le(value)

    @property
    def uuid(self):
        if self._uuid:
            return self._uuid
        p = self.property_entries.get(PID_UUID)
        self._uuid = UUID(bytes_le=p.data)
        return self._uuid

    @property
    def optional(self):
        return self.property_entries[PID_OPTIONAL].data == b"\x01"

    @property
    def typedef_id(self):
        if self._typedef_id:
            return self._typedef_id

        p = self.property_entries.get(PID_TYPE)
        self._typedef_id = UUID(bytes_le=p.data)
        return self._typedef_id

    @property
    def typedef(self):
        type_id = self.typedef_id
        if type_id:
            return self.root.metadict.lookup_typedef(type_id)

    @property
    def store_format(self):
        return self.typedef.store_format

    def __repr__(self):
        return "<%s PropertyDef" % self.property_name

@register_class
class ClassDef(core.AAFObject):
    class_id = UUID("0d010101-0201-0000-060e-2b3402060101")
    __slots__ = ('propertydef_by_pid')

    def __new__(cls, root=None, name=None, class_uuid=None, parent_uuid=None, concrete=None):
        self = super(ClassDef, cls).__new__(cls)
        self.root = root
        self.propertydef_by_pid = {}
        if root:
            properties.add_string_property(self, PID_NAME, name)
            properties.add_uuid_property(self, PID_UUID, class_uuid)
            properties.add_bool_property(self, PID_CONCRETE, concrete)

            # reference self uuid if no parent
            properties.add_classdef_weakref_property(self, PID_PARENT, parent_uuid or class_uuid)
            properties.add_strongref_set_property(self, PID_PROPERTIES, "Properties", PID_UUID)

        return self

    def __eq__(self, other):
        self.uuid == other.uuid

    @property
    def uuid(self):
        data = self.property_entries[PID_UUID].data
        if data is not None:
            return UUID(bytes_le=self.property_entries[PID_UUID].data)

    @property
    def concrete(self):
        return self.property_entries[PID_CONCRETE].data == b"\x01"

    @property
    def class_name(self):
        data = self.property_entries[PID_NAME].data
        if data is not None:
            return decode_utf16le(data)

    @property
    def unique_key(self):
        return self.uuid

    @property
    def unique_key_pid(self):
        for p in self.all_propertydefs():
            if p.unique:
                return p.pid

        # Parameter work around
        # Uses the DefinitionObject Identification PID
        if self.isinstance(self.root.metadict.lookup_classdef(UUID("0d010101-0101-3c00-060e-2b3402060101"))):
            return 0x1B01

    @property
    def unique_key_size(self):
        mob_classdef = self.root.metadict.lookup_classdef(UUID("0d010101-0101-3400-060e-2b3402060101"))
        essencedata_classdef = self.root.metadict.lookup_classdef(UUID("0d010101-0101-2300-060e-2b3402060101"))
        if self.isinstance(mob_classdef) or self.isinstance(essencedata_classdef):
            return 32
        return 16

    def isinstance(self, other):

        if self.uuid == other.uuid:
            return True

        for classdef in other.relatives():
            if classdef.uuid == self.uuid:
                return True
        return False

    @property
    def name(self):
        return "ClassDefinition"

    @property
    def classdef(self):
        return self.root.metadict.classdefs_by_name['ClassDefinition']

    @property
    def parent_id(self):
        if PID_PARENT in self.property_entries:
            return self.property_entries[PID_PARENT].ref

    @property
    def parent(self):
        parent_id = self.parent_id

        if parent_id == self.uuid:
            return None

        return self.root.metadict.classdefs_by_uuid.get(parent_id, None)

    @property
    def propertydefs(self):
        if PID_PROPERTIES in self.property_entries:
            return self.property_entries[PID_PROPERTIES].values()
        return []

    def register_propertydef(self, name, property_uuid, pid, typedef, optional, unique=False):

        typedef = str2uuid(typedef)
        property_uuid = str2uuid(property_uuid)
        if isinstance(typedef, UUID):
            typedef_uuid = typedef
        else:
            typedef = self.root.metadict.lookup_typedef(typedef)
            typedef_uuid = typedef.uuid

        # check its not already defined
        if property_uuid in self.property_entries[PID_PROPERTIES].references:
            return self.property_entries[PID_PROPERTIES].get(property_uuid)

        # None signifies Dynamically allocated Local Tags
        # I think this is similar to MXF where pids > 0x8000 < 0xFFFF
        # are extensions pids
        if pid is None:
            pid = self.root.metadict.next_free_pid()

        p = PropertyDef(self.root, name, property_uuid, pid, typedef_uuid, optional, unique)
        # # this is done low level to avoid recursion errors
        properties.add2set(self, PID_PROPERTIES, p.uuid, p)
        self.propertydef_by_pid[pid] = p
        return p

    def relatives(self):
        root = self
        while root:
            yield root
            root = root.parent

    def all_propertydefs(self):
        for classdef in self.relatives():

            if not classdef:
                break
                # raise Exception(self.class_name)

            for p in classdef.propertydefs:
                yield p

    def get_propertydef_from_pid(self, pid, default=None):

        for classdef in self.relatives():
            if not classdef:
                break
            p = classdef.propertydef_by_pid.get(pid, sentinel)

            if p is sentinel:
                 continue
            return p

        return default

    def __repr__(self):
        return "<%s %s>" % (self.class_name, "ClassDef")

root_classes = {
'Root' : ('b3b398a5-1c90-11d4-8053-080036210804', None, True, {
    "Header"              : ('0d010301-0102-0100-060e-2b3401010102', 0x0002, '05022800-0000-0000-060E-2B3401040101', False, False),
    "MetaDictionary"      : ('0d010301-0101-0100-060e-2b3401010102', 0x0001, '05022700-0000-0000-060E-2B3401040101', False, False),
})
}

root_types = {
"HeaderStrongRefence"             : ('05022800-0000-0000-060E-2B3401040101', "0d010101-0101-2f00-060e-2b3402060101"),
"MetaDictionaryStrongReference"   : ('05022700-0000-0000-060E-2B3401040101', "0d010101-0225-0000-060e-2b3402060101"),
}

PID_CLASSDEFS = 0x0003
PID_TYPEDEFS  = 0x0004

@register_class
class MetaDictionary(core.AAFObject):
    class_id = UUID("0d010101-0225-0000-060e-2b3402060101")
    def __init__(self, root):
        super(MetaDictionary, self).__init__(root)

        self.root = root
        properties.add_strongref_set_property(self, PID_CLASSDEFS, "ClassDefinitions", PID_UUID)
        properties.add_strongref_set_property(self, PID_TYPEDEFS, "TypeDefinitions", PID_UUID)

        self.classdefs_by_name = {}
        self.classdefs_by_uuid = {}
        self.typedefs_by_name = {}
        self.typedefs_by_uuid = {}

        self.typedefs_classes = {}

        self.local_pids = set()
        self.next_pid = 0xFFFF

        for name, args in root_classes.items():
            self.register_classdef(name, *args)

        for name, args in classdefs.classdefs.items():
            self.register_classdef(name, *args)

        for alias, name in classdefs.aliases.items():
            self.classdefs_by_name[alias]= self.classdefs_by_name[name]

        # setup typedefs
        self.register_typedef_model({'strongrefs': root_types})
        self.register_typedef_model(base_typedefs.__dict__)

    def register_typedef_model(self, typedef_model):

        for cat, classobj in types.categories.items():
            for name, args in typedef_model.get(cat, {}).items():

                if not isinstance(args, (tuple,list)):
                    args = [args]

                if cat == "extenums":
                    if name in self.typedefs_by_name:
                        t = self.typedefs_by_name[name]
                        for element_value, element_name in args[1].items():
                            t.register_element(element_name, UUID(element_value))
                    else:
                        t = types.TypeDefExtEnum(self.root, name, *args)
                        properties.add2set(self, PID_TYPEDEFS, t.uuid, t)
                elif cat == "enums":
                    if name in self.typedefs_by_name:
                        t = self.typedefs_by_name[name]
                        for element_value, element_name in args[2].items():
                            t.register_element(element_name, element_value)
                    else:
                        t = types.TypeDefEnum(self.root, name, *args)
                        properties.add2set(self, PID_TYPEDEFS, t.uuid, t)
                else:

                    t = classobj(self.root, name, *args)
                    properties.add2set(self, PID_TYPEDEFS, t.uuid, t)

                self.typedefs_by_name[name] = t
                self.typedefs_by_uuid[t.uuid] = t
                self.typedefs_classes[t.uuid] = t.__class__

    def register_extensions(self):
        from .model.ext import classdefs as ext_classdefs
        from .model.ext import typedefs as ext_typedefs

        for name, args in ext_classdefs.classdefs.items():
            self.register_classdef(name, *args)

        for alias, name in ext_classdefs.aliases.items():
            self.classdefs_by_name[alias]= self.classdefs_by_name[name]

        self.register_typedef_model(ext_typedefs.__dict__)

    def register_classdef(self, name, class_uuid, parent, concrete, propertydefs=None):
        if not isinstance(class_uuid, UUID):
            class_uuid = UUID(class_uuid)

        parent = str2uuid(parent)

        if parent is None:
            parent_uuid = None
        elif isinstance(parent, UUID):
            parent_uuid = parent
        else:
            parent_classdef = self.lookup_classdef(parent)
            parent_uuid = parent_classdef.uuid

        if name in self.classdefs_by_name:
            c = self.classdefs_by_name[name]
        elif class_uuid in self.classdefs_by_uuid:
            c = self.classdefs_by_name[class_uuid]
        else:
            c = ClassDef(self.root, name, class_uuid, parent_uuid, concrete)

        if propertydefs:
            for prop_name, prop_args in propertydefs.items():
                pid = prop_args[1]
                if pid and pid >= 0x8000:
                    assert pid not in self.local_pids
                    self.local_pids.add(pid)
                c.register_propertydef(prop_name, *prop_args)

        self.classdefs_by_name[name]   = c
        self.classdefs_by_uuid[c.uuid] = c

        # Root is not include in the data model for some reason
        if c.class_name != "Root":
            properties.add2set(self, PID_CLASSDEFS, c.uuid, c)
        return c

    def lookup_class(self, class_id):
        aaf_class = AAFClaseID_dict.get(class_id, None)
        if aaf_class:
            return aaf_class

        aaf_class = AAFClassName_dict.get(class_id, None)
        if aaf_class:
            return aaf_class

        aaf_class =  self.typedefs_classes.get(class_id, None)
        if aaf_class:
            return aaf_class

        return core.AAFObject

    def lookup_typedef(self, t):
        if isinstance(t, types.TypeDef):
            return t

        t = str2uuid(t)
        if isinstance(t, UUID):
            return self.typedefs_by_uuid.get(t, None)
        return self.typedefs_by_name.get(t, None)

    def lookup_classdef(self, t):
        if isinstance(t, ClassDef):
            return t
        t = str2uuid(t)
        if isinstance(t, UUID):
            return self.classdefs_by_uuid.get(t, None)
        return self.classdefs_by_name.get(t, None)

    @property
    def classdef(self):
        return self.classdefs_by_name['MetaDictionary']

    def next_free_pid(self):

        while self.next_pid in self.local_pids:
            self.next_pid -= 1
            if self.next_pid < 0x8000:
                raise ValueError("ran out of local pids")

        result = self.next_pid
        self.next_pid -= 1

        self.local_pids.add(result)
        return result


    def read_properties(self):
        super(MetaDictionary, self).read_properties()
        for key, typedef in self['TypeDefinitions'].items():
            self.typedefs_by_name[typedef.type_name] = typedef
            self.typedefs_by_uuid[typedef.uuid] = typedef

        # reset local pids
        self.local_pids = set()
        for key, classdef in self['ClassDefinitions'].items():
            self.classdefs_by_name[classdef.class_name] = classdef
            self.classdefs_by_uuid[classdef.uuid] = classdef
            propertydef_by_pid = {}
            for pdef in classdef['Properties'].values():
                if pdef.pid >= 0x8000:
                    self.local_pids.add(pdef.pid)

                propertydef_by_pid[pdef.pid] = pdef

            classdef.propertydef_by_pid = propertydef_by_pid


        # add typedefs not defined by file data model
        if self.root.writeable:
            for key, typedef in self.typedefs_by_uuid.items():
                # skip root typedefs
                if key in (UUID('05022800-0000-0000-060E-2B3401040101'),
                           UUID('05022700-0000-0000-060E-2B3401040101')):
                    # print("skipping root typedef")
                    continue

                if key not in self['TypeDefinitions']:
                    self['TypeDefinitions'].append(typedef)

        # add classdefs not defined by file data model
        if self.root.writeable:
            for key, classdef in self.classdefs_by_uuid.items():
                # skip root classdefs
                if key in (UUID('b3b398a5-1c90-11d4-8053-080036210804'), ):
                    # print("skipping root")
                    continue

                if key not in self['ClassDefinitions']:

                    # handle any conflicting dynamic pids
                    for pdef in classdef['Properties'].values():
                        if pdef.pid >= 0x8000:
                            if pdef.pid in self.local_pids:
                                pdef.pid = self.next_free_pid()

                    self['ClassDefinitions'].append(classdef)
