
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
