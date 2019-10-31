from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import aaf2
import sys

out_file = "link_external_mxf_with_changes_0780GI0.aaf"
with aaf2.open(out_file, 'w') as f:
    for path in sys.argv[1:]:
        for mob in f.content.link_external_mxf(path):
            print(mob.name)
