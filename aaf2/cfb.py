from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import logging

import sys
import os
import uuid
import io
import math
import weakref
from array import array
from struct import Struct
import struct

from .utils import (
    read_u8, read_u16le,
    read_u32le, read_u64le,
    read_filetime, read_sid, read_uuid,
    write_u8, write_u16le,
    write_u32le, write_u64le,
    write_filetime, write_sid, write_uuid,
    decode_utf16le,
    decode_sid, encode_sid,
    unpack_u16le_from, unpack_u32le_from, unpack_u64le_from
)
from .exceptions import CompoundFileBinaryError
from .cache import LRUCacheDict

from io import BytesIO

dir_types = {0x00 : 'empty',
             0x01 : 'storage',
             0x02 : 'stream',
             0x03 : 'lock bytes',
             0x04 : 'property',
             0x05 : 'root storage'}

DIFSECT    = 0xFFFFFFFC
FATSECT    = 0xFFFFFFFD
ENDOFCHAIN = 0xFFFFFFFE
FREESECT   = 0xFFFFFFFF

RANGELOCKSECT = (0x7FFFFF00 // 4096) - 1

MAXREGSECT = 0xFFFFFFFA
MAXREGSID  = 0xFFFFFFFA
MAX_DIR_ENTRIES = 0x00FFFFFF

fat_sector_types = {DIFSECT    : "DIFSECT",
                    FATSECT    : "FATSECT",
                    ENDOFCHAIN : "ENDOFCHAIN",
                    FREESECT   : "FREESECT"}

DIR_STRUCT = Struct(str(''.join(( '<',
    '64s', # name 0
    'H',   # name_size 64
    'B',   # dir_type 66
    'B',   # color 67
    'I',   # left_id 68
    'I',   # right_id 72
    'I',   # child_id 76
    '16s', # class_id 80
    'I',   # flags 96
    'Q',   # create_time 100
    'Q',   # modify_time 108
    'I',   # sector_id 116
    'Q',   # byte_size 120
))))

def pretty_sectors(fat):
    return [fat_sector_types.get(item, item) for item in fat]

class Stream(object):

    def __init__(self, storage, entry, mode='r'):
        self.storage = storage
        self.dir = entry
        self.mode = mode
        self.pos = 0
        self.fat_chain = array(str('I'))
        if not mode in ('r', 'w'):
            raise ValueError("invalid mode: %s" % mode)
        if self.dir.sector_id is not None:
            self.fat_chain.extend(self.storage.get_fat_chain(self.dir.sector_id, self.is_mini_stream()))

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_CUR:
            offset = self.tell() + offset
        elif whence == io.SEEK_END:
            offset = self.dir.byte_size + offset
        if offset < 0:
            raise ValueError('New position is before the start of the stream')

        if offset > self.dir.byte_size:
            # logging.debug("overseek %d bytes, padding with zeros" % (offset - self.dir.byte_size))
            self.pos = self.dir.byte_size
            bytes_left = offset - self.dir.byte_size
            min_seek_size = self.storage.sector_size * 4
            while bytes_left:
                bytes_to_write = min(min_seek_size, offset - self.dir.byte_size)
                zeros = bytearray(bytes_to_write)
                self.write(zeros)
                bytes_left -= bytes_to_write

        self.pos = offset
        return offset

    def is_mini_stream(self):
        return self.dir.byte_size < self.storage.min_stream_max_size

    def sector_size(self):
        if self.is_mini_stream():
            return self.storage.mini_stream_sector_size
        else:
            return self.storage.sector_size

    def sector_offset(self):
        return self.pos % self.sector_size()

    def sector_index(self):
        return self.pos // self.sector_size()

    def abs_pos(self):
        minifat = self.is_mini_stream()
        sector_size = self.storage.sector_size
        mini_sector_size = self.storage.mini_stream_sector_size

        if minifat:
            minifat_chain = self.fat_chain
            mini_fat_index, sector_offset = divmod(self.pos, mini_sector_size)
            mini_stream_sid = minifat_chain[mini_fat_index]
            mini_steam_pos = (mini_stream_sid * mini_sector_size) + sector_offset

            index, offset  = divmod(mini_steam_pos, sector_size)
            sid = self.storage.mini_stream_chain[index]
            seek_pos = ((sid + 1) *  sector_size) + offset
            return seek_pos
        else:
            fat_chain = self.fat_chain
            index, offset  = divmod(self.pos, sector_size)

            sid = fat_chain[index]
            seek_pos = ((sid + 1) *  sector_size) + offset
            return seek_pos

    def readinto1(self, buf, n=-1):
        if n == -1:
            n = max(0, self.dir.byte_size - self.tell())
        else:
            n = max(0, min(n, self.dir.byte_size - self.tell()))

        sector_size = self.storage.sector_size
        mini_sector_size = self.storage.mini_stream_sector_size

        # inlined on purpose this method gets called alot
        if self.dir.byte_size < self.storage.min_stream_max_size:
            mini_fat_index = self.pos // mini_sector_size
            sector_offset  = self.pos % mini_sector_size

            mini_stream_sid = self.fat_chain[mini_fat_index]
            mini_steam_pos  = (mini_stream_sid * mini_sector_size) + sector_offset

            index      = mini_steam_pos // sector_size
            sid_offset = mini_steam_pos % sector_size

            sid = self.storage.mini_stream_chain[index]

            sector_size = mini_sector_size

        else:
            sector_size = self.storage.sector_size
            index       = self.pos // sector_size
            sid_offset  = self.pos % sector_size

            sid = self.fat_chain[index]
            sector_offset = sid_offset

        n = min(n, sector_size - sector_offset, len(buf))
        if n == 0:
            return 0

        sector_data = self.storage.read_sector_data(sid)
        buf[:n] = sector_data[sid_offset:sid_offset+n]

        self.pos += n
        return n

    def read(self, n=-1):
        if n == -1:
            n = max(0, self.dir.byte_size - self.tell())
        else:
            n = max(0, min(n, self.dir.byte_size - self.tell()))

        result = bytearray(n)
        mv = memoryview(result)
        i = 0
        while i < n:
            bytes_read = self.readinto1(mv[i:], n - i)
            if bytes_read <= 0:
                logging.warn('file appears to be truncated')
                break
            i += bytes_read

        return result

    def write1(self, data):
        sector_size = self.sector_size()
        sector_offset = self.sector_offset()

        byte_writeable = min(len(data), sector_size - sector_offset)
        f = self.storage.f
        pos = self.abs_pos()
        sid, sid_offset = self.storage.get_sid_offset(pos)

        if sid in self.storage.sector_cache:
            del self.storage.sector_cache[sid]

        f.seek(pos)
        # logging.debug("write stream %d bytes at %d" % (byte_writeable, pos))
        f.write(data[:byte_writeable])
        self.pos += byte_writeable

        return byte_writeable

    def allocate(self, byte_size):

        minifat = self.is_mini_stream()
        realloc_data = None

        # convert from minifat to fat
        if minifat and byte_size >= self.storage.min_stream_max_size:
            logging.debug("converting stream for minifat to fat")
            self.seek(0)
            realloc_data = self.read()
            assert len(realloc_data) == self.dir.byte_size
            self.pos = 0
            self.storage.free_fat_chain(self.dir.sector_id, True)
            self.dir.sector_id = None
            minifat = False
            self.fat_chain = array(str('I'))

        self.dir.byte_size = byte_size
        sector_count = int(math.ceil(byte_size / float(self.sector_size())))

        current_sects= len(self.fat_chain)
        # logging.debug("%d bytes requires %d sectors at %d has %d" % (byte_size, sector_count, self.sector_size(), current_sects))

        while len(self.fat_chain) < sector_count:
            last_sector_id = self.fat_chain[-1] if self.fat_chain else None
            sid = self.storage.fat_chain_append(last_sector_id, minifat)
            self.fat_chain.append(sid)
            if self.dir.sector_id is None:
                self.dir.sector_id = sid

        if not realloc_data is None:
            self.seek(0)
            self.write(realloc_data)

    def write(self, data):
        size = len(data)
        new_size = max(self.tell() + size, self.dir.byte_size)
        if new_size > self.dir.byte_size:
            self.allocate(new_size)

        while data:
            bytes_written = self.write1(data)
            data = data[bytes_written:]

        return size

    def close(self):
        pass

class DirEntry(object):
    __slots__ = ('storage', 'dir_id', 'parent', 'data', '__weakref__')

    def __init__(self, storage, dir_id, data=None):
        self.storage = storage

        self.parent = None
        if data is None:
            self.data = bytearray(128)
            # setting dir_id to None disable mark_modified
            self.dir_id = None
            self.left_id = None
            self.right_id = None
            self.child_id = None
            self.sector_id = None
        else:
            self.data = data

        # mark modified will now work
        self.dir_id = dir_id

    @property
    def name(self):
        name_size = unpack_u16le_from(self.data, 64)
        assert name_size <= 64
        name =  decode_utf16le(self.data[:name_size])
        return name

    @name.setter
    def name(self, value):
        name_data = value.encode("utf-16le")
        name_size = len(name_data)
        assert name_size <= 64
        self.data[:name_size] = name_data
        pad = 64 - name_size
        for i in range(pad):
            self.data[name_size +i] = 0

        # includes null terminator? should re-verify this
        struct.pack_into(str('<H'), self.data, 64, min(name_size+2, 64))
        self.mark_modified()

    @property
    def type(self):
        return dir_types.get(self.data[66] , "unknown")

    @type.setter
    def type(self, value):
        t = None
        for k,v in dir_types.items():
            if v == value:
                t = k
                break
        if t is None:
            raise ValueError("invalid dir type: %s" % str(value))

        self.data[66] = t
        self.mark_modified()

    @property
    def color(self):
        if self.data[67] == 0x01:
            return 'black'
        return 'red'

    @color.setter
    def color(self, value):
        if value == 'black':
            self.data[67] = 0x01
        elif value == 'red':
            self.data[67] = 0x00
        else:
            raise ValueError("invalid dir type: %s" % str(value))

        self.mark_modified()

    @property
    def left_id(self):
        sid = unpack_u32le_from(self.data, 68)
        return decode_sid(sid)

    @left_id.setter
    def left_id(self, value):
        struct.pack_into(str('<I'), self.data, 68, encode_sid(value))
        self.mark_modified()

    @property
    def right_id(self):
        sid = unpack_u32le_from(self.data, 72)
        # sid = struct.unpack_from(str('<I'), bytes(self.data), 72)[0]
        return decode_sid(sid)

    @right_id.setter
    def right_id(self, value):
        struct.pack_into(str('<I'), self.data, 72, encode_sid(value))
        self.mark_modified()

    @property
    def child_id(self):
        sid = unpack_u32le_from(self.data, 76)
        return decode_sid(sid)

    @child_id.setter
    def child_id(self, value):
        struct.pack_into(str('<I'), self.data, 76, encode_sid(value))
        self.mark_modified()

    @property
    def class_id(self):
        value = uuid.UUID(bytes_le=bytes(self.data[80:96]))
        if value.int == 0:
            return None
        return value

    @class_id.setter
    def class_id(self, value):
        if value is None:
            self.data[80:96] = bytearray(16)
        else:
            self.data[80:96] = value.bytes_le
        self.mark_modified()

    @property
    def flags(self):
        flags = unpack_u32le_from(self.data, 96)
        return flags

    @flags.setter
    def flags(self, value):
        struct.pack_into(str('<I'), self.data, 96, value)
        self.mark_modified()

    @property
    def create_time(self):
        value = unpack_u64le_from(self.data, 100)
        return value

    @create_time.setter
    def create_time(self, value):
        struct.pack_into(str('<Q'), self.data, 100, value)
        self.mark_modified()

    @property
    def modify_time(self):
        value = unpack_u64le_from(self.data, 108)
        return value

    @modify_time.setter
    def modify_time(self, value):
        struct.pack_into(str('<Q'), bytes(self.data), 108, value)
        self.mark_modified()

    @property
    def sector_id(self):
        sid = unpack_u32le_from(self.data, 116)
        return decode_sid(sid)

    @sector_id.setter
    def sector_id(self, value):
        struct.pack_into(str('<I'), self.data, 116, encode_sid(value))
        self.mark_modified()

    @property
    def byte_size(self):
        value = unpack_u64le_from(self.data, 120)
        return value

    @byte_size.setter
    def byte_size(self, value):
        struct.pack_into(str('<Q'), self.data, 120, value)
        self.mark_modified()

    def mark_modified(self):
        if self.storage.mode in ('r', 'rb'):
            return

        if self.dir_id is None:
            return

        self.storage.modified[self.dir_id] = self
        if len(self.storage.modified) > 128:
            self.storage.write_modified_dir_entries()

    def __lt__(self, other):
        if isinstance(other, DirEntry):
            other = other.name

        if len(self.name) == len(other):
            # compare not case senstive
            return self.name.upper() < other.upper()
        else:
            # shorter names are always less then
            return len(self.name) < len(other)

    def __le__(self, other):
        if self == other:
            return True
        return self < other

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        if self == other:
            return True
        return self > other

    def __eq__(self, other):
        if other is None:
            return False

        if isinstance(other, DirEntry):
            other = other.name
        if len(self.name) == len(other):
            return self.name.upper() == other.upper()
        return False

    def left(self):
        return self.storage.read_dir_entry(self.left_id, self.parent)

    def right(self):
        return self.storage.read_dir_entry(self.right_id, self.parent)

    def child(self):
        return self.storage.read_dir_entry(self.child_id, self)

    def add_child(self, entry):
        entry.parent = self
        entry.color = 'black'
        child = self.child()
        if child:
            child.insert(entry)
        else:
            self.child_id = entry.dir_id

        if self.dir_id in self.storage.children_cache:
            self.storage.children_cache[self.dir_id][entry.name] = entry

    def pop(self):
        """
        remove self from binary search tree
        """
        entry = self
        parent = self.parent

        root = parent.child()

        dir_per_sector = self.storage.sector_size // 128
        max_dirs_entries = self.storage.dir_sector_count * dir_per_sector
        count = 0

        if root.dir_id == entry.dir_id:
            parent.child_id = None
        else:
            # find dir entry pointing to self
            while True:
                if count > max_dirs_entries:
                    raise CompoundFileBinaryError("max dir entries limit reached")

                if entry < root:
                    if root.left_id == entry.dir_id:
                        root.left_id = None
                        break
                    root = root.left()
                else:
                    if root.right_id == entry.dir_id:
                        # root right is pointing to self
                        root.right_id = None
                        break
                    root = root.right()

                count += 1


        left = entry.left()
        right = entry.right()

        # clear from cache
        if parent.dir_id in self.storage.children_cache:
            del self.storage.children_cache[parent.dir_id][entry.name]
            if left:
                del self.storage.children_cache[parent.dir_id][left.name]
            if right:
                del self.storage.children_cache[parent.dir_id][right.name]

        if left is not None:
            parent.add_child(left)
        if right is not None:
            parent.add_child(right)

        # clear parent and left and right
        self.left_id = None
        self.right_id = None
        self.parent = None

    def insert(self, entry):

        root = self

        dir_per_sector = self.storage.sector_size // 128
        max_dirs_entries = self.storage.dir_sector_count * dir_per_sector

        count = 0
        entry.color = 'black'

        # avoids recursion
        while True:
            if count > max_dirs_entries:
                raise CompoundFileBinaryError("max dir entries limit reached")

            if entry < root:
                left = root.left()
                if left:
                    root = left
                else:
                    root.left_id = entry.dir_id
                    entry.parent = self.parent
                    break
            else:
                right = root.right()
                if right:
                    root = right
                else:
                    root.right_id = entry.dir_id
                    entry.parent = self.parent
                    break
            count += 1

        # resucive version
        # if entry < self:
        #     left = self.left()
        #     if left:
        #         left.insert(entry)
        #     else:
        #         self.left_id = entry.dir_id
        # else:
        #     right = self.right()
        #     if right:
        #         right.insert(entry)
        #     else:
        #         self.right_id = entry.dir_id

    def path(self):
        path = []
        parent = self
        while parent:
            name = parent.name
            if name == "Root Entry":
                break
            path.append(parent.name)
            parent= parent.parent
        return  '/' + '/'.join(reversed(path))

    def open(self, mode='r'):
        if self.type != 'stream':
            raise TypeError("can only open streams")
        return self.storage.open(self, mode)

    def isdir(self):
        return self.type in ('storage', 'root storage')

    def isroot(self):
        return self.type == 'root storage'

    def listdir(self):
        return self.storage.listdir(self)

    def makedir(self, relative_path, class_id = None):
        if not self.isdir():
            raise TypeError("can only add a DirEntry to a storage type")
        sep = '/'
        if self.isroot():
            sep = ''

        path = self.path() + sep + relative_path
        return self.storage.makedir(path, class_id)

    def isfile(self):
        return self.type == 'stream'

    def get(self, name, default=None):
        dir_dict = self.storage.listdir_dict(self)
        return dir_dict.get(name, default)

    def touch(self, name):
        item = self.get(name, None)
        if item:
            return item

        sep = '/'
        if self.isroot():
            sep = ''

        path = self.path() + sep + name
        return self.storage.create_dir_entry(path, 'stream', None)

    def write(self):
        f = self.storage.f
        f.seek(self.storage.dir_entry_pos(self.dir_id))
        f.write(self.data)

    def read(self):
        f = self.storage.f
        f.seek(self.storage.dir_entry_pos(self.dir_id))
        f.readinto(self.data)

    def __repr__(self):
        return self.name

def extend_sid_table(f, table, byte_size):
    n = byte_size // 4
    if isinstance(f, io.RawIOBase):
        table.fromfile(f, n)
    elif hasattr(table, 'frombytes'):
        table.frombytes(f.read(byte_size))
    else:
        # try deprecated from string
        table.fromstring(f.read(byte_size))

class CompoundFileBinary(object):
    def __init__(self, file_object, mode='rb', sector_size=4096):

        self.f = file_object

        self.difat = [[]]
        self.fat = array(str('I'))
        self.fat_freelist = array(str('I'))

        self.minifat = array(str('I'))
        self.minifat_freelist = array(str('I'))

        self.difat_chain = []
        self.minifat_chain = []
        self.dir_fat_chain = []

        self.mini_stream_chain = []

        self.modified = {}

        self.sector_cache = LRUCacheDict(size=1024)
        self.dir_cache = weakref.WeakValueDictionary()
        self.children_cache = LRUCacheDict()
        self.dir_freelist = array(str('I'))

        self.debug_grow = False
        self.is_open = True

        if isinstance(self.f, BytesIO):
            self.mode = 'wb+'
        else:
            self.mode = mode

        if self.mode in ("r", "r+", "rb", 'rb+'):

            self.read_header()
            self.read_fat()
            self.read_minifat()

            # create dir_fat_chain and read root dir entry
            self.dir_fat_chain = self.get_fat_chain(self.dir_sector_start)
            if len(self.dir_fat_chain) != self.dir_sector_count:
                logging.info("read dir_sector_count missmatch, using fat chain length")
                self.dir_sector_count = len(self.dir_fat_chain)

            logging.debug("read %d dir sectors" % len(self.dir_fat_chain))
            self.root = self.read_dir_entry(0)
            self.dir_cache[0] = self.root

            # create mini stream fat chain
            if self.minifat_sector_count:
                self.mini_stream_chain = self.get_fat_chain(self.root.sector_id)
        else:
            self.setup_empty(sector_size)
            self.write_header()

            logging.debug("pos: %d" % self.f.tell())

            logging.debug("writing root dir sector")
            self.root.write()
            for i in range(self.sector_size - 128):
                self.f.write(b'\0')

            self.write_fat()

    def close(self):
        if self.mode in ("r", "rb"):
            return

        self.write_header()
        self.write_difat()
        self.write_fat()
        self.write_minifat()
        self.write_dir_entries()
        self.is_open = False

    def setup_empty(self, sector_size):

        if sector_size == 4096:
            self.class_id = uuid.UUID("0d010201-0200-0000-060e-2b3403020101")
        elif sector_size == 512:
            self.class_id = uuid.UUID("42464141-000d-4d4f-060e-2b34010101ff")
        else:
            raise ValueError("sector size must be 4096 or 512")

        self.major_version = 4
        self.minor_version =  62

        self.byte_order = "le"

        self.sector_size = sector_size
        self.mini_stream_sector_size = 64

        self.dir_sector_count = 1
        self.fat_sector_count = 1
        self.dir_sector_start = 0

        self.transaction_signature = 1
        self.min_stream_max_size = 4096

        self.minifat_sector_start = FREESECT
        self.minifat_sector_count = 0

        self.difat_sector_start = FREESECT
        self.difat_sector_count = 0

        self.difat = [[]]
        for i in range(109):
            self.difat[0].append(FREESECT)

        self.difat[0][0] = 1

        for i in range(self.sector_size // 4):
            self.fat.append(FREESECT)
            if i > 1:
                self.fat_freelist.append(i)

        self.fat[0] = ENDOFCHAIN # end of dir chain
        self.fat[self.difat[0][0]] = FATSECT

        self.root = DirEntry(self, 0)
        self.root.name = 'Root Entry'
        self.root.sector_id = None
        self.root.type = 'root storage'
        self.root.class_id = uuid.UUID("b3b398a5-1c90-11d4-8053-080036210804")

        self.dir_cache[0] = self.root

        self.dir_fat_chain = [0]

        # raise NotImplementedError("mode: %s supported not implemented" % self.f.mode)

    def write_header(self):
        logging.debug("writiing header")
        f = self.f
        f.seek(0)
        f.write(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1') # Magic
        write_uuid(f, self.class_id)
        write_u16le(f, self.minor_version)
        write_u16le(f, self.major_version)
        write_u16le(f, 0xFFFE) #byte order le
        write_u16le(f, int(math.log(self.sector_size, 2)))
        write_u16le(f, int(math.log(self.mini_stream_sector_size, 2)))
        f.write(b'\0' * 6) #skip reseverd

        write_u32le(f, self.dir_sector_count)
        write_u32le(f, self.fat_sector_count)
        write_u32le(f, self.dir_sector_start)
        write_u32le(f, self.transaction_signature)
        write_u32le(f, self.min_stream_max_size)

        write_u32le(f, self.minifat_sector_start)
        write_u32le(f, self.minifat_sector_count)

        write_u32le(f, self.difat_sector_start)
        write_u32le(f, self.difat_sector_count)

        for i in range(109):
            write_u32le(f, self.difat[0][i])

        for i in range(self.sector_size - f.tell()):
            f.write(b'\0')


    def read_header(self):

        f = self.f
        f.seek(0)

        magic = f.read(8)
        # logging.debug("magic: %s" % magic.encode("hex"))
        logging.debug("magic: %s" % str([magic]))

        # clsid = f.read(16)
        # logging.debug("clsid: %s" % clsid.encode("hex"))
        self.class_id = read_uuid(f)
        logging.debug("clsid: %s" % str(self.class_id))

        self.minor_version = read_u16le(f)
        logging.debug("minor_version: %d" % self.minor_version)

        self.major_version = read_u16le(f)
        logging.debug("major_version: %d" % self.major_version)

        byte_order = read_u16le(f)
        if byte_order == 0xFFFE:
            self.byte_order = 'le'
        else:
            raise NotImplementedError("endian format:0x%X not supported" % byte_order)

        logging.debug("byte_order: %s" % self.byte_order)

        size = read_u16le(f)
        self.sector_size = pow(2, size)
        logging.debug("sector_size: %d -> %d" % (size, self.sector_size))

        size = read_u16le(f)
        self.mini_stream_sector_size = pow(2, size)
        logging.debug("mini_stream_sector_size: %d -> %d" % (size, self.mini_stream_sector_size))

        if not self.sector_size in (4096, 512):
            raise NotImplementedError("unsupported sector size: %d" % self.sector_size)
        if self.mini_stream_sector_size != 64:
            raise NotImplementedError("unsupported mini sector size: %d" % self.mini_stream_sector_size)

        f.read(6) #skip reseverd

        self.dir_sector_count = read_u32le(f)
        logging.debug("dir_sector_count: %d" % self.dir_sector_count)

        self.fat_sector_count = read_u32le(f)
        logging.debug("fat_sector_count: %d" % self.fat_sector_count)

        self.dir_sector_start = read_u32le(f)
        logging.debug("dir_sector_start: %d" % self.dir_sector_start)

        self.transaction_signature = read_u32le(f)
        logging.debug("transaction_signature: %d" % self.transaction_signature)

        self.min_stream_max_size = read_u32le(f)
        logging.debug("min_stream_max_size: %d" % self.min_stream_max_size)

        self.minifat_sector_start = read_u32le(f)
        logging.debug("minifat_sector_start: %d" % self.minifat_sector_start)

        self.minifat_sector_count = read_u32le(f)
        logging.debug("minifat_sector_count: %d" % self.minifat_sector_count)

        self.difat_sector_start = read_u32le(f)
        logging.debug("difat_sector_start: %d" % self.difat_sector_start)

        self.difat_sector_count = read_u32le(f)
        logging.debug("difat_sector_count: %d" % self.difat_sector_count)

        self.difat = [[]]

        logging.debug("reading header difat at %d" % f.tell())
        for i in range(109):
            item = read_u32le(f)
            # item = fat_sector_types.get(item, item)
            self.difat[0].append(item)

        sectors_left = self.difat_sector_count

        sid = self.difat_sector_start

        # reading difat sectors
        while sectors_left:
            logging.debug("reading difat sid: %d", sid)
            sector_type = fat_sector_types.get(sid, sid)
            if not isinstance(sector_type, int):
                break

            self.difat_chain.append(sid)
            f.seek((sid + 1) *  self.sector_size)
            difat = []
            for i in range( (self.sector_size // 4)):
                item = read_u32le(f)
                difat.append(item)
            self.difat.append(difat)

            sid = difat[-1]
            logging.debug("next difat: %d" % sid)
            sectors_left -= 1

    def iter_difat(self):
        for i, sid in enumerate(self.difat[0]):
            yield 0, i, sid

        t = 1
        for item in self.difat[1:]:
            for i, sid in enumerate(item[:-1]):
                yield t, i, sid
            t+=1


    def write_difat(self):
        f = self.f
        # write header entries
        f.seek(76)

        logging.debug("writing header difat")
        for i in range(109):
            write_u32le(f, self.difat[0][i])

        for i in range(self.sector_size - f.tell()):
            f.write(b'\0')

        if self.difat_sector_count == 0:
            return

        sid = self.difat_sector_start
        assert len(self.difat[1:]) == self.difat_sector_count
        for table in self.difat[1:]:

            sector_type = fat_sector_types.get(sid, sid)
            if not isinstance(sector_type, int):
                raise IOError("bad difat sector type")

            pos = (sid + 1) * self.sector_size
            logging.debug("writing difat to sid: %d at: %d" % (sid,pos))
            f.seek(pos)
            for i in range(self.sector_size // 4):
                write_u32le(f, table[i])

            sid = table[-1]

    def read_fat(self):
        f = self.f
        self.fat = array(str('I'))
        sector_count = 0
        fat_sectors = []
        for t, i, sid in self.iter_difat():

            sector_type = fat_sector_types.get(sid, sid)
            if not isinstance(sector_type, int):

                continue
            fat_sectors.append(sid)

        #  len(fat_sectors),self.fat_sector_count
        # assert len(fat_sectors) == self.fat_sector_count
        if len(fat_sectors) != self.fat_sector_count:
            logging.warn("fat sector count missmatch difat: %d header: %d" % (len(fat_sectors), self.fat_sector_count))
            self.fat_sector_count = len(fat_sectors)

        for sid in fat_sectors:
            pos = (sid + 1) *  self.sector_size
            f.seek(pos)
            extend_sid_table(f, self.fat, self.sector_size)
            sector_count += 1

        if sys.byteorder == 'big':
            self.fat.byteswap()

        for i,v in enumerate(self.fat):
            if v == FREESECT:
                self.fat_freelist.append(i)

        logging.debug("read %d fat sectors ", sector_count)

        if self.sector_size == 4096 and len(self.fat) > RANGELOCKSECT:
            if self.fat[RANGELOCKSECT] != ENDOFCHAIN:
                logging.warn("range lock sector has data")

        # logging.debug("fat: %s" % str(pretty_sectors(self.fat)))

    def write_fat(self):
        logging.debug("writing fat")
        f = self.f
        sector_count = 0

        assert len(self.fat)*4 % self.sector_size == 0

        fat_sectors = []

        for t, i, sid in self.iter_difat():
            sector_type = fat_sector_types.get(sid, sid)
            if not isinstance(sector_type, int):
                continue
            fat_sectors.append(sid)

        # check that the difat has enough entries to hold the current fat
        assert len(fat_sectors) == len(self.fat)*4 // self.sector_size

        for i, sid in enumerate(fat_sectors):

            logging.debug("writing fat to sid: %d" % sid)
            f.seek((sid + 1) *  self.sector_size)

            offset = i * self.sector_size // 4

            for j in range(self.sector_size // 4):
                write_u32le(f, self.fat[offset + j])

    def read_minifat(self):
        f = self.f
        sector_count = 0
        self.minifat = array(str('I'))

        for sid in self.get_fat_chain(self.minifat_sector_start):
            self.minifat_chain.append(sid)
            f.seek((sid + 1) *  self.sector_size)
            extend_sid_table(f, self.minifat, self.sector_size)
            sector_count += 1

        if sys.byteorder == 'big':
             self.minifat.byteswap()

        for i,v in enumerate(self.minifat):
            if v == FREESECT:
                self.minifat_freelist.append(i)

        logging.debug("read %d mini fat sectors", sector_count)

    def write_minifat(self):
        f = self.f
        sector_count = 0
        for i, sid in enumerate(self.get_fat_chain(self.minifat_sector_start)):
            pos = (sid + 1) *  self.sector_size
            f.seek(pos)
            logging.debug("writing minifat to sid: %d at: %d" % (sid,pos))

            offset = i * self.sector_size // 4
            for j in range(self.sector_size // 4):
                write_u32le(f, self.minifat[offset + j])

            assert f.tell() - pos == self.sector_size

    def write_modified_dir_entries(self):
        for entry in self.modified.values():
            sid, sid_offset = self.dir_entry_sid_offset(entry.dir_id)
            entry.write()

            # invalidate  sector
            if sid in self.sector_cache:
                del self.sector_cache[sid]

        self.modified = {}

    def write_dir_entries(self):
        self.write_modified_dir_entries()

        for dir_id in self.dir_freelist:
            # clear DirEntry
            f = self.f
            f.seek(self.dir_entry_pos(dir_id))
            logging.debug("clearing dir id: %d" % (dir_id))
            for i in range(128):
                f.write(b'\0')

    def next_free_minifat_sect(self):

        idx_per_sect = self.sector_size // self.mini_stream_sector_size
        stream_sects = len(self.mini_stream_chain) * idx_per_sect

        if self.minifat_freelist:
            i = self.minifat_freelist.pop(0)
            assert self.minifat[i] == FREESECT
            if i+1 > stream_sects:
                self.mini_stream_grow()
            return i

        # for i, item in enumerate(self.minifat):
        #     if item == FREESECT:
        #         if i+1 > stream_sects:
        #             self.mini_stream_grow()
        #         return i

        # if we got here need to add aditional fat
        logging.debug("minifat full, size: %d growing" % len(self.minifat_chain))
        self.minifat_grow()
        return self.next_free_minifat_sect()

    def next_free_sect(self):

        if self.fat_freelist:
            # print("using fat free list")
            i = self.fat_freelist.pop(0)
            assert self.fat[i] == FREESECT

            # Handle Range Lock Sector
            if self.sector_size == 4096 and i == RANGELOCKSECT:
                self.fat[i] = ENDOFCHAIN
                logging.warning("range lock sector in fat freelist, marking ENDOFCHAIN")
                return self.next_free_sect()
            return i

        # if we got here need to add aditional fat
        logging.debug("fat full, growing")

        difat_table = None
        difat_index = None

        for t, i, v in self.iter_difat():

            # hack to grow difat faster
            if self.debug_grow:
                size = len(self.difat[t])
                if i < size - 2:
                    continue

            if v == FREESECT:
                difat_table = t
                difat_index = i
                break

        new_difat_sect = None
        if difat_index is None:
            logging.debug("difat full, growing")
            new_difat_sect = len(self.fat) + 1
            logging.debug("adding new difat to sid: %d" % new_difat_sect)
            if self.difat_sector_count == 0:
                self.difat_sector_start = new_difat_sect
                self.difat_sector_count = 1
            else:
                self.difat[-1][-1] = new_difat_sect
                self.difat_sector_count += 1

            # add difat table
            difat = []
            for i in range(self.sector_size // 4):
                difat.append(FREESECT)

            difat[-1] == ENDOFCHAIN
            self.difat.append(difat)

            for t, i, v in self.iter_difat():
                if v == FREESECT:
                    difat_table = t
                    difat_index = i
                    break

        new_fat_sect = len(self.fat)
        logging.debug("adding new fat to sid: %d" % new_fat_sect)

        self.difat[difat_table][difat_index] = new_fat_sect

        # grow fat entries
        idx_start = len(self.fat)
        for i in range(self.sector_size // 4):
            self.fat.append(FREESECT)
            index = idx_start + i

            # Handle Range Lock Sector

            # The range lock sector is the sector
            # that covers file offsets 0x7FFFFF00-0x7FFFFFFF in the file
            if self.sector_size == 4096 and index == RANGELOCKSECT:
                logging.debug("adding range lock")
                self.fat[index] = ENDOFCHAIN
                continue

            if index in (new_fat_sect, new_difat_sect):
                continue
            self.fat_freelist.append(index)

        self.fat[new_fat_sect] = FATSECT
        self.fat_sector_count += 1

        if not new_difat_sect is None:
            self.fat[new_difat_sect] = DIFSECT

        return self.next_free_sect()
        # raise NotImplementedError("adding additional fat")

    def read_sector_data(self, sid):

        sector_data = self.sector_cache.get(sid, None)
        if sector_data is not None:
            return sector_data
        else:
            pos = (sid + 1) *  self.sector_size
            self.f.seek(pos)
            sector_data = bytearray(self.sector_size)
            self.f.readinto(sector_data)
            self.sector_cache[sid] = sector_data
            return sector_data

    def get_sid_offset(self, abs_pos):
        sid, sid_offset = divmod(abs_pos, self.sector_size)
        return sid-1, sid_offset

    def dir_entry_sid_offset(self, dir_id):
        stream_pos = dir_id * 128
        chain_index, sid_offset = divmod(stream_pos, self.sector_size)
        sid = self.dir_fat_chain[chain_index]
        return sid, sid_offset

    def dir_entry_pos(self, dir_id):
        sid, sid_offset = self.dir_entry_sid_offset(dir_id)
        pos = ((sid + 1) *  self.sector_size) + sid_offset
        return pos

    def read_dir_entry(self, dir_id, parent = None):
        if dir_id is None:
            return None

        entry = self.dir_cache.get(dir_id, None)
        if entry is not None:
            return entry

        # assert not dir_id in self.dir_freelist

        stream_pos = dir_id * 128
        chain_index = stream_pos // self.sector_size
        sid_offset  = stream_pos % self.sector_size
        sid = self.dir_fat_chain[chain_index]

        sector_data = self.read_sector_data(sid)

        data= bytearray(sector_data[sid_offset:sid_offset+128])
        entry = DirEntry(self, dir_id, data=data)

        entry.parent = parent
        self.dir_cache[dir_id] = entry
        return entry

    def clear_sector(self, sid):
        sector_pos = (sid + 1) * self.sector_size
        self.f.seek(sector_pos)
        for i in range(self.sector_size):
            self.f.write(b'\0')

    def next_free_dir_id(self):

        # use free list first
        if self.dir_freelist:
            return self.dir_freelist.pop(0)

        f = self.f

        # this is just too slow just add a new sector

        # for i, sid in enumerate(self.dir_fat_chain):
        #     logging.debug("reading dir sector: %d" % sid)
        #     sector_pos = (sid + 1) *  self.sector_size
        #
        #     sector_first_dir_id = i * (self.sector_size // 128)
        #     for j in range(self.sector_size // 128):
        #         dir_type_offset = 66
        #         offset = j * 128
        #
        #         seek_pos = sector_pos + offset + dir_type_offset
        #
        #         f.seek(seek_pos)
        #         dir_type = read_u8(f)
        #         if dir_types.get(dir_type , "unknown") == 'empty':
        #             return sector_first_dir_id + j

        # if here we need to add to dir sector

        sect = self.fat_chain_append(self.dir_fat_chain[-1])

        self.dir_fat_chain.append(sect)
        self.dir_sector_count += 1
        self.clear_sector(sect)
        first_dir_id = (len(self.dir_fat_chain) - 1) * self.sector_size // 128
        for i in range(self.sector_size // 128):
            self.dir_freelist.append(first_dir_id + i)

        return self.next_free_dir_id()

    def get_fat_chain(self, start_sid, minifat=False):
        fat = self.fat
        fat_name = "FAT"
        if minifat:
            fat = self.minifat
            fat_name = "MINIFAT"

        # Floyd's Tortoise and Hare cycle-finding algorithm
        a = start_sid
        b = start_sid
        sectors = []

        if start_sid in (None, ENDOFCHAIN, FREESECT, DIFSECT, FATSECT):
            return []

        while b != ENDOFCHAIN:
            sectors.append(b)
            b = fat[b]
            if a != ENDOFCHAIN:
                a = fat[a]
                if a != ENDOFCHAIN:
                    a = fat[a]
                    if a == b:
                        raise CompoundFileBinaryError('cyclic %s fat chain found starting at %d' % (fat_name, start_sid))

        return sectors

    def mini_stream_grow(self):
        sid = self.next_free_sect()
        logging.debug("adding to mini stream fat sid: %d" %  sid)
        if not self.mini_stream_chain:
            self.mini_stream_chain = [sid]
            self.root.sector_id = sid
        else:
            self.fat[self.mini_stream_chain[-1]] = sid
            self.mini_stream_chain.append(sid)

        # self.root.byte_size += self.sector_size
        self.fat[sid] = ENDOFCHAIN
        self.clear_sector(sid)

    def minifat_grow(self):
        # grow minifat
        sid = self.next_free_sect()
        logging.debug("growing minifat to sid %d" % sid)

        idx_start = len(self.minifat)

        for i in range(self.sector_size // 4):
            self.minifat.append(FREESECT)
            self.minifat_freelist.append(idx_start + i)

        if self.minifat_sector_count == 0:
            self.minifat_sector_count = 1
            self.minifat_sector_start = sid
        else:
            self.minifat_sector_count += 1
            self.fat[self.minifat_chain[-1]] = sid

        self.minifat_chain.append(sid)
        self.fat[sid] = ENDOFCHAIN

    def fat_chain_append(self, start_sid, minifat=False):

        if minifat:
            sect = self.next_free_minifat_sect()
            logging.debug("creating new mini sector: %d" % sect)
            fat = self.minifat
            self.root.byte_size += 64
        else:
            sect = self.next_free_sect()
            logging.debug("creating new sector: %d" % sect)
            fat = self.fat

        # fat[sect] = ENDOFCHAIN

        if start_sid is None:
            fat[sect] = ENDOFCHAIN
        else:
            fat_chain = self.get_fat_chain(start_sid, minifat)
            assert fat_chain
            fat[fat_chain[-1]] = sect
            fat[sect] = ENDOFCHAIN

        return sect

    def free_fat_chain(self, start_sid, minifat=False):
        fat =self.fat
        fat_name = "fat"
        if minifat:
            fat = self.minifat
            fat_name = "minifat"
        #  self.get_fat_chain(start_sid, minifat)
        for sid in self.get_fat_chain(start_sid, minifat):
            logging.debug("marking %s sid: %d as FREESECT" % (fat_name, sid))
            fat[sid] = FREESECT
            if minifat:
                self.root.byte_size -= 64
                self.minifat_freelist.insert(0, sid)
            else:
                self.fat_freelist.insert(0, sid)


    def create_dir_entry(self, path, dir_type='storage', class_id=None):

        if self.exists(path):
            raise ValueError("%s already exists" % path)

        dirname = os.path.dirname(path)
        basename = os.path.basename(path)

        root = self.find(dirname)

        if root is None:
            raise ValueError("parent dirname does not exist: %s" % dirname)

        if not root.type in ('storage', 'root storage'):
            raise ValueError("can not add entry to non storage type")

        dir_id = self.next_free_dir_id()
        logging.debug("next dir id %d" % dir_id)

        entry = DirEntry(self, dir_id)
        entry.name = basename
        entry.type = dir_type
        entry.class_id = class_id

        # TODO: Implement a Red Black tree
        # all new DirEntries are black, so there is no tree balancing.
        # AAF Low-Level Container Specification says its alright to do this.

        entry.color = 'black'

        root.add_child(entry)
        self.dir_cache[dir_id] = entry

        return entry

    def free_dir_entry(self, entry):

        # add freelist
        self.dir_freelist.append(entry.dir_id)

        # remove from dir caches
        if entry.dir_id in self.dir_cache:
            del self.dir_cache[entry.dir_id]

        if entry.dir_id in self.children_cache:
            del self.children_cache[entry.dir_id]

        if entry.dir_id in self.modified:
            del self.modified[entry.dir_id]

        entry.dir_id = None


    def remove(self, path):
        """
        Removes both streams and storage DirEntry types from file.
        storage type entries need to be empty dirs.
        """

        entry = self.find(path)

        if not entry:
            raise ValueError("%s does not exists" % path)

        if entry.type == 'root storage':
            raise ValueError("can no remove root entry")

        if entry.type == "storage" and not entry.child_id is None:
            raise ValueError("storage contains children")

        entry.pop()

        # remove stream data
        if entry.type == "stream":
            self.free_fat_chain(entry.sector_id, entry.byte_size < self.min_stream_max_size)

        self.free_dir_entry(entry)


    def rmtree(self, path):
        """
        Removes directory structure, similar to shutil.rmtree.
        """
        for root, storage, streams in self.walk(path, topdown=False):

            for item in streams:
                self.free_fat_chain(item.sector_id, item.byte_size < self.min_stream_max_size)
                self.free_dir_entry(item)

            for item in storage:
                self.free_dir_entry(item)

            root.child_id = None

        # remove root item
        self.remove(path)


    def listdir(self, path = None):
        """
        Return a list containing the ``DirEntry`` objects in the directory
        given by path.
        """

        result = self.listdir_dict(path)
        return result.values()

    def listdir_dict(self, path = None):
        """
        Return a dict containing the ``DirEntry`` objects in the directory
        given by path with name of the dir as key.
        """

        if path is None:
            path = self.root

        root = self.find(path)
        if root is None:
            raise ValueError("unable to find dir: %s" % str(path))

        if not root.isdir():
            raise ValueError("can only list storage types")

        children = self.children_cache.get(root.dir_id, None)
        if children is not None:
            return children

        child = root.child()

        result = {}
        if not child:
            self.children_cache[root.dir_id] = result
            return result

        dir_per_sector = self.sector_size // 128
        max_dirs_entries = self.dir_sector_count * dir_per_sector

        current = child
        stack = []

        while True:

            # go to left most node
            while current is not None:
                stack.append(current)
                current = current.left()
                if len(stack) > max_dirs_entries:
                    raise CompoundFileBinaryError("corrupt folder structure")

            # done if stack is empy
            if not stack:
                break

            current = stack.pop()
            result[current.name] = current
            current = current.right()

        self.children_cache[root.dir_id] = result
        return result

    def find(self, path):
        """
        find a ``DirEntry`` located at *path*. Returns ``None`` if path
        does not exist.
        """

        if isinstance(path, DirEntry):
            return path

        if path == "/":
            return self.root

        split_path = path.lstrip('/').split("/")

        i = 0
        root = self.root

        while True:

            children = self.listdir_dict(root)
            match = children.get(split_path[i], None)

            if match:
                if i == len(split_path) - 1:
                    return match
                root = match
                i += 1
            else:
                return None

    def walk(self, path = None, topdown=True):
        """
        Similar to :func:`os.walk`, yeields a 3-tuple ``(root, storage_items, stream_items)``
        """

        if path is None:
            path = self.root

        root = self.find(path)

        if not root.isdir():
            raise ValueError("can only walk storage types")

        if not root.child_id:
            return

        if topdown:
            storage_items = []
            stream_items = []

            for item in self.listdir(root):
                if item.isdir():
                    storage_items.append(item)
                else:
                    stream_items.append(item)

            yield root, storage_items, stream_items

            for item in storage_items:
                for root, storage_items, stream_items in self.walk(item):
                    yield root, storage_items, stream_items
        else:

            def topdown_visit_node(root):
                storage_items = []
                stream_items = []
                for item in self.listdir(root):
                    if item.isdir():
                        for sub_root, sub_storage, sub_stream in topdown_visit_node(item):
                            yield sub_root, sub_storage, sub_stream

                        storage_items.append(item)
                    else:
                        stream_items.append(item)

                yield root, storage_items, stream_items

            for root_item, storage, stream in topdown_visit_node(root):
                yield root_item, storage, stream


    def exists(self, path):
        """
        Return ``True`` if path refers to a existing path.
        """
        if self.find(path) is None:
            return False
        return True

    def makedir(self, path, class_id=None):
        """
        Create a storage DirEntry name path
        """
        return self.create_dir_entry(path, dir_type='storage', class_id=class_id)

    def makedirs(self, path):
        """
        Recursive storage DirEntry creation function.
        """
        root = ""

        assert path.startswith('/')
        p = path.strip('/')
        for item in p.split('/'):
            root += "/" + item
            if not self.exists(root):
                self.makedir(root)

        return self.find(path)

    def move(self, src, dst):
        """
        Moves ``DirEntry`` from src to dst
        """
        src_entry = self.find(src)
        if src_entry is None:
            raise ValueError("src path does not exist: %s" % src)

        if dst.endswith('/'):
            dst += src_entry.name

        if self.exists(dst):
            raise ValueError("dst path already exist: %s" % dst)

        if dst == '/' or src == '/':
            raise ValueError("cannot overwrite root dir")

        split_path = dst.strip('/').split('/')
        dst_basename = split_path[-1]
        dst_dirname = '/' + '/'.join(split_path[:-1])

        # print(dst)
        # print(dst_basename, dst_dirname)

        dst_entry = self.find(dst_dirname)
        if dst_entry is None:
            raise ValueError("src path does not exist: %s" % dst_dirname)

        if not dst_entry.isdir():
            raise ValueError("dst dirname cannot be stream: %s" % dst_dirname)

        # src_entry.parent.remove_child(src_entry)

        src_entry.pop()

        src_entry.parent = None
        src_entry.name = dst_basename
        dst_entry.add_child(src_entry)

        self.children_cache[dst_entry.dir_id][src_entry.name] = src_entry

        return src_entry

    def open(self, path, mode='r'):
        """Open stream, returning ``Stream`` object"""

        entry = self.find(path)
        if entry is None:
            if mode == 'r':
                raise ValueError("stream does not exists: %s" % path)
            entry = self.create_dir_entry(path, 'stream', None)

        else:
            if not entry.isfile():
                raise ValueError("can only open stream type DirEntry's")

            if mode == 'w':
                logging.debug("stream: %s exists, overwriting" % path)
                self.free_fat_chain(entry.sector_id, entry.byte_size < self.min_stream_max_size)
                entry.sector_id = None
                entry.byte_size = 0
                entry.class_id = None

        s = Stream(self, entry, mode)
        return s
