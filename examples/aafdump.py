from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import aaf2
import sys

with aaf2.open(sys.argv[1], 'r') as f:
    f.dump()
