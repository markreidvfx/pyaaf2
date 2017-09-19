from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from . import core
from .utils import register_class

@register_class
class ContentStorage(core.AAFObject):
    class_id = UUID("0d010101-0101-1800-060e-2b3402060101")
