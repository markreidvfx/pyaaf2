
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from io import BytesIO

from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    write_u8,
    write_u16le,
    write_u32le,
    )
from uuid import UUID
from .exceptions import AAFPropertyError, AAFAttachError
from . import properties
from .properties import property_formats

class AAFObject(object):
    class_id = None

    def __new__(cls, *args, **kwargs):
        self = super(AAFObject, cls).__new__(cls)
        self.root = None
        self.dir = None
        self.property_entries = {}
        return self

    def __init__(self, *args, **kwargs):
        pass

    @property
    def classdef(self):
        return self.root.metadict.classdefs_by_uuid.get(self.class_id, None)

    @property
    def name(self):
        classdef = self.classdef
        if classdef:
            return classdef.class_name
        return self.__class__.__name__

    @property
    def unique_key(self):
        classdef = self.classdef
        if classdef:
            pid = self.classdef.unique_key_pid
            if pid:
                p = self.property_entries.get(pid, None)
                if p:
                    return p.value
        raise AAFPropertyError("Object has no unique key")

    def read_properties(self):
        stream = self.dir.get('properties')
        if stream is None:
            return

        s = stream.open()
        # read the whole stream
        f = BytesIO(s.read())

        byte_order = read_u8(f)
        if byte_order != 0x4c:
            raise NotImplementedError("be byteorder")
        version = read_u8(f)
        entry_count = read_u16le(f)

        props = []
        for i in range(entry_count):
            pid = read_u16le(f)
            format = read_u16le(f)
            byte_size = read_u16le(f)

            props.append([pid, format, byte_size])

        for pid, format, byte_size in props:
            data = f.read(byte_size)
            p = property_formats[format](self, pid, format, version)
            p.data = data
            self.property_entries[pid] = p

        for p in self.property_entries.values():
            p.decode()
            if isinstance(p, (properties.StrongRefSetProperty,
                              properties.StrongRefVectorProperty,
                              properties.WeakRefArrayProperty)):
                p.read_index()

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
            raise AAFPropertyError(message)

    def write_properties(self):

        self.validate()

        s = self.dir.touch("properties").open(mode='w')

        f = BytesIO()
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
            if p.data is None:
                print("??", p)
                print("!!", p.data)
                print(p.value)
                raise Exception()

            write_u16le(f, len(p.data))

        # write the data
        for p in self.property_entries.values():
            f.write(p.data)

        s.write(f.getvalue())

        # write index's
        for p in self.property_entries.values():
            if isinstance(p, (properties.StrongRefSetProperty,
                              properties.StrongRefVectorProperty,
                              properties.WeakRefArrayProperty)):
                # print('writing index', self, p)
                p.write_index()


    def detach(self):
        for item, streams in self.walk_references(topdown=True):
            if item.dir:
                # remove from path_cache
                self.root.path_cache.pop(item.dir.path(), None)
                # remove DirEntry from storage
                self.root.cfb.rmtree(item.dir)

                item.dir = None
        self.dir = None


    def attach(self, dir_entry):
        if self.dir:
            raise AAFAttachError("object already attached to %s" % (self.dir.path()))

        self.dir = dir_entry
        self.dir.class_id = self.class_id
        self.root.path_cache[dir_entry.path()] = self
        # print("attach: %s" % self.dir.path(), self)
        for pid, p in self.property_entries.items():
            if isinstance(p, (properties.StrongRefProperty,
                              properties.StrongRefArrayProperty)):

                p.attach()

    def walk_references(self, topdown=False):

        refs = []
        streams = []
        for p in self.properties():
            if isinstance(p, properties.StrongRefProperty):
                obj = p.value
                if obj:
                    refs.append(obj)

            elif isinstance(p, properties.StrongRefVectorProperty):
                for v in p.value:
                    refs.append(v)

            elif isinstance(p, properties.StrongRefSetProperty):

                for obj in p.value:
                    refs.append(obj)

            elif isinstance(p, properties.StreamProperty):
                streams.append(p)

        if not topdown:
            yield self, streams

        for obj in refs:
            for item, item_streams in obj.walk_references(topdown):
                yield item, item_streams

        if topdown:
            yield self, streams

    def copy(self, new_dir=None):
        # new_obj = self.__class__(self.root)
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.root = self.root
        new_obj.class_id = self.class_id
        new_obj.dir = new_dir
        new_obj.dir.class_id = self.class_id

        for pid, p in self.property_entries.items():
            new_obj.property_entries[pid] = p.copy(new_obj)

        return new_obj

    def properties(self):

        for pid, p in self.property_entries.items():
            yield p

    def allkeys(self):
        keys = []
        classdef = self.classdef
        if not classdef:
            return keys
        for propertydef in classdef.all_propertydefs():
            keys.append(propertydef.property_name)
        return keys

    def keys(self):
        keys = []
        for pid, p in self.property_entries.items():
            keys.append(p.name)
        return keys

    def get(self, key, default=None):
        for item in self.properties():
            if item.name == key:
                return item

        classdef = self.classdef
        for propertydef in classdef.all_propertydefs():
            if propertydef.property_name == key:
                fmt = propertydef.store_format

                # OperationDef Parameters spec seems incorrect
                if propertydef.uuid == UUID("06010104-060a-0000-060e-2b3401010102"):
                    fmt = properties.SF_STRONG_OBJECT_REFERENCE_SET

                p = property_formats[fmt](self, propertydef.pid, fmt)
                return p

        return default

    def getvalue(self, key, default=None):
        if not key in self.keys():
            return default

        p = self.get(key, None)
        if p is None:
            return default
        return p.value

    def __getitem__(self, key):
        result = self.get(key, default=None)
        if result is None:
            raise KeyError(key)
        return result

    def __repr__(self):
        s = "%s.%s" % (self.__class__.__module__,
                                self.__class__.__name__)
        name = self.name
        if name:
            s += ' %s' % name

        return '<%s at 0x%x>' % (s, id(self))

    def dump(self, space=""):

        indent = "  "

        for p in self.properties():

            if isinstance(p, properties.StrongRefProperty):
                print(space, p.name, p.typedef)

                p.value.dump(space + indent)

            if isinstance(p, properties.StrongRefVectorProperty):
                print(space, p.name, p.typedef)
                for obj in p.value:
                    print(space + indent, obj)
                    obj.dump(space + indent*2)
                continue

            if isinstance(p, properties.StrongRefSetProperty):
                print(space, p.name, p.typedef)
                for key, obj in p.items():
                    print(space + indent, obj)
                    obj.dump(space + indent*2)

                continue
                # print(space, p.name,  p.typedef)

            print(space, p.name, p.typedef, p.value)
