from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import uuid

from .auid import AUID
from .model import datadefs
from . import core
from .utils import register_class

def short_name(name):
    for s in ('DataDef_', 'ContainerDef_'):
        name = name.replace(s, "")
    return name

def lookup_def(dictionary, name, instance_type, key):
    if isinstance(name, AUID):
        return dictionary[key].get(name, None)

    if isinstance(name, uuid.UUID):
        return dictionary[key].get(AUID(name), None)

    if isinstance(name, instance_type):
        return name

    name = short_name(name).lower()

    for key, value in dictionary[key].items():
        value_name = value.short_name or ''
        if name == value_name.lower():
            return value

    raise Exception("No Definition: %s" % str(name))

@register_class
class DefinitionObject(core.AAFObject):
    class_id = AUID("0d010101-0101-1a00-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, auid=None, name=None, description=None):
        super(DefinitionObject, self).__init__()
        self.name = name
        self.description = description
        if auid:
            self.auid = AUID(str(auid))

    @property
    def name(self):
        return self['Name'].value

    @name.setter
    def name(self, value):
        self['Name'].value = value

    @property
    def short_name(self):
        name = self.name
        if name:
            return short_name(name)

    @property
    def description(self):
        return self['Description'].value

    @description.setter
    def description(self, value):
        self['Description'].value =  value

    @property
    def auid(self):
        return self['Identification'].value

    @auid.setter
    def auid(self, value):
        self['Identification'].value = value

    @property
    def uuid(self):
        auid = self.auid
        if auid is not None:
            return auid.uuid

    @uuid.setter
    def uuid(self, value):
        self.auid = AUID(value)

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                       self.__class__.__name__)
        name = self.name
        if name:
            s += " %s" % name

        return '<%s %s at 0x%x>' % (s, str(self.auid), id(self))

    @property
    def unique_key(self):
        return self.auid

@register_class
class DataDef(DefinitionObject):
    class_id = AUID("0d010101-0101-1b00-060e-2b3402060101")
    __slots__ = ()

@register_class
class OperationDef(DefinitionObject):
    class_id = AUID("0d010101-0101-1c00-060e-2b3402060101")
    __slots__ = ()

    @property
    def datadef(self):
        return self['DataDefinition'].value

    @datadef.setter
    def datadef(self, value):
        self['DataDefinition'].value = value

    @property
    def media_kind(self):
        datadef = self.datadef
        if datadef:
            return datadef.short_name

    @media_kind.setter
    def media_kind(self, value):
        self.datadef = self.root.dictionary.lookup_datadef(value)

    @property
    def parameters(self):
        return self['ParametersDefined']

    @property
    def number_inputs(self):
        return self['NumberInputs'].value

    @number_inputs.setter
    def number_inputs(self, value):
        self['NumberInputs'].value = value


@register_class
class ParameterDef(DefinitionObject):
    class_id = AUID("0d010101-0101-1d00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, auid=None, name=None, description=None, typedef=None):
        super(ParameterDef, self).__init__(auid, name, description)
        if typedef:
            self.typedef = self.root.dictionary.lookup_typedef(typedef)

    @property
    def typedef(self):
        return self['Type'].value

    @typedef.setter
    def typedef(self, value):
        self['Type'].value = value

@register_class
class PluginDef(DefinitionObject):
    class_id = AUID("0d010101-0101-1e00-060e-2b3402060101")
    __slots__ = ()

@register_class
class CodecDef(DefinitionObject):
    class_id = AUID("0d010101-0101-1f00-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, dictionary, auid=None, name=None, description=None, classdef=None, datadef_names=None):
        super(CodecDef, self).__init__(auid, name, description)
        if classdef:
            self['FileDescriptorClass'].value = self.root.metadict.lookup_classdef(classdef)

        for d in datadef_names or []:
            self['DataDefinitions'].append(dictionary.lookup_datadef(d))

@register_class
class ContainerDef(DefinitionObject):
    class_id = AUID("0d010101-0101-2000-060e-2b3402060101")
    __slots__ = ()

@register_class
class InterpolationDef(DefinitionObject):
    class_id = AUID("0d010101-0101-2100-060e-2b3402060101")
    __slots__ = ()

@register_class
class TaggedValueDef(DefinitionObject):
    class_id = AUID("0d010101-0101-4c00-060e-2b3402060101")
    __slots__ = ()

@register_class
class Dictionary(core.AAFObject):
    class_id = AUID("0d010101-0101-2200-060e-2b3402060101")
    __slots__ = ()
    def __init__(self):
        super(Dictionary, self).__init__()

        for key, args in datadefs.DataDefs.items():
            d = self.root.create.DataDef(key, *args)
            self['DataDefinitions'].append(d)

        for key, args in datadefs.ContainerDefs.items():
            d = self.root.create.ContainerDef(key, *args)
            self['ContainerDefinitions'].append(d)

    def setup_defaults(self):

        for key, args in datadefs.CodecDefs.items():
            if len(args) > 2:
                d = self.root.create.CodecDef(self, key, *args)
                self['CodecDefinitions'].append(d)

    def register_def(self, defobject):

        if isinstance(defobject, DataDef):
            self['DataDefinitions'].append(defobject)
        elif isinstance(defobject, ContainerDef):
            self['ContainerDefinitions'].append(defobject)
        elif isinstance(defobject, CodecDef):
            self['CodecDefinitions'].append(defobject)
        elif isinstance(defobject, ParameterDef):
            self['ParameterDefinitions'].append(defobject)
        elif isinstance(defobject, OperationDef):
            self['OperationDefinitions'].append(defobject)
        elif isinstance(defobject, InterpolationDef):
            self['InterpolationDefinitions'].append(defobject)
        elif isinstance(defobject, TaggedValueDef):
            self['TaggedValueDefinitions'].append(defobject)
        else:
            raise ValueError("unknown definitions type: %s" % str(type(defobject)))

    def lookup_typedef(self, name):
        return self.root.metadict.lookup_typedef(name)

    def lookup_datadef(self, name):
        return lookup_def(self, name, DataDef, 'DataDefinitions')

    def lookup_containerdef(self, name):
        return lookup_def(self, name, ContainerDef, 'ContainerDefinitions')

    def lookup_codecdef(self, name):
        return lookup_def(self, name, CodecDef, 'CodecDefinitions')

    def lookup_parameterdef(self, name):
        return lookup_def(self, name, ParameterDef, 'ParameterDefinitions')

    def lookup_operationdef(self, name):
        return lookup_def(self, name, OperationDef, 'OperationDefinitions')

    def lookup_interperlationdef(self, name):
        return lookup_def(self, name, InterpolationDef, 'InterpolationDefinitions')

    def lookup_taggedvaluedef(self, name):
        return lookup_def(self, name, TaggedValueDef, 'TaggedValueDefinitions')

    def update(self, other):
        if not isinstance(other, Dictionary):
            raise ValueError("other must be a Dictionary object")

        for def_type in ('DataDefinitions',
                         'ContainerDefinitions',
                         'CodecDefinitions',
                         'ParameterDefinitions',
                         'OperationDefinitions',
                         'InterpolationDefinitions',
                         'TaggedValueDefinitions'):

            for other_def in other[def_type].values():
                if other_def.auid not in self[def_type]:
                    self[def_type].append(other_def.copy(root=self.root))

                elif def_type == 'OperationDefinitions':
                    # make sure operation all the same parameters
                    opdef = self.lookup_operationdef(other_def.auid)
                    for p in other_def.parameters:
                        param = self.lookup_parameterdef(p.auid)
                        if param.unique_key not in opdef.parameters:
                            opdef.append(param)
