from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import traceback
from StringIO import StringIO

from . import core
from . mobid import MobID
from uuid import UUID
from .utils import register_class

@register_class
class Mob(core.AAFObject):
    class_id = UUID("0d010101-0101-3400-060e-2b3402060101")

    @property
    def unique_key(self):
        return self.mob_id

    @property
    def mob_id(self):
        return self['MobID'].value

    @mob_id.setter
    def mob_id(self, value):
        self['MobID'].value = value

@register_class
class CompositionMob(Mob):
    class_id = UUID("0d010101-0101-3500-060e-2b3402060101")

@register_class
class MasterMob(Mob):
    class_id = UUID("0d010101-0101-3600-060e-2b3402060101")

@register_class
class SourceMob(Mob):
    class_id = UUID("0d010101-0101-3700-060e-2b3402060101")
