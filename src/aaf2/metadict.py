from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from io import BytesIO
from . import types
from .model import classdefs
from .model import typedefs as base_typedefs
from . import properties
from .auid import AUID

from . import core
from .utils import (register_class, read_u16le, decode_utf16le,
                    encode_utf16le, encode_u16le, str2auid,
                    AAFClaseID_dict, AAFClassName_dict)

PID_NAME      = 0x0006
PID_AUID      = 0x0005
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
    class_id = AUID("0d010101-0202-0000-060e-2b3402060101")
    __slots__ = ('_typedef_id', '_auid', '_property_name')

    def __new__(cls, root=None, name=None, auid=None, pid=None, typedef=None, optional=None, unique=None):
        self = super(PropertyDef, cls).__new__(cls)
        self.root = root
        self._typedef_id = None
        self._auid = None
        self._property_name = name
        if root:
            properties.add_string_property(self, PID_NAME, name)
            properties.add_bool_property(self, PID_OPTIONAL, optional)
            properties.add_bool_property(self, PID_UNIQUE, unique)
            properties.add_u16le_property(self, PID_PID, pid)
            properties.add_auid_property(self, PID_AUID, auid)
            properties.add_auid_property(self, PID_TYPE, typedef)

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
        return self.auid

    @property
    def unique(self):
        if PID_UNIQUE in self.property_entries:
            return self.property_entries[PID_UNIQUE].data == b"\x01"
        return False

    @property
    def pid(self):
        with BytesIO(self.property_entries[PID_PID].data) as f:
            return read_u16le(f)

    @pid.setter
    def pid(self, value):
        self.property_entries[PID_PID].data = encode_u16le(value)

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
    def optional(self):
        return self.property_entries[PID_OPTIONAL].data == b"\x01"

    @property
    def typedef_id(self):
        if self._typedef_id:
            return self._typedef_id

        p = self.property_entries.get(PID_TYPE)
        self._typedef_id = AUID(bytes_le=p.data)
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
        return "<%s PropertyDef>" % self.property_name


@register_class
class ClassDef(core.AAFObject):
    class_id = AUID("0d010101-0201-0000-060e-2b3402060101")
    __slots__ = ('propertydef_by_pid')

    def __new__(cls, root=None, name=None, class_auid=None, parent_auid=None, concrete=None):
        self = super(ClassDef, cls).__new__(cls)
        self.root = root
        self.propertydef_by_pid = {}
        if root:
            properties.add_string_property(self, PID_NAME, name)
            properties.add_auid_property(self, PID_AUID, class_auid)
            properties.add_bool_property(self, PID_CONCRETE, concrete)

            # reference self auid if no parent
            properties.add_classdef_weakref_property(self, PID_PARENT, parent_auid or class_auid)
            properties.add_strongref_set_property(self, PID_PROPERTIES, "Properties", PID_AUID)

        return self

    def __eq__(self, other):
        self.auid == other.auid

    @property
    def auid(self):
        data = self.property_entries[PID_AUID].data
        if data is not None:
            return AUID(bytes_le=self.property_entries[PID_AUID].data)

    @property
    def uuid(self):
        return self.auid.uuid

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
        return self.auid

    @property
    def unique_key_pid(self):
        for p in self.all_propertydefs():
            if p.unique:
                return p.pid

        # Parameter work around
        # Uses the DefinitionObject Identification PID
        if self.isinstance(self.root.metadict.lookup_classdef(AUID("0d010101-0101-3c00-060e-2b3402060101"))):
            return 0x1B01

    @property
    def unique_key_size(self):
        mob_classdef = self.root.metadict.lookup_classdef(AUID("0d010101-0101-3400-060e-2b3402060101"))
        essencedata_classdef = self.root.metadict.lookup_classdef(AUID("0d010101-0101-2300-060e-2b3402060101"))
        if self.isinstance(mob_classdef) or self.isinstance(essencedata_classdef):
            return 32
        return 16

    def isinstance(self, other):

        if self.auid == other.auid:
            return True

        for classdef in other.relatives():
            if classdef.auid == self.auid:
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

        if parent_id == self.auid:
            return None

        return self.root.metadict.classdefs_by_auid.get(parent_id, None)

    @property
    def propertydefs(self):
        if PID_PROPERTIES in self.property_entries:
            return self.property_entries[PID_PROPERTIES].values()
        return []

    def lookup_propertydef(self, property_auid):
        for classdef in self.relatives():
            p = classdef.property_entries.get(PID_PROPERTIES, {}).get(property_auid, None)
            if p:
                return p

    def register_propertydef(self, name, property_auid, pid, typedef, optional, unique=False):

        # check if PropertyDef is already defined
        property_auid = str2auid(property_auid)
        p = self.property_entries.get(PID_PROPERTIES, {}).get(property_auid, None)
        if p:
            return p

        typedef = str2auid(typedef)
        if isinstance(typedef, AUID):
            typedef_auid = typedef
        else:
            typedef = self.root.metadict.lookup_typedef(typedef)
            typedef_auid = typedef.auid

        # None signifies Dynamically allocated Local Tags
        # I think this is similar to MXF where pids > 0x8000 < 0xFFFF
        # are extensions pids
        if pid is None:
            pid = self.root.metadict.next_free_pid()
            # assert False

        p = PropertyDef(self.root, name, property_auid, pid, typedef_auid, optional, unique)
        # # this is done low level to avoid recursion errors

        if PID_PROPERTIES not in self.property_entries:
            properties.add_strongref_set_property(self, PID_PROPERTIES, "Properties", PID_AUID)

        properties.add2set(self, PID_PROPERTIES, p.auid, p)
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
    class_id = AUID("0d010101-0225-0000-060e-2b3402060101")
    def __init__(self, root):
        super(MetaDictionary, self).__init__(root)

        self.root = root
        root.metadict = self

        properties.add_strongref_set_property(self, PID_CLASSDEFS, "ClassDefinitions", PID_AUID)
        properties.add_strongref_set_property(self, PID_TYPEDEFS, "TypeDefinitions", PID_AUID)

        self.classdefs_by_name = {}
        self.classdefs_by_auid = {}
        self.typedefs_by_name = {}
        self.typedefs_by_auid = {}

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
                            t.register_element(element_name, AUID(element_value))
                    else:
                        t = types.TypeDefExtEnum(self.root, name, *args)
                        properties.add2set(self, PID_TYPEDEFS, t.auid, t)
                elif cat == "enums":
                    if name in self.typedefs_by_name:
                        t = self.typedefs_by_name[name]
                        for element_value, element_name in args[2].items():
                            t.register_element(element_name, element_value)
                    else:
                        t = types.TypeDefEnum(self.root, name, *args)
                        properties.add2set(self, PID_TYPEDEFS, t.auid, t)
                else:

                    t = classobj(self.root, name, *args)
                    properties.add2set(self, PID_TYPEDEFS, t.auid, t)

                self.typedefs_by_name[name] = t
                self.typedefs_by_auid[t.auid] = t
                self.typedefs_classes[t.auid] = t.__class__

    def register_extensions(self):
        from .model.ext import classdefs as ext_classdefs
        from .model.ext import typedefs as ext_typedefs

        for name, args in ext_classdefs.classdefs.items():
            self.register_classdef(name, *args)

        for alias, name in ext_classdefs.aliases.items():
            self.classdefs_by_name[alias]= self.classdefs_by_name[name]

        self.register_typedef_model(ext_typedefs.__dict__)

    def register_classdef(self, name, class_auid, parent, concrete, propertydefs=None):
        if not isinstance(class_auid, AUID):
            class_auid = AUID(class_auid)

        parent = str2auid(parent)

        if parent is None:
            parent_auid = None
        elif isinstance(parent, AUID):
            parent_auid = parent
        else:
            parent_classdef = self.lookup_classdef(parent)
            parent_auid = parent_classdef.auid

        if name in self.classdefs_by_name:
            c = self.classdefs_by_name[name]
        elif class_auid in self.classdefs_by_auid:
            c = self.classdefs_by_name[class_auid]
        else:
            c = ClassDef(self.root, name, class_auid, parent_auid, concrete)

        if propertydefs:
            for prop_name, prop_args in propertydefs.items():
                property_auid = prop_args[0]
                pid = prop_args[1]

                if pid is None:
                    pid = self.next_free_pid()
                elif pid and pid >= 0x8000:
                    assert pid not in self.local_pids
                    self.local_pids.add(pid)

                c.register_propertydef(prop_name, property_auid, pid, *prop_args[2:])

        self.classdefs_by_name[name]   = c
        self.classdefs_by_auid[c.auid] = c

        # Root is not include in the data model for some reason
        if c.class_name != "Root":
            properties.add2set(self, PID_CLASSDEFS, c.auid, c)
        return c

    def register_external_typedef(self, ext_typedef):
        if not isinstance(ext_typedef, types.TypeDef):
            return None

        typedef = self.lookup_typedef(ext_typedef.auid)

        # create typedef if missing
        if not typedef:
            if isinstance(ext_typedef, (types.TypeDefStrongRef,
                                        types.TypeDefWeakRef)):
                # could this cause RecursionError?
                classdef = ext_typedef.ref_classdef
                self.register_external_classdef(classdef)

            elif isinstance(ext_typedef, (types.TypeDefFixedArray,
                                          types.TypeDefVarArray,
                                          types.TypeDefSet,
                                          types.TypeDefString,
                                          types.TypeDefEnum)):

                self.register_external_typedef(ext_typedef.element_typedef)

            elif isinstance(ext_typedef, types.TypeDefRecord):
                for t in ext_typedef.member_types:
                    self.register_external_typedef(t)

            elif isinstance(ext_typedef, types.TypeDefRename):
                self.register_external_typedef(ext_typedef.renamed_typedef)

            elif isinstance(ext_typedef, types.TypeDefEnum):
                self.register_external_typedef(ext_typedef.element_typedef)

            typedef = ext_typedef.copy(self.root)

            self['TypeDefinitions'].append(typedef)
            self.typedefs_by_name[typedef.type_name] = typedef
            self.typedefs_by_auid[typedef.auid] = typedef

        # make sure enum has all the values
        if isinstance(ext_typedef, (types.TypeDefExtEnum, types.TypeDefEnum)):
            ext_elements = ext_typedef.elements
            elements = typedef.elements

            for k, v in ext_elements.items():
                if k not in elements:
                    typedef.register_element(v, k)

        return typedef

    def register_external_classdef(self, ext_classdef):
        class_chain = list(ext_classdef.relatives())
        class_chain.reverse()
        for c in class_chain[1:]:
            classdef = self.lookup_classdef(c.auid)
            if not classdef:
                classdef = self.register_classdef(c.class_name,
                                                  c.auid,
                                                  c.parent.auid,
                                                  c.concrete)

            for p in c.propertydefs:
                typedef = self.register_external_typedef(p.typedef)
                pid = p.pid

                if pid >= 0x8000:
                    pid = None

                classdef.register_propertydef(p.property_name, p.auid, pid, typedef.auid, p.optional, p.unique)

        return self.lookup_classdef(ext_classdef.auid)

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

        t = str2auid(t)
        if isinstance(t, AUID):
            return self.typedefs_by_auid.get(t, None)
        return self.typedefs_by_name.get(t, None)

    def lookup_classdef(self, t):
        if isinstance(t, ClassDef):
            return t
        t = str2auid(t)
        if isinstance(t, AUID):
            return self.classdefs_by_auid.get(t, None)
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
            self.typedefs_by_auid[typedef.auid] = typedef

        # reset local pids
        self.local_pids = set()
        for key, classdef in self['ClassDefinitions'].items():
            self.classdefs_by_name[classdef.class_name] = classdef
            self.classdefs_by_auid[classdef.auid] = classdef
            propertydef_by_pid = {}
            for pdef in classdef['Properties'].values():
                if pdef.pid >= 0x8000:
                    self.local_pids.add(pdef.pid)

                propertydef_by_pid[pdef.pid] = pdef

            classdef.propertydef_by_pid = propertydef_by_pid


        # add typedefs not defined by file data model
        if self.root.writeable:
            for key, typedef in self.typedefs_by_auid.items():
                # skip root typedefs
                if key in (AUID('05022800-0000-0000-060E-2B3401040101'),
                           AUID('05022700-0000-0000-060E-2B3401040101')):
                    continue

                if key not in self['TypeDefinitions']:
                    # this is super annoying, handle typedefs that have dynamic pids
                    classdef = self.classdefs_by_auid.get(typedef.class_id)
                    assert classdef
                    for pdef in classdef['Properties'].values():
                        if pdef.pid >= 0x8000:
                            # if typedef has a dynamic pid might need to change it
                            if pdef.pid in self.local_pids:
                                old_pid = pdef.pid
                                new_pid = self.next_free_pid()
                                pdef.pid = new_pid

                                prop = typedef.property_entries.pop(old_pid)
                                prop.pid = new_pid
                                typedef.property_entries[new_pid] = prop

                    self['TypeDefinitions'].append(typedef)
                    if classdef.auid not in self['ClassDefinitions']:
                        self['ClassDefinitions'].append(classdef)

        # add classdefs not defined by file data model
        if self.root.writeable:
            for key, classdef in self.classdefs_by_auid.items():
                # skip root classdefs
                if key in (AUID('b3b398a5-1c90-11d4-8053-080036210804'), ):
                    continue

                if key not in self['ClassDefinitions']:

                    # handle any conflicting dynamic pids
                    for pdef in classdef['Properties'].values():
                        if pdef.pid >= 0x8000:
                            if pdef.pid in self.local_pids:
                                pdef.pid = self.next_free_pid()

                    self['ClassDefinitions'].append(classdef)
