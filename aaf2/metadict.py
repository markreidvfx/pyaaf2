
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import traceback
from StringIO import StringIO
from . import types

from .model import classdefs
from .model import typedefs
from .model import datadefs

from . import core
from .utils import read_u16le

import uuid
from uuid import UUID

class PropertyDef(core.AAFObject):
    def __init__(self, root, name=None, uuid=None, pid=None, typedef=None, optional=None, unique=None):
        super(PropertyDef, self).__init__(root)
        self.class_id = UUID("0d010101-0202-0000-060e-2b3402060101")
        self.property_name = name
        self.uuid = None
        if uuid:
            self.uuid = UUID(uuid)
        self.pid = pid
        self.typedef_name = typedef
        self.optional = optional
        self.unique = unique

    @property
    def typedef(self):
        return self.root.metadict.lookup_typedef(self.typedef_name)
    @property
    def store_format(self):
        return self.typedef.store_format

    def read_properties(self):
        super(PropertyDef, self).read_properties()

        # print(self.property_entries)

        pid_name = 6
        pid_uuid = 5
        pid_type = 11
        pid_required= 12
        pid_pid = 13
        pid_unique = 14

        self.property_name = self.property_entries[pid_name].data[:-2].decode("utf-16le")
        self.uuid = UUID(bytes_le=self.property_entries[pid_uuid].data)
        self.typedef_name = UUID(bytes_le=self.property_entries[pid_type].data)
        self.pid = read_u16le(StringIO(self.property_entries[pid_pid].data))
        self.required = self.property_entries[pid_required].data == "\x01"
        if pid_unique in self.property_entries:
            self.unique = self.property_entries[pid_unique].data == "\x01"

    def __repr__(self):
        return "<%s PropertyDef" % self.property_name

class ClassDef(core.AAFObject):
    def __init__(self, root=None, name=None, uuid=None, parent=None, abstract=None):
        super(ClassDef, self).__init__(root)
        self.class_id = UUID("0d010101-0201-0000-060e-2b3402060101")
        self.class_name = name
        self.uuid = None
        if uuid:
            self.uuid = UUID(uuid)
        self.parent_name = parent
        self.abstract = abstract
        self._propertydefs = []

    def __eq__(self, other):
        self.uuid == other.uuid

    def isinstance(self, other):
        if not isinstance(other, ClassDef):
            other = other.classdef
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
        if self.class_name in ('InterchangeObject', 'Root', 'MetaDefinition'):
            return None

        parent = self.parent_name
        parent_pid = 8
        if parent is None and parent_pid in self.property_entries:
            p = self.property_entries[parent_pid].value
            parent = p.class_name

        if parent == ('InterchangeObject', 'Root', 'MetaDefinition'):
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
                continue
                # raise Exception(self.class_name)

            for p in classdef.propertydefs:
                yield p

    def read_properties(self):
        super(ClassDef, self).read_properties()

        pid_name = 6
        pid_uuid = 5
        pid_abstract = 10
        pid_properties = 9

        self.class_name = self.property_entries[pid_name].data[:-2].decode('utf-16le')
        self.uuid = UUID(bytes_le=self.property_entries[pid_uuid].data)
        self.abstract = self.property_entries[pid_abstract].data == '\x01'

        if pid_properties in self.property_entries:
            for key,value in self.property_entries[pid_properties].items():
                self._propertydefs.append(value)



    def __repr__(self):
        return "<%s %s>" % (self.class_name, "ClassDef")

root_classes = {
#Hack property ids are class ids
'Root' : ('b3b398a5-1c90-11d4-8053-080036210804', None, True, {
    "Header"              : (None, 0x0002, "HeaderStrongRefence", False, False),
    "MetaDictionary"      : (None, 0x0001, "MetaDictionaryStrongReference", False, False),
})
}

root_types = {
"HeaderStrongRefence"             : (None, "Header"),
"MetaDictionaryStrongReference"   : (None, "MetaDictionary"),
}

class MetaDictionary(core.AAFObject):
    def __init__(self, root):
        super(MetaDictionary, self).__init__(root)
        self.class_id = UUID("0d010101-0225-0000-060e-2b3402060101")
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

        for name, args in typedefs.arrays.items():
            if args[-1] is None:
                t = types.TypeDefVarArray(self.root, name, *args[:-1])
            else:
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

        # need to look more into these
        for name, args in typedefs.strongref_sets.items():
            self.typedefs_by_name[name] = types.TypeDefSet(self.root, name, *args)

        for name, args in typedefs.strongref_vectors.items():
            self.typedefs_by_name[name] = types.TypeDefVarArray(self.root, name, *args)

        for name, args in typedefs.weakrefs.items():
            self.typedefs_by_name[name] = types.TypeDefWeakRef(self.root, name, *args)

        for name, args in typedefs.weakref_sets.items():
            self.typedefs_by_name[name] = types.TypeDefSet(self.root, name, *args)

        for name, args in typedefs.weakref_vectors.items():
            self.typedefs_by_name[name] = types.TypeDefVarArray(self.root, name, *args)

        for name, auid in typedefs.streams.items():
            self.typedefs_by_name[name] = types.TypeDefStream(self.root, name, auid)

        for name, typedef in self.typedefs_by_name.items():
            self.typedefs_by_uuid[typedef.auid] = typedef
            self.typedefs_classes[typedef.class_id] = typedef.__class__

    def setup_empty(self):
        d = {}
        for name, typedef in self.typedefs_by_name.items():
            d[str(uuid.uuid4())] = typedef

        self['TypeDefinitions'].value = d

    def add_classdef(self, name, *args):
        c = ClassDef(self.root, name, *args[:3])

        for prop_name, prop_args in args[3].items():
            p = PropertyDef(self.root, prop_name, *prop_args)
            c.propertydefs.append(p)

        self.classdefs_by_name[name]   = c
        self.classdefs_by_uuid[c.uuid] = c


    def lookup_class(self, class_id):

        if class_id == UUID("0d010101-0201-0000-060e-2b3402060101"):
            return ClassDef

        if class_id == UUID("0d010101-0202-0000-060e-2b3402060101"):
            return PropertyDef

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
