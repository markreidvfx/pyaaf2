from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2 import properties


def test_mangle():

    for item, pid, size in (('tessdsdsddssssssssssttwtestestst',1000, 32),
                            ('tesstwtestst',1000, 32),
                            ('TaggedValueAttributeList', 0xffd0, 32-10)):

        result = properties.mangle_name(item, pid, size)
        assert len(result) <= size


if __name__ == "__main__":
    test_mangle()
