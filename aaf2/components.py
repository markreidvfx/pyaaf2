from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from . import core
from .utils import register_class

class Component(core.AAFObject):
    class_id = UUID("0d010101-0101-0200-060e-2b3402060101")

class Segment(Component):
    class_id = UUID("0d010101-0101-0300-060e-2b3402060101")

@register_class
class Sequence(Segment):
    class_id = UUID("0d010101-0101-0f00-060e-2b3402060101")

@register_class
class NestedScope(Segment):
    class_id = UUID("0d010101-0101-0b00-060e-2b3402060101")

class SourceReference(Segment):
    class_id = UUID("0d010101-0101-1000-060e-2b3402060101")

@register_class
class SourceClip(SourceReference):
    class_id = UUID("0d010101-0101-1100-060e-2b3402060101")
