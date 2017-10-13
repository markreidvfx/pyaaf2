from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from struct import unpack, pack
import uuid

def read_u8(f):
    return unpack("B", f.read(1))[0]

def write_u8(f, value):
    f.write(pack("B", value))

def read_u16le(f):
    return unpack("<H", f.read(2))[0]

def write_u16le(f, value):
    f.write(pack("<H", value))

def read_u32le(f):
    return unpack("<I", f.read(4))[0]

def write_u32le(f, value):
    return f.write(pack("<I", value))

def read_u64le(f):
    return unpack("<Q", f.read(8))[0]

def write_u64le(f, value):
    return f.write(pack("<Q", value))

def read_sid(f):
    sid = read_u32le(f)
    if sid in (0xFFFFFFFF,):
        return None
    return sid

def write_sid(f, value):
    if value is None:
        value = 0xFFFFFFFF
    write_u32le(f, value)

def read_uuid(f):
    data = f.read(16)
    return uuid.UUID(bytes_le=data)

def write_uuid(f, value):
    if value is None:
        f.write(b'\0' * 16)
    else:
        f.write(value.bytes_le)

def read_filetime(f):
    return read_u64le(f)

def write_filetime(f, value):
    write_u64le(f, value)

def int_from_bytes(data, endianess='little'):
    num = 0
    if endianess == 'little':
        length = len(data) - 1
        for i, byte in enumerate(data):
            num += byte << ((length-i) * 8)
        return num
    elif endianess == 'big':
        for i, byte in enumerate(data):
            num += byte << (i * 8)
        return num
    else:
        raise ValueError('endianess must be "little" or "big"')

def bytes_from_int(num, length, endianess='little'):
    if endianess == 'little':
        v = bytearray((num >> (length - 1 - i) * 8) & 0xff for i in range(length))
        return bytes(v)
    elif endianess == 'big':
        v = bytearray((num >> (i * 8) & 0xff for i in range(length)))
        return bytes(v)
    else:
        raise ValueError('endianess must be "little" or "big"')


def squeeze_name(name, size):
    if len(name) <= size:
        return name

    half = size//2
    new_name = ""
    for i in range(size):
        if i < half:
            ch = name[i]
        elif i == half:
            ch = '-'
        else:
            ch = name[len(name) - (size-i)]
        new_name += ch

    return new_name

def mangle_name(name, pid, size):
    p = "%x" % pid
    max_size = size - len(p) - 1 -1
    new_name = squeeze_name(name, max_size)
    return "%s-%s" % (new_name, p)

AAFClaseID_dict = {}
AAFClassName_dict = {}
def register_class(classobj):
    AAFClaseID_dict[classobj.class_id] = classobj
    AAFClassName_dict[classobj.__name__] = classobj

    return classobj

def rescale(value, current_rate, new_rate):
    return (float(value) * float(new_rate)) / float(current_rate)
