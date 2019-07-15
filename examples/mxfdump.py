from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2 import mxf
import sys

path = sys.argv[1]
f = mxf.MXFFile(path)
f.dump()
