
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
    write_u8,
    write_u16le,
    write_u32le,
    )

from . import properties
from .properties import property_formats

class AAFObject(object):
    class_id = None
    def __init__(self, root=None,):
        self.root = root
        self.dir = None
        self.property_entries = {}
        self.class_id = self.class_id

    @property
    def classdef(self):
        return self.root.metadict.classdefs_by_uuid.get(self.class_id, None)

    @property
    def name(self):
        classdef = self.classdef
        if classdef:
            return classdef.class_name
        return self.__class__.__name__

    def read_properties(self):

        stream = self.dir.get('properties')
        if stream is None:
            return

        f = stream.open()

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

            p = property_formats[format](self, pid, format, version)
            p.decode(data)
            self.property_entries[pid] = p

    def validate(self):
        missing = []

        for propertydef in self.classdef.all_propertydefs():

            if propertydef.optional:
                continue

            if propertydef.pid in self.property_entries:
                continue

            # stored on dir entry I guess...
            if propertydef.property_name in ('ObjClass',):
                continue

            missing.append(propertydef)

        if missing:
            m = []
            for p in missing:
                m.append("%s %s" % (p.property_name, str(p.typedef)))
            message = "%s missing the following required properties:\n    %s" % (str(self), "\n    ".join(m))
            raise Exception(message)

    def write_properties(self):

        self.validate()

        f = self.dir.touch("properties").open(mode='w')
        # print("writing", f.dir.path())
        byte_order = 0x4c
        entry_count = len(self.property_entries)
        version = properties.PROPERTY_VERSION

        write_u8(f, byte_order)
        write_u8(f, version)
        write_u16le(f, entry_count)

        for p in self.property_entries.values():
            write_u16le(f, p.pid)
            write_u16le(f, p.format)
            write_u16le(f, len(p.data))

        # write the data
        for p in self.property_entries.values():
            f.write(p.data)

        # write index's
        for p in self.property_entries.values():
            if isinstance(p, (properties.SFStrongRefSet,
                              properties.SFStrongRefVector,
                              properties.SFWeakRefArray)):
                # print('writing index', self, p)
                p.write_index()


    def detach(self):
        pass

    def attach(self, dir_entry):
        if self.dir:
            self.detach()

        self.dir = dir_entry
        self.dir.class_id = self.class_id
        self.root.path_cache[dir_entry.path()] = self

        for pid, p in self.property_entries.items():
            if isinstance(p, (properties.SFStrongRef,
                              properties.SFStrongRefVector,
                              properties.SFStrongRefSet)):
                p.attach()



    def walk_references(self, topdown=False):

        if not topdown:
            yield self

        refs = []
        for pid, p in self.property_entries.items():
            if isinstance(p, properties.SFStrongRef):
                obj = p.value
                if obj:
                    refs.append(obj)

            if isinstance(p, properties.SFStrongRefVector):
                refs.extend(p.value)

            if isinstance(p, properties.SFStrongRefSet):
                refs.extend([obj for key, obj in p.items()])

        for obj in refs:

            for item in obj.walk_references(topdown):
                yield item

        if topdown:
            yield self

    def properties(self):

        for pid, p in self.property_entries.items():
            yield p

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

        classdef = self.classdef
        for propertydef in classdef.all_propertydefs():
            if propertydef.property_name == key:
                fmt = propertydef.store_format
                # print(fmt,propertydef.typedef)
                p = property_formats[fmt](self, propertydef.pid, fmt)
                return p

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
