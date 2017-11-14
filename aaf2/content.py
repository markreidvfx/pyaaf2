from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from . import core
from .utils import register_class
from . import mobs
from . import mxf

@register_class
class ContentStorage(core.AAFObject):
    class_id = UUID("0d010101-0101-1800-060e-2b3402060101")

    @property
    def mobs(self):
        return self['Mobs']

    def toplevel(self):
        for mob in self.compositionmobs():
            if mob.usage == 'Usage_TopLevel':
                yield mob

    def mastermobs(self):
        for mob in self.mobs:
            if isinstance(mob, mobs.MasterMob):
                yield mob

    def compositionmobs(self):
        for mob in self.mobs:
            if isinstance(mob, mobs.CompositionMob):
                yield mob

    def sourcemobs(self):
        for mob in self.mobs:
            if isinstance(mob, mobs.SourceMob):
                yield mob

    def link_mxf(self, path):
        m = mxf.MXFFile(path)
        m.link(self.root)

    @property
    def essencedata(self):
        return self["EssenceData"]
