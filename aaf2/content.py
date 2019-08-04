from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from . import core
from .utils import register_class
from . import mobs
from . import mxf
from . import ama
from . import audio
from .auid import AUID

@register_class
class Header(core.AAFObject):
    class_id = AUID("0d010101-0101-2f00-060e-2b3402060101")
    __slots__ = ()

@register_class
class ContentStorage(core.AAFObject):
    """
    This object has all ``Mob`` and ``EssenceData`` objects in the file
    """

    class_id = AUID("0d010101-0101-1800-060e-2b3402060101")
    __slots__ = ()

    @property
    def mobs(self):
        """
        Access to all the ``Mobs`` objects in the aaf file.
        """
        return self['Mobs']

    def toplevel(self):
        """
        Convenience generator method that yields only TopLevel :class:`aaf2.mobs.CompositionMob` objects.
        """
        for mob in self.compositionmobs():
            if mob.usage == 'Usage_TopLevel':
                yield mob

    def mastermobs(self):
        """
        Convenience generator method that yields only :class:`aaf2.mobs.MasterMob` objects.
        """
        for mob in self.mobs:
            if isinstance(mob, mobs.MasterMob):
                yield mob

    def compositionmobs(self):
        """
        Convenience generator method that yields only :class:`aaf2.mobs.CompositionMob` objects.
        """

        for mob in self.mobs:
            if isinstance(mob, mobs.CompositionMob):
                yield mob

    def sourcemobs(self):
        """
        Convenience generator method that yields only :class:`aaf2.mobs.SourceMob` objects.
        """

        for mob in self.mobs:
            if isinstance(mob, mobs.SourceMob):
                yield mob

    def link_external_mxf(self, path):
        m = mxf.MXFFile(path)
        if m.operation_pattern != "OPAtom":
            raise Exception("can only link OPAtom mxf files")
        return m.link(self.root)

    def link_external_wav(self, metadata):
        """
        Create a link source MOB to a wav file, along with a corresponding master MOB and tape MOB.

        Returns a 3-tuple: a master mob, the source MOB whose essence is a WAVEDescriptor link,
        and a source MOB whose essence is a TapeDescriptor.
        """
        path = metadata['format']['filename']
        return self.create_ama_link(path, metadata)

    def create_ama_link(self, path, metadata):
        return ama.create_media_link(self.root, path, metadata)

    @property
    def essencedata(self):
        """
        Access to :class:`aaf2.essence.EssenceData` objects in the aaf file.
        """
        return self["EssenceData"]
