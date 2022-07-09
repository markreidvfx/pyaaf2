
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
from io import BytesIO
import io
import traceback
import os
from uuid import uuid4
import sys
import datetime
import weakref
from .utils import (
    read_u8,
    read_u16le,
    read_u32le,
    write_u8,
    write_u16le,
    write_u32le,
    )

from .auid import AUID
from .cfb import (CompoundFileBinary, DirEntry)
from .core import AAFObject
from .metadict import MetaDictionary
from .cache import LRUCacheDict

class AAFFactory(object):

    def __init__(self, root):
        self.root = root
        self.class_name = None

    def __getattr__(self, name):
        self.class_name = name
        return self.create_instance

    def from_name(self, name, *args, **kwargs):
        classdef = self.root.metadict.lookup_classdef(name)
        if classdef is None:
            raise ValueError("no class found with name: %s" % name)

        if not classdef.concrete:
            raise ValueError("cannot initialize abstract class: %s" % name)

        classobj = self.root.metadict.lookup_class(name)

        # obj = classobj(None, *args, **kwargs)
        obj = classobj.__new__(classobj)
        obj.root = self.root
        obj.__init__(*args, **kwargs)

        # if a helper class is not found set class_id
        if type(obj) is AAFObject:
            obj.class_id = classdef.auid

        return obj

    def create_instance(self, *args, **kwargs):
        return self.from_name(self.class_name, *args, **kwargs)

class AAFObjectManager(object):

    def __init__(self, root):
        self.root = root
        self.path_cache = weakref.WeakValueDictionary()
        self.lru_cache = LRUCacheDict()
        # to hold onto modified objects
        self.modified = {}

    def create_temp_dir(self):
        return self.root.cfb.makedirs("/tmp/" + str(uuid4()).replace('-', '/'))

    def remove_temp(self):
        if self.root.cfb.exists("/tmp"):
            self.root.cfb.rmtree("/tmp")

    def add_modified(self, obj):
        if self.root.mode == 'rb':
            raise ValueError("cannot modify read only file")

        path = obj.dir.path()
        self.modified[path] = obj
        self[path] = obj

    def pop(self, path, default=None):
        cached_obj = self.path_cache.pop(path, default)
        modified_obj = self.modified.pop(path, default)
        if path in self.lru_cache:
            del self.lru_cache[path]

        return modified_obj or cached_obj

    def __setitem__(self, key, value):
        self.lru_cache[key] = value
        self.path_cache[key] = value

    def read_object(self, path):
        if isinstance(path, DirEntry):
            dir_entry = path
            path = dir_entry.path()
            obj = self.path_cache.get(path, None)
            if obj is not None:
                return obj
        else:
            obj = self.path_cache.get(path, None)
            if obj is not None:
                return obj

            dir_entry = self.root.cfb.find(path)

        if dir_entry is None:
            raise ValueError("cannot find path: %s" % path)

        obj_class = self.root.metadict.lookup_class(dir_entry.class_id)

        # NOTE: objects read from file do not run __init__
        obj = obj_class.__new__(obj_class)
        obj.root = self.root
        obj.dir = dir_entry
        if obj_class is AAFObject:
            obj.class_id = dir_entry.class_id
        obj.read_properties()

        self[path] = obj
        # obj.dump()
        return obj

    def write_objects(self):
        written = []
        for path, obj in self.modified.items():
            try:
                obj.write_properties()
                written.append(path)
            except:
                print("failed to write: %s %s" %  (str(path), str(obj)))
                raise

        # no longer need to be in modified
        for path in written:
            self.modified.pop(path)

class AAFFile(object):
    """
    AAF File Object. This is the entry point object for most of the API.
    This object is designed to be like python's native open function.
    It is recommended to create this object with the `aaf.open` alias.
    It is also highly recommended to use the with statement.

    .. warning::
       If an exception is raised inside the with block and the file was opened
       as writable, the final file should be considered bad or corrupted.

       Take this snippet as an example:

       .. code-block:: python

           try:
               with aaf.open('/path/to/aaf_file.aaf', 'r+') as f:
                   raise ValueError('asd')
           except:
               pass

       in this case, even if the exception is properly handled, the content
       of ``/path/to/aaf_file.aaf`` shouldn't be trusted anymore.

    For example. Opening existing AAF file readonly::

        with aaf.open('/path/to/aaf_file.aaf', 'r') as f:

    Opening new AAF file overwriting existing one::

        with aaf.open('/path/to/aaf_file.aaf', 'w') as f:

    Opening existing AAF in read and write::

        with aaf.open('/path/to/aaf_file.aaf', 'rw') as f:

    Opening in memory BytesIO file::

        with aaf.open() as f:
    """

    def __init__(self, path=None, mode='r', sector_size=4096, extensions=True, buffering=io.DEFAULT_BUFFER_SIZE):

        if mode in ('r', 'rb'):
            mode = 'rb'
        elif mode in ('r+', 'rb+', 'rw'):
            mode = 'rb+'
        elif mode in ('w', 'w+', 'wb+'):
            mode = 'wb+'
        else:
            raise ValueError("invalid mode: %s" % mode)
        self.mode = mode
        if path is None:
            self.mode = 'wb+'
            self.f = BytesIO()
        else:
            self.f = io.open(path, mode, buffering=buffering)

        self.cfb = CompoundFileBinary(self.f, self.mode, sector_size=sector_size)
        self.weakref_table = []
        self.manager = AAFObjectManager(self)
        self.create = AAFFactory(self)
        self.is_open = True

        if self.mode in ("rb", "rb+"):
            self.read_reference_properties()
            self.metadict = MetaDictionary(self)
            self.metadict.dir = self.cfb.find('/MetaDictionary-1')
            self.manager['/MetaDictionary-1'] = self.metadict
            self.root = self.manager.read_object("/")
            self.metadict.read_properties()

        elif self.mode in ("wb+",):
            self.setup_empty()

        if extensions and self.writeable:
            self.metadict.register_extensions()

    @property
    def header(self):
        """
        :class:`aaf2.content.Header` object for AAF file.
        """
        header_pid = 0x02
        return self.root.property_entries[header_pid].value

    @property
    def content(self):
        """
        :class:`aaf2.content.ContentStorage` object for AAF File. This has the Mob and EssenceData objects.
        """
        return self.header['Content'].value

    @property
    def dictionary(self):
        """
        :class:`aaf2.dictionary.Dictionary` for AAF file.  The dictionary property has DefinitionObject objects.
        """
        return self.header['Dictionary'].value

    def setup_empty(self):
        now = datetime.datetime.now()
        self.metadict = MetaDictionary(self)
        self.root = self.create.Root()
        self.root.attach(self.cfb.find("/"))
        self.root['MetaDictionary'].value = self.metadict
        self.root['Header'].value = self.create.Header()

        self.header['Dictionary'].value = self.create.Dictionary()
        self.dictionary.setup_defaults()

        self.header['Content'].value = self.create.ContentStorage()
        self.header['OperationalPattern'].value = AUID("0d011201-0100-0000-060e-2b3404010105")
        self.header['ObjectModelVersion'].value = 1
        self.header['Version'].value =  {u'major': 1, u'minor': 2}

        i = self.create.Identification()
        i['ProductName'].value = "PyAAF"
        i['CompanyName'].value = "CompanyName"
        i['ProductVersionString'].value = '2.0.0'
        i['ProductID'].value = AUID("97e04c67-dbe6-4d11-bcd7-3a3a4253a2ef")
        i['Date'].value = now
        i['Platform'].value = sys.platform
        i['GenerationAUID'].value = uuid4()

        self.header['IdentificationList'].value = [i]
        self.header['LastModified'].value = now
        self.header['ByteOrder'].value = 0x4949

        self.content['Mobs'].value = []

    @property
    def writeable(self):
        return self.mode in ("wb+", "rb+")

    def resovle_weakref(self, index, ref_pid, ref):
        parent, p = self.weakref_prop(index)
        return p[ref]

    def weakref_prop(self, index):
        path = self.weakref_table[index]
        root = self.root

        for pid in path[:-1]:
            p = root.property_entries[pid]
            root = p.value

        p = root.property_entries[path[-1]]
        return root, p

    def weakref_index(self, pid_path):

        if pid_path in self.weakref_table:
            index = self.weakref_table.index(pid_path)
        else:
            index = len(self.weakref_table)
            self.weakref_table.append(pid_path)

        return index

    def read_reference_properties(self):
        s = self.cfb.open("/referenced properties")
        with io.BytesIO(s.read()) as f:

            byte_order = read_u8(f)
            if byte_order != 0x4c:
                raise NotImplementedError("be byteorder")

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
        if (exc_type is None and exc_value is None and traceback is None):
            self.close()
        else:
            self.is_open = False
            try:
                self.cfb.close()
            finally:
                self.f.close()

    def __enter__(self):
        return self

    def dump(self):
        self.root.dump()

    def save(self):
        """
        Writes current changes to disk and flushes modified objects in the
        AAFObjectManager
        """
        if self.mode in ("wb+", 'rb+'):
            if not self.is_open:
                raise IOError("file closed")
            self.write_reference_properties()
            self.manager.write_objects()

    def close(self):
        """
        Close the file. A closed file cannot be read or written any more.
        """
        self.save()
        self.manager.remove_temp()
        self.cfb.close()
        self.is_open = False
        self.f.close()
