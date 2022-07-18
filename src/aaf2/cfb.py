from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import logging

import sys
import os
import io
import math
import weakref
from array import array
from struct import Struct
import struct
from collections import deque
import random

from .utils import (
    read_u8, read_u16le,
    read_u32le, read_u64le,
    read_filetime, read_sid,
    write_u8, write_u16le,
    write_u32le, write_u64le,
    write_filetime, write_sid,
    decode_utf16le,
    decode_sid, encode_sid,
    unpack_u16le_from, unpack_u32le_from, unpack_u64le_from
)
from .exceptions import CompoundFileBinaryError
from .cache import LRUCacheDict
from .import auid

from io import BytesIO

sentinel = object()

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
    __slots__ = ('storage', 'dir', 'mode', 'pos', 'fat_chain')
    def __init__(self, storage, entry, mode='r'):
        self.storage = storage
        self.dir = entry
        self.mode = mode
        self.pos = 0
        self.fat_chain = []
        if not mode in ('r', 'w', 'rw'):
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
        if self.dir.type == 'root storage':
            return False
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

    def read(self, n=-1):

        byte_size = self.dir.byte_size
        if n == -1:
            bytes_to_read = max(0, byte_size - self.tell())
        else:
            bytes_to_read = max(0, min(n, byte_size - self.tell()))

        result = bytearray(bytes_to_read)
        mv = memoryview(result)

        is_mini_stream = byte_size < self.storage.min_stream_max_size
        full_sector_size = self.storage.sector_size
        mini_sector_size = self.storage.mini_stream_sector_size
        mini_stream_chain = self.storage.mini_stream_chain
        read_sector_data = self.storage.read_sector_data
        sector_data = None
        prev_sid = -1

        if is_mini_stream:
            mini_fat_index     = self.pos // mini_sector_size
            mini_sector_offset = self.pos  % mini_sector_size
            sector_size = mini_sector_size
        else:
            index      = self.pos // full_sector_size
            start_offset = self.pos  % full_sector_size
            sector_size = full_sector_size

        while bytes_to_read > 0:

            # inlined on purpose this loop runs a lot
            if is_mini_stream:
                mini_stream_sid = self.fat_chain[mini_fat_index]
                mini_stream_pos = (mini_stream_sid * mini_sector_size) + mini_sector_offset

                index      = mini_stream_pos // full_sector_size
                sid_offset = mini_stream_pos  % full_sector_size

                sid = mini_stream_chain[index]
                sector_offset = mini_sector_offset

                mini_sector_offset = 0
                mini_fat_index += 1

                if sid != prev_sid:
                    sector_data = read_sector_data(sid)
                    prev_sid = sid

            else:
                sid = self.fat_chain[index]
                sector_offset = start_offset
                sid_offset = start_offset

                index += 1
                start_offset = 0

                sector_data = read_sector_data(sid)

            bytes_can_read = min(bytes_to_read, sector_size - sector_offset)
            assert bytes_can_read > 0

            mv[:bytes_can_read] = sector_data[sid_offset:sid_offset+bytes_can_read]

            self.pos += bytes_can_read
            mv = mv[bytes_can_read:]

            bytes_to_read -= bytes_can_read

        return result

    def allocate(self, byte_size):

        minifat = self.is_mini_stream()
        realloc_data = None
        orig_pos = None
        # convert from minifat to fat
        if minifat and byte_size >= self.storage.min_stream_max_size:
            # logging.debug("converting stream for minifat to fat")
            orig_pos = self.pos
            self.seek(0)
            realloc_data = self.read()
            assert len(realloc_data) == self.dir.byte_size
            self.storage.free_fat_chain(self.dir.sector_id, True)
            self.dir.sector_id = None
            minifat = False
            self.fat_chain = []

        self.dir.byte_size = byte_size
        sector_size = self.sector_size()
        sector_count = (byte_size + sector_size - 1) // sector_size

        current_sects= len(self.fat_chain)
        # logging.debug("%d bytes requires %d sectors at %d has %d" % (byte_size, sector_count, self.sector_size(), current_sects))

        while len(self.fat_chain) < sector_count:
            last_sector_id = self.fat_chain[-1] if self.fat_chain else None
            sid = self.storage.fat_chain_append(last_sector_id, minifat)
            self.fat_chain.append(sid)
            if self.dir.sector_id is None:
                self.dir.sector_id = sid

        if realloc_data is not None:
            self.pos = 0
            self.write(realloc_data)
            self.pos = min(orig_pos, len(realloc_data))

    def write(self, data):
        data_size = len(data)
        current_size = self.dir.byte_size
        new_size = max(self.tell() + data_size, current_size)
        if new_size > current_size:
            self.allocate(new_size)

        mv = memoryview(data)

        is_mini_stream = self.dir.byte_size < self.storage.min_stream_max_size
        full_sector_size = self.storage.sector_size
        mini_sector_size = self.storage.mini_stream_sector_size
        mini_stream_chain = self.storage.mini_stream_chain
        sector_cache = self.storage.sector_cache
        f = self.storage.f

        if is_mini_stream:
            mini_fat_index     = self.pos // mini_sector_size
            mini_sector_offset = self.pos  % mini_sector_size
            sector_size = mini_sector_size
        else:
            index      = self.pos // full_sector_size
            sid_offset = self.pos  % full_sector_size
            sector_size = full_sector_size

        while data_size > 0:

            # inlined on purpose this method can get called a lot
            if is_mini_stream:
                mini_stream_sid = self.fat_chain[mini_fat_index]
                mini_stream_pos  = (mini_stream_sid * mini_sector_size) + mini_sector_offset

                index      = mini_stream_pos // full_sector_size
                sid_offset = mini_stream_pos  % full_sector_size

                sid = mini_stream_chain[index]

                sector_offset = mini_sector_offset
                seek_pos = ((sid + 1) *  full_sector_size) + sid_offset

                mini_fat_index += 1
                mini_sector_offset = 0

            else:
                sid = self.fat_chain[index]
                sector_offset = sid_offset

                seek_pos = ((sid + 1) *  full_sector_size) + sid_offset

                index += 1
                sid_offset = 0

            byte_writeable = min(len(mv), sector_size - sector_offset)
            assert byte_writeable > 0

            if sid in sector_cache:
                del sector_cache[sid]

            f.seek(seek_pos)
            f.write(mv[:byte_writeable])
            self.pos += byte_writeable

            mv = mv[byte_writeable:]
            data_size -= byte_writeable

        assert self.pos <= self.dir.byte_size

    def truncate(self, size=None):
        # print("trunc", self.dir.path())
        if size is None:
            size = self.pos

        current_byte_size = self.dir.byte_size
        is_mini_stream = self.is_mini_stream()
        full_sector_size = self.storage.sector_size
        mini_sector_size = self.storage.mini_stream_sector_size

        # free the stream
        if size == 0:
            self.storage.free_fat_chain(self.dir.sector_id, is_mini_stream)
            self.pos = 0
            self.dir.sector_id = None
            self.dir.byte_size = 0
            self.fat_chain = []
            return


        # grown the stream
        if size > current_byte_size:
            self.allocate(size)
            return

        # shrink to mini stream
        if size < self.storage.min_stream_max_size and not is_mini_stream and self.dir.type != 'root storage':
            orig_pos = self.pos
            self.pos = 0

            realloc_data = self.read(size)
            self.storage.free_fat_chain(self.dir.sector_id, False)

            self.pos = 0
            self.dir.sector_id = None
            self.dir.byte_size = 0
            self.fat_chain = []

            self.write(realloc_data)
            self.pos = min(orig_pos, size)
            assert self.dir.byte_size == size
            return

        if is_mini_stream:
            sector_size = mini_sector_size
            fat_table = self.storage.minifat
        else:
            sector_size = full_sector_size
            fat_table = self.storage.fat

        sector_count = (size + sector_size - 1) // sector_size

        if len(self.fat_chain) > sector_count:
            last_sector_id = self.fat_chain[sector_count-1]
            self.storage.free_fat_chain(self.fat_chain[sector_count], is_mini_stream)
            fat_table[last_sector_id] = ENDOFCHAIN
            self.fat_chain = self.fat_chain[:sector_count]

        self.dir.byte_size = size
        self.pos = min(self.pos, size)

    def close(self):
        pass


def is_red(entry):
    if (entry is not None) and entry.red:
        return True
    return False

def is_not_red(entry):
    return not is_red(entry)

def is_parent_of(parent, entry):
    return parent[0] is entry or parent[1] is entry

def validate_rbtree(root):
    if root is None:
        return 1

    left = root.left()
    right = root.right()

    if is_red(root):
        if is_red(left) or is_red(right):
            print("Red violation {}".format(root.path()))
            # raise CompoundFileBinaryError()

    lh = validate_rbtree(left)
    rh = validate_rbtree(right)

    if left is not None and left >= root:
        raise CompoundFileBinaryError("Binary tree violation" )

    if right is not None and right <= root:
        raise CompoundFileBinaryError("Binary tree violation")

    # Black height mismatch
    # cannot guarantee all aaf Implementations use rbtree
    # if lh != 0 and rh != 0 and lh != rh:
    #     print(lh, rh)
    #     raise CompoundFileBinaryError("Black violation {}".format(root.path()))

    if lh != 0 and rh != 0:
        return lh if is_red(root) else lh + 1
    else:
        return 0

def jsw_single(root, direction):
    other_side = 1 - direction

    new_root = root[other_side]

    root[other_side] = new_root[direction]
    new_root[direction] = root

    root.red = True
    new_root.red = False

    return new_root

def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)

def find_entry_parent(root, entry, max_depth):
    parent = None
    node = root
    count = 0
    while node is not None and count < max_depth:
        if node is entry:
            return parent

        direction = 0 if entry < node else 1
        parent = node
        node = node[direction]
        count += 1

    raise CompoundFileBinaryError("Max Depth Exceeded")

def get_entry_path(root, entry, max_depth):
    parent = None
    node = root
    count = 0
    path = []
    while node is not None and count < max_depth:

        path.append(node)
        if node is entry:
            break
        direction = 0 if entry < node else 1
        parent = node
        node = node[direction]
        count += 1

    return path


class DirEntry(object):
    __slots__ = ('storage', 'dir_id', 'parent', 'data', '_name', '__weakref__')

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
        self._name = sentinel

    @property
    def name(self):
        if self._name is not sentinel:
            return self._name
        name_size = unpack_u16le_from(self.data, 64)
        assert name_size <= 64
        name =  decode_utf16le(self.data[:name_size])
        self._name = name
        return name

    @name.setter
    def name(self, value):
        name_data = value.encode("utf-16le")
        name_size = len(name_data)
        assert name_size <= 64
        self._name = value
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
    def red(self):
        if self.data[67] == 0x01:
            return False
        return True

    @red.setter
    def red(self, value):
        if value:
            self.data[67] = 0x00
        else:
            self.data[67] = 0x01

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
        value = auid.AUID(bytes_le=self.data[80:96])
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

    def __getitem__(self, index):
        return self.left() if index == 0 else self.right()

    def __setitem__(self, index, value):
        if value is None:
            dir_id = None
        else:
            dir_id = value.dir_id

        if index == 0:
            self.left_id = dir_id
        else:
            self.right_id = dir_id

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
        if child is None:
            self.child_id = entry.dir_id
        else:
            # child.insert_old(entry)

            # make sure entry is part of cache
            # or insert might now work correctly
            self.storage.dir_cache[entry.dir_id] = entry
            self.insert(entry)

        if self.dir_id in self.storage.children_cache:
            self.storage.children_cache[self.dir_id][entry.name] = entry

    def insert(self, entry):
        """
        Inserts entry into child folder tree.
        Tries to maintain a balanced red black tree.
        Technique is base on topdown insert approach in described in
        https://eternallyconfuzzled.com/red-black-trees-c-the-most-common-balanced-binary-search-tree
        """

        dir_per_sector = self.storage.sector_size // 128
        max_dirs_entries = self.storage.dir_sector_count * dir_per_sector

        head = DirEntry(self.storage, None) # False tree root
        head.red = True
        entry.red = True

        grand_grand_grand_parent = None
        grand_grand_parent = head
        grand_parent = None
        parent = None
        direction = 0
        last = 0

        node = self.child()
        self.child_id = None
        grand_grand_parent.right_id = node.dir_id

        assert node
        count = 0

        while count < max_dirs_entries:

            if node is None:
                node = entry
                parent[direction] = node

            elif is_red(node[0]) and is_red(node[1]):
                # Color flip
                node.red = True
                node[0].red = False
                node[1].red = False

            # Fix red violations
            if is_red(node) and is_red(parent):
                if grand_grand_parent[0] is grand_parent:
                    direction2 = 0
                elif grand_grand_parent[1] is grand_parent:
                    direction2 = 1
                else:
                    raise CompoundFileBinaryError()

                if node is parent[last]:
                    grand_grand_parent[direction2] = jsw_single(grand_parent, 1 - last)
                    # restore parent references
                    # NOTE: Example implementation doesn't do this
                    grand_parent = grand_grand_parent
                    grand_grand_parent = grand_grand_grand_parent

                    # assert is_parent_of(parent, node)
                    # assert is_parent_of(grand_parent, parent)

                elif node is parent[1-last]:
                    grand_grand_parent[direction2] = jsw_double(grand_parent, 1 - last)
                    # restore parent references
                    # NOTE: Example implementation doesn't do this
                    parent = grand_grand_parent
                    if parent is head:
                        grand_parent = None
                    else:
                        grand_parent = grand_grand_grand_parent
                    grand_grand_parent = None

                    # assert is_parent_of(parent, node)
                    # if grand_parent is not None:
                    #     assert is_parent_of(grand_parent, parent)
                else:
                    # can this happen?
                    raise CompoundFileBinaryError()

            # node has been inserted
            if node is entry:
                break

            last = direction
            direction = 0 if entry < node else 1

            if grand_grand_parent is not None:
                grand_grand_grand_parent = grand_grand_parent

            if grand_parent is not None:
                grand_grand_parent = grand_parent

            grand_parent = parent
            parent = node
            node = node[direction]

            assert is_parent_of(parent, node)
            if grand_parent:
                assert is_parent_of(grand_parent, parent)
            if grand_grand_parent:
                assert is_parent_of(grand_grand_parent, grand_parent)

            count += 1

        if count >= max_dirs_entries:
            raise CompoundFileBinaryError("max dir entries limit reached")

        # update root of tree as it could have changed
        self.child_id = head.right_id
        self.child().red = False

    def pop(self):
        """
        remove self from self.parent folder binary search tree.
        Tries to maintain a balanced red black tree.
        Technique is base on topdown remove approach in described in
        https://eternallyconfuzzled.com/red-black-trees-c-the-most-common-balanced-binary-search-tree
        """
        entry = self

        dir_per_sector = self.storage.sector_size // 128
        max_dirs_entries = self.storage.dir_sector_count * dir_per_sector
        count = 0

        head = DirEntry(self.storage, None) # False tree root
        head.red = True
        head.name = "" # NOTE: any name will be less then this
        node = head
        node[1] = self.parent.child()
        grand_parent = None
        parent = None
        entry_parent = None
        entry_grand_parent = None
        direction = 1
        found = None

        # This keeps going until predecessor is found, even if entry is found
        while node[direction] is not None and count < max_dirs_entries:

            last = direction
            grand_parent = parent
            parent = node
            node = node[direction]

            # The trick here is after entry is found
            # this will continue to be used to find the predecessor of entry.
            # its quite clever!
            direction = int(node < entry)

            if node is entry:
                # store the grand parent because the parent of entry
                # can change during rebalance below
                if grand_parent is None:
                    entry_grand_parent = head
                else:
                    entry_grand_parent = grand_parent
                found = node

            # Push the red node down
            if is_not_red(node) and is_not_red(node[direction]):

                if is_red(node[1 - direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                    assert is_parent_of(parent, node)

                elif is_not_red(node[1 - direction]):
                    sibling = parent[1 - direction]
                    if sibling is not None:

                        if is_not_red(sibling[1 - last]) and is_not_red(sibling[last]):
                            # Color flip
                            parent.red = False
                            sibling.red = True
                            node.red = True
                        else:
                            if grand_parent[0] == parent:
                                direction2 = 0
                            elif  grand_parent[1] == parent:
                                direction2 = 1
                            else:
                                # can this happen?
                                raise CompoundFileBinaryError()

                            if is_red(sibling[last]):
                                grand_parent[direction2] = jsw_double(parent, last)

                            elif is_red(sibling[1 - last]):
                                grand_parent[direction2] = jsw_single(parent, last)

                            # Ensure correct coloring
                            node.red = True
                            grand_parent[direction2].red = True;
                            grand_parent[direction2][0].red = False;
                            grand_parent[direction2][1].red = False;

                            assert is_parent_of(parent, node)

            count += 1

        assert found
        if count >= max_dirs_entries:
            raise CompoundFileBinaryError("max dir entries limit reached")

        # entry parent could have changed during rebalance
        max_search_depth = 4 # grand_parent -> parent -> node
        entry_parent = find_entry_parent(entry_grand_parent, entry, max_search_depth)

        if entry_parent[0] is entry:
            entry_direction = 0
        elif entry_parent[1] is entry:
            entry_direction = 1
        else:
            raise CompoundFileBinaryError("Unable to find entry parent")

        # node is the predecessor. node will be removed and entry will be replaced
        if node is not entry:
            # remove the predecessor
            parent[parent[1] is node] = node[node[0] is None]

            # replace entry with its predecessor
            node[0] = entry[0]
            node[1] = entry[1]
            node.red = entry.red

            entry_parent[entry_direction] = node
        else:
            entry_side = int(entry[0] is None)
            entry_parent[entry_direction] = entry[entry_side]

        # update root of tree as it could have changed
        self.parent.child_id = head.right_id
        if self.parent.child_id:
            self.parent.child().red = False

        # clear from cache
        if self.parent.dir_id in self.storage.children_cache:
            del self.storage.children_cache[self.parent.dir_id][entry.name]

        # clear parent and left and right
        self.left_id = None
        self.right_id = None
        self.parent = None

    def rebalance_children_tree(self):

        children  = self.listdir()
        self.child_id = None
        random.shuffle(children)
        for c in children:
            c.left_id = None
            c.right_id = None
            self.add_child(c)


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
        self.fat_freelist = []

        self.minifat = array(str('I'))
        self.minifat_freelist = []

        self.difat_chain = []
        self.minifat_chain = []
        self.dir_fat_chain = []

        self.mini_stream_chain = []

        self.modified = {}

        self.sector_cache = LRUCacheDict()
        self.dir_cache = weakref.WeakValueDictionary()
        self.children_cache = LRUCacheDict()
        self.dir_freelist = []

        self.debug_grow = False
        self.is_open = True

        if isinstance(self.f, BytesIO):
            self.mode = 'wb+'
        else:
            self.mode = mode

        if self.mode in ("r", "r+", "rb", 'rb+'):

            self.read_header()
            self.read_fat()
            mini_stream_byte_size = self.read_minifat()

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

            if self.root.sector_id is not None and mini_stream_byte_size != self.root.byte_size:
                message = "mini stream size missmatch: %d != %d, using size from minifat"
                logging.warning(message % (self.root.byte_size, mini_stream_byte_size))
        else:
            self.setup_empty(sector_size)
            self.write_header()

            logging.debug("pos: %d" % self.f.tell())

            logging.debug("writing root dir sector")
            self.root.write()
            self.f.write(bytearray(self.sector_size - 128))
            self.write_fat()

    def close(self):
        if self.mode in ("r", "rb"):
            return

        # calculate mini stream size
        if self.root.sector_id is not None:
            # I cannot find this documented anywhere but the size of the mini stream
            # is the size up to the last mini sector is uses. Not the total Non FREESECT's.
            # If self.root.byte_size is not set correctly the some applications will crash hard...

            # find last non-free sect
            for i,v in enumerate(reversed(self.minifat)):
                if v != FREESECT:
                    break

            last_used_sector_id = len(self.minifat) - i
            mini_stream_byte_size = (last_used_sector_id * self.mini_stream_sector_size)
            self.root.byte_size = mini_stream_byte_size

            # Truncate ministream
            s = Stream(self, self.root, 'rw')
            s.truncate(mini_stream_byte_size)

        self.write_header()
        self.write_difat()
        self.write_fat()
        self.write_minifat()
        self.write_dir_entries()

        # Truncate file to the last free sector
        for i,v in enumerate(reversed(self.fat)):
            if v != FREESECT:
                break

        last_used_sector_id = len(self.fat) - i
        pos = (last_used_sector_id + 1) *  self.sector_size
        self.f.seek(pos)
        self.f.truncate()

        self.is_open = False

    def setup_empty(self, sector_size):

        if sector_size == 4096:
            self.class_id = auid.AUID("0d010201-0200-0000-060e-2b3403020101")
        elif sector_size == 512:
            self.class_id = auid.AUID("42464141-000d-4d4f-060e-2b34010101ff")
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
        self.root.class_id = auid.AUID("b3b398a5-1c90-11d4-8053-080036210804")

        self.dir_cache[0] = self.root

        self.dir_fat_chain = [0]

        # raise NotImplementedError("mode: %s supported not implemented" % self.f.mode)

    def write_header(self):
        logging.debug("writiing header")
        f = self.f
        f.seek(0)
        f.write(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1') # Magic
        f.write(self.class_id.bytes_le)
        write_u16le(f, self.minor_version)
        write_u16le(f, self.major_version)
        write_u16le(f, 0xFFFE) # byte order le
        write_u16le(f, int(math.log(self.sector_size, 2)))
        write_u16le(f, int(math.log(self.mini_stream_sector_size, 2)))
        f.write(b'\0' * 6) # skip reserved

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

        self.magic = f.read(8)
        logging.debug("magic: %s" % str([self.magic]))

        if self.magic != b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
            raise CompoundFileBinaryError("invalid file magic signature: {}".format([self.magic]))

        self.class_id = auid.AUID(bytes_le=f.read(16))
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

        f.read(6) # skip reserved

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
            logging.warning("fat sector count missmatch difat: %d header: %d" % (len(fat_sectors), self.fat_sector_count))
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
                logging.warning("range lock sector has data")

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

        element_count = self.sector_size // 4
        fat_table_struct = Struct(str('<%dI' % element_count))
        for i, sid in enumerate(fat_sectors):

            # logging.debug("writing fat to sid: %d" % sid)
            f.seek((sid + 1) *  self.sector_size)
            start = i * element_count
            end = start + element_count
            f.write(fat_table_struct.pack(*self.fat[start:end]))

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

        last_used_sector = 0
        for i,v in enumerate(self.minifat):
            if v == FREESECT:
                self.minifat_freelist.append(i)
            else:
                last_used_sector = i

        mini_stream_byte_size = ((last_used_sector+1) * self.mini_stream_sector_size)

        logging.debug("read %d mini fat sectors", sector_count)
        return mini_stream_byte_size

    def write_minifat(self):
        f = self.f
        sector_count = 0

        element_count = self.sector_size // 4
        fat_table_struct = Struct(str('<%dI' % element_count))

        for i, sid in enumerate(self.get_fat_chain(self.minifat_sector_start)):
            pos = (sid + 1) *  self.sector_size
            f.seek(pos)
            start = i * element_count
            end = start + element_count
            f.write(fat_table_struct.pack(*self.minifat[start:end]))

    def write_modified_dir_entries(self):

        f = self.f
        for dir_id in sorted(self.modified):
            entry = self.modified[dir_id]
            stream_pos = entry.dir_id * 128
            chain_index = stream_pos // self.sector_size
            sid_offset  = stream_pos % self.sector_size
            sid = self.dir_fat_chain[chain_index]

            pos = ((sid + 1) *  self.sector_size) + sid_offset

            f.seek(pos)
            # force black everything
            # entry.data[67] = 0x01
            f.write(entry.data)

            # invalidate  sector
            if sid in self.sector_cache:
                del self.sector_cache[sid]

        self.modified = {}

    def write_dir_entries(self):
        self.write_modified_dir_entries()

        # clear empty DirEntrys
        empty_dir = bytearray(128)
        f = self.f

        self.dir_freelist.sort()
        for dir_id in self.dir_freelist:

            stream_pos = dir_id * 128
            chain_index = stream_pos // self.sector_size
            sid_offset  = stream_pos % self.sector_size
            sid = self.dir_fat_chain[chain_index]

            pos = ((sid + 1) *  self.sector_size) + sid_offset

            f.seek(pos)
            f.write(empty_dir)

    def next_free_minifat_sect(self):

        idx_per_sect = self.sector_size // self.mini_stream_sector_size
        stream_sects = len(self.mini_stream_chain) * idx_per_sect

        if self.minifat_freelist:
            i = self.minifat_freelist.pop(0)
            assert self.minifat[i] == FREESECT
            if i+1 > stream_sects:
                self.mini_stream_grow()
            return i

        # if we got here need to add additional fat
        sid = self.next_free_sect()
        # logging.warning("growing minifat to sid %d" % sid)

        idx_start = len(self.minifat)
        idx_end = idx_start + self.sector_size // 4

        self.minifat.extend([FREESECT for i in range(idx_start, idx_end)])
        self.minifat_freelist.extend([i for i in range(idx_start, idx_end)])

        if self.minifat_sector_count == 0:
            self.minifat_sector_count = 1
            self.minifat_sector_start = sid
        else:
            self.minifat_sector_count += 1
            self.fat[self.minifat_chain[-1]] = sid

        self.minifat_chain.append(sid)
        self.fat[sid] = ENDOFCHAIN

        return self.next_free_minifat_sect()

    def next_free_sect(self):

        if self.fat_freelist:
            # print("using fat free list")
            i = self.fat_freelist.pop(0)
            assert self.fat[i] == FREESECT

            # Handle Range Lock Sector
            if i == RANGELOCKSECT and self.sector_size == 4096:
                self.fat[i] = ENDOFCHAIN
                logging.warning("range lock sector in fat freelist, marking ENDOFCHAIN")
                return self.next_free_sect()
            return i

        # if we got here need to add additional fat
        # logging.debug("fat full, growing")

        difat_table = None
        difat_index = None

        for t, i, v in self.iter_difat():
            if v == FREESECT:
                difat_table = t
                difat_index = i
                break

        new_difat_sect = None
        if difat_index is None:
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
        # logging.debug("adding new fat to sid: %d" % new_fat_sect)

        self.difat[difat_table][difat_index] = new_fat_sect

        # grow fat entries
        idx_start = len(self.fat)
        idx_end = idx_start + (self.sector_size // 4)

        self.fat.extend([FREESECT for i in range(self.sector_size // 4)])

        non_free_sids = set([new_fat_sect, new_difat_sect])

        # Handle Range Lock Sector
        # The range lock sector is the sector
        # that covers file offsets 0x7FFFFF00-0x7FFFFFFF in the file
        if RANGELOCKSECT < idx_end and RANGELOCKSECT > idx_start and self.sector_size == 4096:
            non_free_sids.add(RANGELOCKSECT)
            logging.debug("adding range lock")
            self.fat[RANGELOCKSECT] = ENDOFCHAIN

        freelist = [i for i in range(idx_start, idx_end) if i not in non_free_sids]

        self.fat_freelist.extend(freelist)

        self.fat[new_fat_sect] = FATSECT
        self.fat_sector_count += 1

        if not new_difat_sect is None:
            self.fat[new_difat_sect] = DIFSECT

        return self.next_free_sect()

    def read_sector_data(self, sid):

        sector_data = self.sector_cache.get(sid, None)
        if sector_data is not None:
            return sector_data
        else:
            pos = (sid + 1) *  self.sector_size
            self.f.seek(pos)
            sector_data = bytearray(self.sector_size)
            # NOTE: if requested sector doesn't exist or
            # is truncated will pad with zeros, expected behavior
            bytes_read = self.f.readinto(sector_data)
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
        self.f.write(bytearray(self.sector_size))

    def next_free_dir_id(self):

        # use free list first
        if self.dir_freelist:
            return self.dir_freelist.pop(0)

        f = self.f

        sect = self.fat_chain_append(self.dir_fat_chain[-1])

        self.dir_fat_chain.append(sect)
        self.dir_sector_count += 1

        first_dir_id = (len(self.dir_fat_chain) - 1) * self.sector_size // 128
        last_dir_id = first_dir_id + (self.sector_size // 128)
        self.dir_freelist.extend(range(first_dir_id, last_dir_id))

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
        # logging.debug("adding to mini stream fat sid: %d" %  sid)
        if not self.mini_stream_chain:
            self.mini_stream_chain = [sid]
            self.root.sector_id = sid
        else:
            self.fat[self.mini_stream_chain[-1]] = sid
            self.mini_stream_chain.append(sid)

        self.fat[sid] = ENDOFCHAIN

    def fat_chain_append(self, start_sid, minifat=False):

        if minifat:
            sect = self.next_free_minifat_sect()
            # logging.debug("creating new mini sector: %d" % sect)
            fat = self.minifat
        else:
            sect = self.next_free_sect()
            # logging.debug("creating new sector: %d" % sect)
            fat = self.fat

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
        if minifat:
            fat = self.minifat

        for sid in self.get_fat_chain(start_sid, minifat):
            fat[sid] = FREESECT
            if minifat:
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

        stack =  deque([child])
        count = 0

        while stack:
            current = stack.pop()
            result[current.name] = current
            count += 1

            if count > max_dirs_entries:
                raise CompoundFileBinaryError("corrupt folder structure")

            left = current.left()
            if left:
                stack.append(left)
            right =  current.right()
            if right:
                stack.append(right)

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

    def validate_directory_structure(self):
        for root, storage, stream in self.walk():
            validate_rbtree(root.child())


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
            elif mode == 'rw':
                pass

        s = Stream(self, entry, mode)
        return s
