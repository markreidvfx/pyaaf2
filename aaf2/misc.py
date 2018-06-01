from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID
from datetime import datetime
import io

from . import core
from . utils import register_class

class TaggedValueHelper(object):
    def __init__(self, poperty_vector):
        self.p = poperty_vector

    def get(self, key, default=None):
        for item in self.p:
            if item['Name'].value == key:
                return item
        return default

    def __contains__(self, key):
        return not self.get(key, None) is None

    def __getitem__(self, key):
        p = self.get(key, None)
        if p:
            return p['Value'].value

        raise IndexError(key)

    def items(self):
        for item in self.p:
            yield item['Name'].value, item["Value"].value

    def append(self, value):
        self.p.append(value)

    def __setitem__(self, key, value):
        tag = self.get(key, None)
        if tag is None:
            tag = self.p.parent.root.create.TaggedValue()
            tag['Name'].value = key
            self.p.append(tag)

        tag['Value'].value = value

@register_class
class TaggedValue(core.AAFObject):
    class_id = UUID("0d010101-0101-3f00-060e-2b3402060101")
    __slots__ = ()

    def __init__(self, name=None, value=None, value_typedef=None):
        self.name = name
        if value is not None:
            self.encode_value(value, value_typedef)

    @property
    def name(self):
        return self['Name'].value

    @name.setter
    def name(self, value):
        self['Name'].value = value

    @property
    def value(self):
        return self['Value'].value

    @value.setter
    def value(self, value):
        self['Value'].value = value

    @property
    def value_typedef(self):
        if self['Value'].data:
            return self['Value'].typedef.decode_typedef(self['Value'].data)

    def encode_value(self, value, value_typedef=None):
        if value_typedef is None:
            self.value = value
            return
        self['Value'].add_pid_entry()
        self['Value'].data = self['Value'].typedef.encode(value, value_typedef)
        self['Value'].mark_modified()

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                                self.__class__.__name__)
        name = self.name
        if name:
            s += ' %s' % name

        s += " = " + str(self.value)

        return '<%s at 0x%x>' % (s, id(self))

class Parameter(core.AAFObject):
    class_id = UUID("0d010101-0101-3c00-060e-2b3402060101")
    __slots__ = ()

    @property
    def uuid(self):
        return self['Definition'].value
    @uuid.setter
    def uuid(self, value):
        self['Definition'].value = value

    @property
    def parameterdef(self):
        return self.root.dictionary.lookup_parameterdef(self['Definition'].value)

    @parameterdef.setter
    def parameterdef(self, value):
        self['Definition'].value = value.uuid


@register_class
class ConstantValue(Parameter):
    class_id = UUID("0d010101-0101-3d00-060e-2b3402060101")
    __slots__ = ()
    def __init__(self, parameterdef=None, value=None):
        if parameterdef is not None:
            self.parameterdef = parameterdef

        if value is not None:
            if parameterdef is None:
                raise ValueError("need parameterdef to initialize value")
            self.value = value

    @property
    def typedef(self):
        return self.parameterdef.typedef

    @property
    def value(self):
        return self['Value'].value

    @value.setter
    def value(self, value):
        self['Value'].add_pid_entry()
        self['Value'].data = self['Value'].typedef.encode(value, self.typedef)
        self['Value'].mark_modified()


@register_class
class VaryingValue(Parameter):
    class_id = UUID("0d010101-0101-3e00-060e-2b3402060101")
    __slots__ = ()
