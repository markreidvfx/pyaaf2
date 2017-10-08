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

@register_class
class DefinitionObject(core.AAFObject):
    class_id = UUID("0d010101-0101-1a00-060e-2b3402060101")
    def __init__(self, uuid=None, name=None, description=None):
        super(DefinitionObject, self).__init__()
        self.def_name = name
        self.description = description
        self.uuid = None
        if uuid:
            self.uuid = UUID(uuid)

    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.def_name)

    def setup_defaults(self):
        self['Name'].value = self.def_name
        self['Identification'].value = self.uuid
        self['Description'].value = self.description

    @property
    def unique_key(self):
        return self.uuid

    def read_properties(self):
        super(DefinitionObject, self).read_properties()
        self.def_name = self['Name'].value
        self.uuid = self['Identification'].value
        self.description = self['Description'].value

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

    def setup_defaults(self):

        for key in ('CodecDefinitions' ,'InterpolationDefinitions' ,
                    'ParameterDefinitions' ,'TaggedValueDefinitions' ,
                    'KLVDataDefinitions' ,'OperationDefinitions' ,
                    'PluginDefinitions' ,'ContainerDefinitions' ,'DataDefinitions'):
            pass
            # self[key].value = []

        for item in self.datadefs.values():
            item.setup_defaults()

        self['DataDefinitions'].value = self.datadefs

        for item in self.containerdefs.values():
            item.setup_defaults()

        self['ContainerDefinitions'].value = self.containerdefs
