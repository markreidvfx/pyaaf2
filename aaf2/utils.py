
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
    return uuid.UUID(bytes_le=f.read(16))

def write_uuid(f, value):
    if value is None:
        f.write('\0' * 16)
    else:
        f.write(value.bytes_le)

def read_filetime(f):
    return read_u64le(f)

def write_filetime(f, value):
    write_u64le(f, value)
