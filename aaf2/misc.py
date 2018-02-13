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
