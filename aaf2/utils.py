from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from struct import unpack, pack
import uuid

def read_u8(f):
    return unpack(b"B", f.read(1))[0]

def write_u8(f, value):
    f.write(pack(b"B", value))

def read_u16le(f):
    return unpack(b"<H", f.read(2))[0]

def read_u16be(f):
    return unpack(b">H", f.read(2))[0]

def write_u16le(f, value):
    f.write(pack(b"<H", value))

def read_u32le(f):
    return unpack(b"<I", f.read(4))[0]

def read_u32be(f):
    return unpack(b">I", f.read(4))[0]

def read_s32be(f):
    return unpack(b">i", f.read(4))[0]

def write_u32le(f, value):
    return f.write(pack(b"<I", value))

def read_u64le(f):
    return unpack(b"<Q", f.read(8))[0]

def read_u64be(f):
    return unpack(b">Q", f.read(8))[0]

def read_s64be(f):
    return unpack(b">q", f.read(8))[0]

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

def read_uuid(f):
    data = f.read(16)
    if data:
        return uuid.UUID(bytes_le=data)

def write_uuid(f, value):
    if value is None:
        f.write(b'\0' * 16)
    else:
        f.write(value.bytes_le)

def read_filetime(f):
    return read_u64le(f)

def decode_utf16le(data):
    return data.decode('utf-16le').rstrip('\x00')

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

def encode_uuid_array(values):
    result = b""
    for item in values:
        if not isinstance(item, uuid.UUID):
            item = uuid.UUID(item)
        result += item.bytes_le
    return result

def str2uuid(value):
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(value)
    except:
        return value

def encode_s64le(value):
    return pack(b"<q", value)

def write_filetime(f, value):
    write_u64le(f, value)

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
        raise ValueError('endianess must be "little" or "big"')

def bytes_from_int(num, length, byte_order='big'):
    if byte_order == 'little':
        v = bytearray((num >> (i * 8) & 0xff for i in range(length)))
        return bytes(v)
    elif byte_order == 'big':
        v = bytearray((num >> (length - 1 - i) * 8) & 0xff for i in range(length))
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
