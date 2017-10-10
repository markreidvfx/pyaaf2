from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from .model import datadefs
from . import core
from .utils import register_class

def short_name(name):
    for s in ('DataDef_',):
        name = name.replace(s, "")
    return s

@register_class
class DefinitionObject(core.AAFObject):
    class_id = UUID("0d010101-0101-1a00-060e-2b3402060101")
    def __init__(self, uuid=None, name=None, description=None):
        super(DefinitionObject, self).__init__()
        self.name = name
        self.description = description
        if uuid:
            self.uuid = UUID(uuid)

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
    def uuid(self):
        return self['Identification'].value

    @uuid.setter
    def uuid(self, value):
        self['Identification'].value = value

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                       self.__class__.__name__)
        name = self.name
        if name:
            s += " %s" % name

        return '<%s at 0x%x>' % (s, id(self))

    @property
    def unique_key(self):
        return self.uuid

@register_class
class DataDef(DefinitionObject):
    class_id = UUID("0d010101-0101-1b00-060e-2b3402060101")

@register_class
class OperationDef(DefinitionObject):
    class_id = UUID("0d010101-0101-1c00-060e-2b3402060101")

@register_class
class ParameterDef(DefinitionObject):
    class_id = UUID("0d010101-0101-1d00-060e-2b3402060101")

@register_class
class PluginDef(DefinitionObject):
    class_id = UUID("0d010101-0101-1e00-060e-2b3402060101")

@register_class
class CodecDef(DefinitionObject):
    class_id = UUID("0d010101-0101-1f00-060e-2b3402060101")
    def __init__(self, dictionary, uuid=None, name=None, description=None, classdef=None, datadef_names=None):
        super(CodecDef, self).__init__(uuid, name, description)
        if classdef:
            self['FileDescriptorClass'].value = self.root.metadict.lookup_classdef(classdef)

        for d in datadef_names or []:
            self['DataDefinitions'].append(dictionary.lookup_datadef(d))

@register_class
class ContainerDef(DefinitionObject):
    class_id = UUID("0d010101-0101-2000-060e-2b3402060101")

@register_class
class InterpolationDef(DefinitionObject):
    class_id = UUID("0d010101-0101-2100-060e-2b3402060101")

@register_class
class Dictionary(core.AAFObject):
    class_id = UUID("0d010101-0101-2200-060e-2b3402060101")
    def __init__(self):
        super(Dictionary, self).__init__()

        self.datadefs = {}
        for key, args in datadefs.DataDefs.items():
            d = self.root.create.DataDef(key, *args)
            self.datadefs[d.uuid] = d

        self.containerdefs = {}
        for key, args in datadefs.ContainerDefs.items():
            d = self.root.create.ContainerDef(key, *args)
            self.containerdefs[d.uuid] = d

        self['DataDefinitions'].value = self.datadefs
        self['ContainerDefinitions'].value = self.containerdefs

    def setup_defaults(self):
        self.codecdefs = {}
        for key, args in datadefs.CodecDefs.items():
            if len(args) > 2:
                d = self.root.create.CodecDef(self, key, *args)
                self.codecdefs[d.uuid] = d

        self['CodecDefinitions'].value = self.codecdefs

    def lookup_datadef(self, name):
        if isinstance(name, DataDef):
            return name

        name = short_name(name)
        for key, value in self['DataDefinitions'].items():
            if name.lower() == value.short_name.lower():
                return value
            if name == key:
                return value

        raise Exception("No datadef: %s" % str(name))

    def lookup_containerdef(self, name):
        if isinstance(name, ContainerDef):
            return name

        name = short_name(name)
        for key, value in self['ContainerDefinitions'].items():
            if name.lower() == value.short_name.lower():
                return value
            if name == key:
                return value

        raise Exception("No ContainerDef: %s" % str(name))
