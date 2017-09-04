
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from StringIO import StringIO

from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    )

from . import properties
from .properties import property_formats

class AAFObject(object):
    def __init__(self, root=None,):
        self.root = root
        self.dir = None
        self.property_entries = {}

    @property
    def classdef(self):

        # if self.dir.path() == "/":
        #     return self.root.metadict.classdefs_by_name['Root']
        #
        if self.dir:
            return self.root.metadict.classdefs_by_uuid.get(self.dir.class_id, None)

    @property
    def name(self):
        classdef = self.classdef
        if classdef:
            return classdef.class_name
        return self.__class__.__name__

    def read_properties(self):
        f = self.dir.get('properties').open()

        byte_order = read_u8(f)
        if byte_order != 0x4c:
            raise Exception("be byteorder")
        version = read_u8(f)
        entry_count = read_u16le(f)

        props = []
        for i in range(entry_count):
            pid = read_u16le(f)
            format = read_u16le(f)
            byte_size = read_u16le(f)

            props.append([pid, format, byte_size])

        for pid, format, byte_size in props:
            # print(self.root.f.tell())
            data = f.read(byte_size)

            if format == 0x42:
                pass
            p = property_formats[format](self, pid, format, version)
            p.decode(data)
            self.property_entries[pid] = p


    def dump(self):
        print(self.dir.path())
        for p in self.property_entries:
            print(" |-", p, p.value)

    def properties(self):

        for pid, p in self.property_entries.items():
            yield p

        # list(self.classdef.all_propertydefs())
        # for propertydef in self.classdef.all_propertydefs():
        #
        #     if propertydef.pid in self.property_entries:
        #         yield self.property_entries[propertydef.pid]
        #     else:
        #         # create PropertyItem
        #         pass

    def keys(self):
        keys = []
        classdef = self.classdef
        if not classdef:
            return keys
        for propertydef in classdef.all_propertydefs():
            keys.append(propertydef.property_name)
        return keys

    def get(self, key, default=None):
        for item in self.properties():
            if item.name == key:
                return item
        return default

    def get_value(self, key, default=None):
        p = self.get(key, None)
        if p is None:
            return None
        return p.value

    def __getitem__(self, key):
        result =self.get(key, default=None)
        if result is None:
            raise KeyError(key)
        return result

    def __repr__(self):

        return "<%s>" % (self.name)

    def dump(self, space=""):

        indent = "  "

        for p in self.properties():

            if isinstance(p, properties.SFStrongRef):
                print(space, p.name, p.typedef)

                p.value.dump(space + indent)

            if isinstance(p, properties.SFStrongRefVector):
                print(space, p.name, p.typedef)
                for obj in p.value:
                    print(space + indent, obj)
                    obj.dump(space + indent*2)
                continue

            if isinstance(p, properties.SFStrongRefSet):
                print(space, p.name, p.typedef)
                for key, obj in p.items():
                    print(space + indent, obj)
                    obj.dump(space + indent*2)

                continue
                # print(space, p.name,  p.typedef)

            print(space, p.name, p.typedef, p.value)
