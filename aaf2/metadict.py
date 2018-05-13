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
from .model import typedefs

from . import core
from .utils import (register_class, read_u16le, decode_utf16le, AAFClaseID_dict, AAFClassName_dict)

import uuid
from uuid import UUID

@register_class
class PropertyDef(core.AAFObject):
    class_id = UUID("0d010101-0202-0000-060e-2b3402060101")

    def __new__(cls, root=None, name=None, uuid=None, pid=None, typedef=None, optional=None, unique=None):
        self = super(PropertyDef, cls).__new__(cls)

        self.root = root
        self.property_name = name
        self.uuid = None
        if uuid:
            self.uuid = UUID(uuid)
        self.pid = pid
        self.typedef_name = typedef
        self.optional = optional
        self._unique = unique

        return self

    @property
    def unique_key(self):
        return self.uuid

    @property
    def unique(self):
        if self._unique is not None:
            return self._unique
        return False

    @property
    def typedef(self):
        return self.root.metadict.lookup_typedef(self.typedef_name)
        # else:
        #     return self['Type'].value
    @property
    def store_format(self):
        return self.typedef.store_format

    def setup_defaults(self):
        self['Name'].value = self.property_name
        self['Identification'].value = self.uuid
        self['Type'].value = self.typedef.auid
        self['LocalIdentification'].value = self.pid
        self['IsOptional'].value = self.optional

        if not self.unique is None:
            self['IsUniqueIdentifier'].value = self.unique or False

    def read_properties(self):
        super(PropertyDef, self).read_properties()

        # print(self.property_entries)

        pid_name = 6
        pid_uuid = 5
        pid_type = 11
        pid_optional = 12
        pid_pid = 13
        pid_unique = 14

        self.property_name = decode_utf16le(self.property_entries[pid_name].data)
        self.uuid = UUID(bytes_le=self.property_entries[pid_uuid].data)
        self.typedef_name = UUID(bytes_le=self.property_entries[pid_type].data)
        self.pid = read_u16le(BytesIO(self.property_entries[pid_pid].data))
        self.optional = self.property_entries[pid_optional].data == b"\x01"
        if pid_unique in self.property_entries:
            self._unique = self.property_entries[pid_unique].data == b"\x01"

    def __repr__(self):
        return "<%s PropertyDef" % self.property_name

@register_class
class ClassDef(core.AAFObject):
    class_id = UUID("0d010101-0201-0000-060e-2b3402060101")

    def __new__(cls, root=None, name=None, uuid=None, parent=None, concrete=None):
        self = super(ClassDef, cls).__new__(cls)
        self.root = root
        self.class_name = name
        self.uuid = None
        if uuid:
            self.uuid = UUID(uuid)
        self.parent_name = parent
        self.concrete = concrete
        self._propertydefs = []
        return self

    def __eq__(self, other):
        self.uuid == other.uuid

    @property
    def unique_key(self):
        return self.uuid

    @property
    def unique_key_pid(self):
        for p in self.all_propertydefs():
            if p.unique:
                return p.pid

    @property
    def unique_key_size(self):
        mob_classdef = self.root.metadict.lookup_classdef(UUID("0d010101-0101-3400-060e-2b3402060101"))
        essencedata_classdef = self.root.metadict.lookup_classdef(UUID("0d010101-0101-2300-060e-2b3402060101"))
        if self.isinstance(mob_classdef) or self.isinstance(essencedata_classdef):
            return 32
        return 16

    def setup_defaults(self):
        self['Name'].value = self.class_name
        self['Identification'].value = self.uuid
        self['IsConcrete'].value = self.concrete


        for p in self._propertydefs:
            p.setup_defaults()
        if self._propertydefs:
            self['Properties'].value = self._propertydefs

        p = self.parent
        # if p and p.dir:
        # print('parent', p, self)

        # InterchangeObject parent is itself???
        if p is None:
            p = self

        # print(self, p)
        self['ParentClass'].value = p

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
    def parent(self):
        parent = self.parent_name

        parent_pid = 8
        if parent is None and parent_pid in self.property_entries:
            ref = self.property_entries[parent_pid].ref
            p = self.root.metadict.lookup_classdef(ref)
            parent = p.class_name


        if parent == self.class_name:
            # print(parent)
            return None

        return self.root.metadict.classdefs_by_name.get(parent, None)

    @property
    def propertydefs(self):
        return self._propertydefs


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

    def read_properties(self):
        super(ClassDef, self).read_properties()

        pid_name = 6
        pid_uuid = 5
        pid_abstract = 10
        pid_properties = 9

        self.class_name = decode_utf16le(self.property_entries[pid_name].data)
        self.uuid = UUID(bytes_le=self.property_entries[pid_uuid].data)
        self.concrete = self.property_entries[pid_abstract].data == b'\x01'

        if pid_properties in self.property_entries:
            for key,value in self.property_entries[pid_properties].items():
                self._propertydefs.append(value)



    def __repr__(self):
        return "<%s %s>" % (self.class_name, "ClassDef")

root_classes = {
#Hack property ids are class ids
'Root' : ('b3b398a5-1c90-11d4-8053-080036210804', None, True, {
    "Header"              : ('0d010301-0102-0100-060e-2b3401010102', 0x0002, "HeaderStrongRefence", False, False),
    "MetaDictionary"      : ('0d010301-0101-0100-060e-2b3401010102', 0x0001, "MetaDictionaryStrongReference", False, False),
})
}

root_types = {
"HeaderStrongRefence"             : (None, "Header"),
"MetaDictionaryStrongReference"   : (None, "MetaDictionary"),
}
# 0d010301-0101-0100-060e-2b3401010102

@register_class
class MetaDictionary(core.AAFObject):
    class_id = UUID("0d010101-0225-0000-060e-2b3402060101")
    def __init__(self, root):
        super(MetaDictionary, self).__init__(root)
        self.root = root
        self.classdefs_by_name = {}
        self.classdefs_by_uuid = {}
        self.typedefs_by_name = {}
        self.typedefs_by_uuid = {}

        self.typedefs_classes = {}

        for name, args in root_classes.items():
            self.add_classdef(name, *args)

        for name, args in classdefs.classdefs.items():
            self.add_classdef(name, *args)

        for alias, name in classdefs.aliases.items():
            self.classdefs_by_name[alias]= self.classdefs_by_name[name]

        # setup typedefs

        for name, args in root_types.items():
            t = types.TypeDefStrongRef(self.root, name, *args)
            self.typedefs_by_name[name] = t

        for name, args in typedefs.ints.items():
            t = types.TypeDefInt(self.root, name, *args)
            self.typedefs_by_name[name] = t

        for name, args in typedefs.enums.items():
            t = types.TypeDefEnum(self.root, name, *args)
            self.typedefs_by_name[name] = t

        for name, args in typedefs.records.items():
            t = types.TypeDefRecord(self.root, name, *args)
            self.typedefs_by_name[name] = t

        for name, args in typedefs.var_arrays.items():
            t = types.TypeDefVarArray(self.root, name, *args)
            self.typedefs_by_name[name] = t

        for name, args in typedefs.fixed_arrays.items():
            t =  types.TypeDefFixedArray(self.root, name, *args)
            self.typedefs_by_name[name] = t

        for name, args in typedefs.renames.items():
            self.typedefs_by_name[name] = types.TypeDefRename(self.root, name, *args)

        for name, args in typedefs.strings.items():
            self.typedefs_by_name[name] = types.TypeDefString(self.root, name, *args)

        for name, args in typedefs.extenums.items():
            self.typedefs_by_name[name] = types.TypeDefExtEnum(self.root, name, *args)

        for name, auid in typedefs.chars.items():
            self.typedefs_by_name[name] = types.TypeDefCharacter(self.root, name, auid)

        for name, auid in typedefs.indirects.items():
            self.typedefs_by_name[name] = types.TypeDefIndirect(self.root, name, auid)

        for name, auid in typedefs.opaques.items():
            self.typedefs_by_name[name] = types.TypeDefOpaque(self.root, name, auid)

        for name, args in typedefs.sets.items():
            self.typedefs_by_name[name] = types.TypeDefSet(self.root, name, *args)

        for name, args in typedefs.strongrefs.items():
            self.typedefs_by_name[name] = types.TypeDefStrongRef(self.root, name, *args)

        for name, args in typedefs.weakrefs.items():
            self.typedefs_by_name[name] = types.TypeDefWeakRef(self.root, name, *args)

        for name, auid in typedefs.streams.items():
            self.typedefs_by_name[name] = types.TypeDefStream(self.root, name, auid)

        for name, typedef in self.typedefs_by_name.items():
            if typedef.auid is None:
                continue

            self.typedefs_by_uuid[typedef.auid] = typedef
            self.typedefs_classes[typedef.auid] = typedef.__class__


    def setup_defaults(self):

        self['TypeDefinitions'].value = self.typedefs_by_uuid.values()


        classes = []
        for k, c in self.classdefs_by_uuid.items():
            if c.class_name == "Root":
                continue
            classes.append(c)

        self['ClassDefinitions'].value = classes

        for name, typedef in self.typedefs_by_uuid.items():
            typedef.setup_defaults()



        done = set(["Root"])
        for c in classes:
            # print c.class_name

            for p in reversed(list(c.relatives())):
                if p.class_name in done:
                    continue

                p.setup_defaults()
                done.add(p.class_name)

        # for c in classes:
        #     c.setup_defaults()

    def add_classdef(self, name, *args):
        c = ClassDef(self.root, name, *args[:3])

        for prop_name, prop_args in args[3].items():
            p = PropertyDef(self.root, prop_name, *prop_args)
            c.propertydefs.append(p)

        self.classdefs_by_name[name]   = c
        self.classdefs_by_uuid[c.uuid] = c


    def lookup_class(self, class_id):
        if class_id in AAFClaseID_dict:
            return AAFClaseID_dict[class_id]

        if class_id in AAFClassName_dict:
            return AAFClassName_dict[class_id]

        if class_id in self.typedefs_classes:
            return self.typedefs_classes[class_id]

        return core.AAFObject

    def lookup_typedef(self, t):
        if isinstance(t, UUID):
            return self.typedefs_by_uuid.get(t, None)

        # if t == 'MetaDictionaryStrongReference':


        return self.typedefs_by_name.get(t, None)


    def lookup_classdef(self, t):
        if isinstance(t, UUID):
            return self.classdefs_by_uuid.get(t, None)
        return self.classdefs_by_name.get(t, None)

    @property
    def classdef(self):
        return self.classdefs_by_name['MetaDictionary']

    def read_properties(self):
        super(MetaDictionary, self).read_properties()
        for key, typedef in self['TypeDefinitions'].items():
            name = typedef.type_name
            uuid = typedef.auid

            self.typedefs_by_name[name] = typedef
            self.typedefs_by_uuid[uuid] = typedef

        for key, classdef in self['ClassDefinitions'].items():
            name = classdef.class_name
            uuid = classdef.uuid
            self.classdefs_by_name[name] = classdef
            self.classdefs_by_uuid[uuid] = classdef
