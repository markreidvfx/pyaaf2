from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import traceback

from . import core
from . mobid import MobID
from uuid import UUID
from .utils import register_class

@register_class
class EssenceData(core.AAFObject):
    class_id = UUID("0d010101-0101-2300-060e-2b3402060101")

    @property
    def unique_key(self):
        return self.id

    @property
    def id(self):
        return self['MobID'].value

    @id.setter
    def id(self, value):
        self['MobID'].value = value

    def open(self, mode='r'):
        return self['Data'].open(mode)
