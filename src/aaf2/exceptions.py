from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

class AAFError(Exception):
    pass

class AAFAttachError(AAFError):
    pass

class AAFPropertyError(AAFError):
    pass

class CompoundFileBinaryError(AAFError):
    pass
