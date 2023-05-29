from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import sys
from io import BytesIO
import struct
import array

from .utils import (
    write_u8,
    write_u16le,
    safe_print,
    )
from .exceptions import AAFPropertyError, AAFAttachError
from . import properties
from .properties import property_formats
from .auid import AUID

P_HEADER_STRUCT = struct.Struct(str('<BBH'))

OPERATIONGROUP_PARAMETERS_AUID = AUID("06010104-060a-0000-060e-2b3401010102")

sentinel = object()


class AAFObject(object):
    __slots__ = ('class_id', 'root', 'dir', 'property_entries', '__weakref__' )

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
        return self.root.metadict.classdefs_by_auid.get(self.class_id, None)

    @property
    def name(self):
        classdef = self.classdef
        if classdef:
            return classdef.class_name
        return self.__class__.__name__

    @property
    def unique_property(self):
        classdef = self.classdef
        if classdef:
            pid = self.classdef.unique_key_pid
            if pid:
                p = self.property_entries.get(pid, None)
                if p:
                    return p

        raise AAFPropertyError("Object has no unique property")

    @property
    def unique_key(self):
        return self.unique_property.value

    def read_properties(self):
        stream = self.dir.get('properties')
        if stream is None:
            return

        s = stream.open()

        # read the whole stream
        with BytesIO(s.read()) as f:
            (byte_order, version, entry_count) = P_HEADER_STRUCT.unpack(f.read(4))

            if byte_order != 0x4c:
                raise NotImplementedError("be byteorder")

            props = array.array(str('H'))
            if hasattr(props, 'frombytes'):
                props.frombytes(f.read(6 * entry_count))
            else:
                props.fromstring(f.read(6 * entry_count))

            if sys.byteorder == 'big':
                props.byteswap()

            for i in range(entry_count):
                index = i * 3
                pid = props[index + 0]
                format = props[index + 1]
                byte_size = props[index + 2]

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

    def write_properties(self, validate=True):
        if validate:
            self.validate()

        s = self.dir.touch("properties").open(mode='rw')

        with BytesIO() as f:
            byte_order = 0x4c
            entry_count = len(self.property_entries)
            version = properties.PROPERTY_VERSION

            write_u8(f, byte_order)
            write_u8(f, version)
            write_u16le(f, entry_count)

            for p in self.property_entries.values():
                assert p.data is not None
                write_u16le(f, p.pid)
                write_u16le(f, p.format)
                write_u16le(f, len(p.data))

            # write the data
            for p in self.property_entries.values():
                f.write(p.data)

            s.write(f.getvalue())
            s.truncate()
            # write index's
            for p in self.property_entries.values():
                if isinstance(p, (properties.StrongRefSetProperty,
                                  properties.StrongRefVectorProperty,
                                  properties.WeakRefArrayProperty)):
                    p.write_index()

    def detach(self, delete=False):
        items = []
        for item, streams in self.walk_references(topdown=True):
            # store reference not sure if necessary
            items.append(item)

            for pid, p in item.property_entries.items():
                if isinstance(p, (properties.StrongRefProperty,
                                  properties.StrongRefVectorProperty,
                                  properties.StrongRefSetProperty,
                                  properties.StreamProperty)):
                    # converts all internal weakrefs to strongrefs
                    p.detach()

            if item.dir:
                # remove child from object manager
                self.root.manager.pop(item.dir.path(), None)

                # NOTE: do we need to delete directory entry?
                # new objects will overwrite whats there anyway
                # and nothing will point to the old object
                if delete:
                    self.root.cfb.rmtree(item.dir)

                item.dir = None

        # remove self from object manager
        if self.dir:
            self.root.manager.pop(self.dir.path(), None)
            self.dir = None

    def attach(self, dir_entry):
        if self.dir:
            raise AAFAttachError("cannot attached obj to %s already attached to %s" % (dir_entry.path(), self.dir.path()))

        self.dir = dir_entry
        self.dir.class_id = self.class_id

        # add self to modified
        self.root.manager.add_modified(self)

        for pid, p in self.property_entries.items():
            if isinstance(p, (properties.StrongRefProperty,
                              properties.StrongRefVectorProperty,
                              properties.StrongRefSetProperty,
                              properties.StreamProperty)):

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

    def copy(self, new_dir=None, root=None, classdef_cache=None):
        new_obj = self.__class__.__new__(self.__class__)
        classdef_cache = classdef_cache or set()
        root = root or self.root
        new_obj.root = root

        # if copying to new root make sure classdef is defined
        # to prevent excessive calls a cache is used skip already
        # processed classdefs
        if root is not self.root:
            classdef = self.classdef
            if classdef.auid not in classdef_cache:
                root.metadict.register_external_classdef(self.classdef)
                classdef_cache.add(classdef.auid)

        if type(new_obj) is AAFObject:
            new_obj.class_id = self.class_id
        new_obj.dir = new_dir
        if new_dir:
            assert new_dir.storage is root.cfb
            new_obj.dir.class_id = self.class_id

        for pid, p in self.property_entries.items():
            # the pid in the new root could be different
            if pid >= 0x8000 and root is not self.root:
                pdef = new_obj.classdef.lookup_propertydef(p.propertydef.auid)
                assert pdef
                pid = pdef.pid

            new_obj.property_entries[pid] = p.copy(new_obj, pid, classdef_cache)

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

    def get(self, key, default=None, allkeys=True):
        for item in self.properties():
            if item.name == key:
                return item
        if not allkeys:
            return default

        classdef = self.classdef
        for propertydef in classdef.all_propertydefs():
            if propertydef.property_name == key:
                fmt = propertydef.store_format

                # Workaround, for OperationDef Parameters
                # AAF SDK uses a StrongRefSetProperty
                # Spec says its suppose to be a StrongRefVectorProperty
                if propertydef.auid == OPERATIONGROUP_PARAMETERS_AUID:
                    fmt = properties.SF_STRONG_OBJECT_REFERENCE_SET

                p = property_formats[fmt](self, propertydef.pid, fmt)
                return p

        return default

    def getvalue(self, key, default=None):
        if key not in self.keys():
            return default

        p = self.get(key, sentinel)
        if p is sentinel:
            return default
        return p.value

    def __getitem__(self, key):
        result = self.get(key, default=sentinel)
        if result is sentinel:
            raise KeyError(key)
        return result

    def __delitem__(self, key):
        result = self.get(key, default=sentinel, allkeys=False)
        if result is sentinel:
            raise KeyError(key)

        del self.property_entries[result.pid]
        if self.dir:
            self.root.manager.add_modified(self)

    def __contains__(self, key):
        result = self.get(key, default=sentinel, allkeys=False)
        if result is sentinel:
            return False
        return True

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
                safe_print(space, p.name, p.typedef)

                p.value.dump(space + indent)

            if isinstance(p, properties.StrongRefVectorProperty):
                safe_print(space, p.name, p.typedef)
                for obj in p.value:
                    safe_print(space + indent, obj)
                    obj.dump(space + indent*2)
                continue

            if isinstance(p, properties.StrongRefSetProperty):
                safe_print(space, p.name, p.typedef)
                for key, obj in p.items():
                    safe_print(space + indent, obj)
                    obj.dump(space + indent*2)
                continue

            safe_print(space, p.name, p.typedef, p.value)
