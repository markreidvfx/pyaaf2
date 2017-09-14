
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
from StringIO import StringIO
import traceback
import os
from uuid import UUID, uuid4
import sys
import datetime

from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    write_u8,
    write_u16le,
    write_u32le,
    )


from .cfb import (CompoundFileBinary, DirEntry)
from .core import AAFObject
from .properties import SFStrongRef, SFStrongRefArray, SFStrongRefSet
from .metadict import MetaDictionary


class AAFFactory(object):

    def __init__(self, root):
        self.root = root
        self.metadict = root.metadict
        self.class_name = None

    def __getattr__(self, name):
        self.class_name = name
        return self.create_instance

    def from_name(self, name, *args, **kwargs):

        classdef = self.metadict.lookup_classdef(name)
        if classdef is None:
            raise Exception("no class found with name: %s" % name)

        classobj = self.metadict.lookup_class(name)

        obj = classobj(self.root, *args, **kwargs)
        if isinstance(obj, AAFObject):
            obj.class_id = classdef.uuid

        return obj

    def create_instance(self, *args, **kwargs):
        return self.from_name(self.class_name, *args, **kwargs)

class AAFFile(object):

    def __init__(self, path=None, mode='r'):

        if mode in ('r', 'rb'):
            mode = 'rb'
        elif mode in ('r+', 'rb+'):
            mode = 'rb+'
        elif mode in ('w', 'w+', 'wb+'):
            mode = 'wb+'
        else:
            raise Exception("invalid mode: %s" % mode)
        self.mode = mode
        if path is None:
            self.mode = 'wb+'
            self.f = StringIO()
        else:
            self.f = open(path, mode)
        self.cfb = CompoundFileBinary(self.f)
        self.weakref_table = []
        self.path_cache = {}
        self.metadict = MetaDictionary(self)
        self.create = AAFFactory(self)

        if self.mode in ("rb", "rb+"):
            self.metadict.dir = self.cfb.find('/MetaDictionary-1')
            self.path_cache['/MetaDictionary-1'] = self.metadict
            self.root = self.read_object("/")
            self.read_reference_properties()
            self.metadict.read_properties()
            header_pid = 0x02
            self.header = self.root.property_entries[header_pid].value
            self.storage = self.header['Content'].value

        elif self.mode in ("wb+",):
            self.setup_empty()

    def setup_empty(self):
        now = datetime.datetime.now()
        self.root = self.create.Root()
        self.root.attach(self.cfb.find("/"))
        self.root['MetaDictionary'].value = self.metadict
        self.metadict.setup_defaults()

        self.header = self.create.Header()
        self.root['Header'].value = self.header
        self.storage = self.create.ContentStorage()
        d = self.create.Dictionary()
        self.header['Dictionary'].value = d
        d.setup_defaults()
        self.header['Content'].value = self.storage
        self.header['OperationalPattern'].value = UUID("0d011201-0100-0000-060e-2b3404010105")
        self.header['ObjectModelVersion'].value = 1
        self.header['Version'].value =  {u'major': 1, u'minor': 1}

        i = self.create.Identification()
        i['ProductName'].value = "PyAAF"
        i['CompanyName'].value = "CompanyName"
        i['ProductVersionString'].value = '2.0.0'
        i['ProductID'].value = UUID("97e04c67-dbe6-4d11-bcd7-3a3a4253a2ef")
        i['Date'].value = now
        i['Platform'].value = sys.platform
        i['GenerationAUID'].value = uuid4()

        self.header['IdentificationList'].value = [i]
        self.header['LastModified'].value = now
        self.header['ByteOrder'].value = 0x4949

        self.storage['Mobs'].value = []

    def read_object(self, path):
        if isinstance(path, DirEntry):
            dir_entry = path
            path = dir_entry.path()
            if path in self.path_cache:
                return self.path_cache[path]
        else:
            if path in self.path_cache:
                return self.path_cache[path]

            dir_entry = self.cfb.find(path)

        if dir_entry is None:
            raise Exception("cannot find path: %s" % path)

        obj_class = self.metadict.lookup_class(dir_entry.class_id)

        obj = obj_class(self)
        obj.dir = dir_entry
        if obj_class is AAFObject:
            obj.class_id = dir_entry.class_id
        obj.read_properties()

        self.path_cache[path] = obj
        # obj.dump()
        return obj

    def resovle_weakref(self, index, ref_pid, ref):
        # print(index, ref_pid, ref)
        parent, p = self.weakref_prop(index)
        v = p.value.get(ref)
        return v

    def weakref_prop(self, index):
        path = self.weakref_table[index]
        root = self.root

        for pid in path[:-1]:
            p = root.property_entries[pid]
            root = p.value

        p = root.property_entries[path[-1]]
        return root, p

    def create_weakref(self, obj, pid_path):

        if pid_path in self.weakref_table:
            index = self.weakref_table.index(pid_path)
        else:
            index = len(self.weakref_table)
            self.weakref_table.append(pid_path)

        parent_obj, p = self.weakref_prop(index)
        assert isinstance(p, SFStrongRefSet)
        weakref_pid, key_size = self.metadict.weakref_pid(parent_obj.classdef, p.propertydef)

        ref_key = None
        for key, value in p.items():
            if value is obj:
                ref_key = key
                break

        if ref_key is None:
            raise Exception("can not find ref_key")

        return index, weakref_pid, ref_key

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

    def write_reference_properties(self):
        f = self.cfb.open("/referenced properties", 'w')
        byte_order = 0x4c
        path_count = len(self.weakref_table)
        pid_count = 0
        for path in self.weakref_table:
            pid_count += len(path)
            pid_count += 1 # null byte

        write_u8(f, byte_order)
        write_u16le(f, path_count)
        write_u32le(f, pid_count)
        for path in self.weakref_table:
            for pid in path:
                write_u16le(f, pid)
            write_u16le(f, 0) # null terminated

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()

    def __enter__(self):
        return self

    def dump(self):
        self.root.dump()

    def save(self):
        if self.mode in ("wb+", 'rb+'):
            self.write_reference_properties()
            for path, obj in self.path_cache.items():
                # print(path, obj)
                obj.write_properties()

        self.cfb.close()
