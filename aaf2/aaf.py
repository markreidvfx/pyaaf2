
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
from StringIO import StringIO
import traceback

from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    )


from .cfb import (CompoundFileBinary, DirEntry)
from .core import AAFObject
from .properties import SFStrongRef, SFStrongRefArray
from .metadict import MetaDictionary

class AAFFile(object):

    def __init__(self, path, mode='r'):

        if mode in ('r', 'rb'):
            mode = 'rb'
        elif mode in ('r+', 'rb+'):
            mode = 'rb+'
        elif mode in ('w', 'w+', 'wb+'):
            mode = 'wb+'
        else:
            raise Exception("invalid mode: %s" % mode)
        self.mode = mode
        self.f = open(path, mode)
        self.cfb = CompoundFileBinary(self.f)
        self.weakref_table = []

        item = '/MetaDictionary-1'

        item = '/'
        item = '/Header-2'
        item = '/Header-2/Content-3b03'

        self.path_cache = {}
        self.metadict = MetaDictionary(self)

        if mode in ("rb", "rb+"):
            self.metadict.dir = self.cfb.find('/MetaDictionary-1')
            self.path_cache['/MetaDictionary-1'] = self.metadict
            self.root = self.read_object("/")
            self.read_reference_properties()
            self.metadict.read_properties()
            header_pid = 0x02
            self.header = self.root.property_entries[header_pid].value
            self.storage = self.header['Content'].value

    def read_object(self, path):
        if isinstance(path, DirEntry):
            dir_entry = path
            path = dir_entry.path()
            if path in self.path_cache:
                # print(s"UsingCache", path)
                return self.path_cache[path]
        else:
            if path in self.path_cache:
                return self.path_cache[path]

            dir_entry = self.cfb.find(path)

        obj_class = self.metadict.lookup_class(dir_entry.class_id)

        obj = obj_class(self)
        obj.dir = dir_entry
        obj.read_properties()

        self.path_cache[path] = obj
        # obj.dump()
        return obj

    def resovle_weakref(self, index, ref_pid, ref):
        p = self.weakref_prop(index)

        # print("resovle", p, p.pid, ref_pid, ref,)
        # print(p.root.dir.path())
        v = p.value.get(ref)

        # return v
        # raise Exception()
        # traceback.print_stack()
        # ref = p.value[ref]
        return v

    def weakref_prop(self, index):
        path = self.weakref_table[index]
        root = self.root


        for pid in path[:-1]:
            # print(root.dir.path())
            if isinstance(root, MetaDictionary):
                pass
                # print(root.property_entries[pid])

            # print (root.property_entries[pid])

            p = root.property_entries[pid]
            # print(pid, root, p, p.typedef)
            root = p.value



        # print("got", root)
        p = root.property_entries[path[-1]]
        return p

    def read_reference_properties(self):
        f = self.cfb.open("/referenced properties")

        byte_order = read_u8(f)
        if byte_order != 0x4c:
            raise Exception("be byteorder")

        path_count = read_u16le(f)
        pid_count = read_u32le(f)

        self.weakref_table = []
        path = []
        for i in range(pid_count):
            pid = read_u16le(f)
            if pid != 0:
                path.append(pid)
            else:
                self.weakref_table.append(path)
                path = []
        assert len(self.weakref_table) == path_count

        # for i in range(len(self.weakref_table)):
        #     print(self.weakref_path(i))
        # print(self.weakref_table)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __enter__(self):
        return self

    def dump(self):

        self.root.dump()

        # for root, storage, stream in self.cfb.walk():
        #     for item in storage:
        #
        #         path = item.path()
        #         # print(path)
        #         space = " " *len(root.path().split("/")*2)
        #         obj = self.read_object(item)
        #         print(space, obj)
        #
        #         for p in obj.properties():
        #
        #             if isinstance(p, (SFStrongRef, SFStrongRefArray)):
        #                 continue
        #
        #             print(space, "  ", p.name, p.typedef, p.value)


    def close(self):
        self.cfb.close()
