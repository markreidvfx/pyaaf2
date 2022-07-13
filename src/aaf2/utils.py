from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import sys
from struct import unpack, pack
from . import auid

def read_u8(f):
    (result, ) = unpack(b"B", f.read(1))
    return result

def write_u8(f, value):
    f.write(pack(b"B", value))

def read_u16le(f):
    (result, ) = unpack(b"<H", f.read(2))
    return result

def read_u16be(f):
    (result, ) = unpack(b">H", f.read(2))
    return result

def write_u16le(f, value):
    f.write(pack(b"<H", value))

def read_u32le(f):
    (result, ) = unpack(b"<I", f.read(4))
    return result

def read_u32be(f):
    (result, ) = unpack(b">I", f.read(4))
    return result

def read_s32be(f):
    (result, ) = unpack(b">i", f.read(4))
    return result

def write_u32le(f, value):
    return f.write(pack(b"<I", value))

def read_u64le(f):
    (result, ) = unpack(b"<Q", f.read(8))
    return result

def read_u64be(f):
    (result, ) = unpack(b">Q", f.read(8))
    return result

def read_s64be(f):
    (result, ) = unpack(b">q", f.read(8))
    return result

def write_u64le(f, value):
    return f.write(pack(b"<Q", value))

def decode_sid(sid):
    if sid in (0xFFFFFFFF,):
        return None
    return sid

def read_sid(f):
    sid = read_u32le(f)
    return decode_sid(sid)

def encode_sid(sid):
    if sid is None:
        return 0xFFFFFFFF
    return sid

def write_sid(f, value):
    value = encode_sid(value)
    write_u32le(f, value)

def read_filetime(f):
    return read_u64le(f)

def decode_utf16le(data):
    if sys.version_info.major < 3:
        return data.decode('utf-16le').split(u'\x00')[0]
    else:
        return data.decode('utf-16le', 'backslashreplace').split(u'\x00')[0]

def encode_utf16le(data):
    return data.encode("utf-16le") + b"\x00\x00"

def encode_u16le(value):
    return pack(b"<H", value)

def encode_u32le(value):
    return pack(b"<I", value)

def encode_u8(value):
    return pack(b"B", value)

def encode_utf16_array(data):
    result = b""
    for item in data:
        result += encode_utf16le(item)
    return result

def encode_auid_array(values):
    result = b""
    for item in values:
        if not isinstance(item, auid.AUID):
            item = auid.AUID(item)
        result += item.bytes_le
    return result

def str2auid(value):
    if isinstance(value, auid.AUID):
        return value

    if value is None:
        return value

    if len(value) < 32:
        return value

    try:
        return auid.AUID(value)
    except:
        return value

def encode_s64le(value):
    return pack(b"<q", value)

def write_filetime(f, value):
    write_u64le(f, value)

def unpack_u16le_from(buffer, offset):
    value  = buffer[offset]
    value += buffer[offset+1] << 8
    return value

def unpack_u32le_from(buffer, offset):
    value  = buffer[offset]
    value += buffer[offset+1] << 8
    value += buffer[offset+2] << 16
    value += buffer[offset+3] << 24
    return value

def unpack_u64le_from(buffer, offset):
    value  = buffer[offset]
    value += buffer[offset+1] << 8
    value += buffer[offset+2] << 16
    value += buffer[offset+3] << 24
    value += buffer[offset+4] << 32
    value += buffer[offset+5] << 40
    value += buffer[offset+6] << 48
    value += buffer[offset+7] << 56
    return value

def int_from_bytes(data, byte_order='big'):
    num = 0
    if byte_order == 'little':
        for i, byte in enumerate(data):
            num += byte << (i * 8)
        return num
    elif byte_order == 'big':
        length = len(data) - 1
        for i, byte in enumerate(data):
            num += byte << ((length-i) * 8)
        return num
    else:
        raise ValueError('endianness must be "little" or "big"')

def bytes_from_int(num, length, byte_order='big'):
    if byte_order == 'little':
        v = bytearray((num >> (i * 8) & 0xff for i in range(length)))
        return bytes(v)
    elif byte_order == 'big':
        v = bytearray((num >> (length - 1 - i) * 8) & 0xff for i in range(length))
        return bytes(v)
    else:
        raise ValueError('endianness must be "little" or "big"')


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

def safe_print(*args):
    # python 2.7
    if bytes is str:
        s = u' '.join([unicode(item) for item in args])
        print(s.encode('utf-8'))
    else:
        print(*args)

AAFClaseID_dict = {}
AAFClassName_dict = {}
def register_class(classobj):
    AAFClaseID_dict[classobj.class_id] = classobj
    AAFClassName_dict[classobj.__name__] = classobj

    return classobj

def rescale(value, current_rate, new_rate):
    return (float(value) * float(new_rate)) / float(current_rate)
