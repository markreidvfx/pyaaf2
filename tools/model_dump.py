from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from aaf2 import cfb, mobid

from uuid import UUID
from io import BytesIO
from struct import unpack
import pprint

from aaf2.utils import (
    read_u8,
    read_u16le,
    read_u32le,
    decode_utf16le,
    mangle_name
    )

MetaDictionary = UUID("0d010101-0225-0000-060e-2b3402060101")

CLASSDEFINITIONS_PID = 0x0003
TYPEDEFINITIONS_PID  = 0x0004

IDENTIFICATION_PID  = 0x0005
DESCRIPTION_PID     = 0x0007
NAME_PID            = 0x0006

TypeDefInt          = UUID("0d010101-0204-0000-060e-2b3402060101")
TypeDefInt_IsSigned = 0x0010
TypeDefInt_Size     = 0x000F

TypeDefStrongRef                = UUID("0d010101-0205-0000-060e-2b3402060101")
TypeDefStrongRef_ReferencedType = 0x0011

TypeDefWeakRef                = UUID("0d010101-0206-0000-060e-2b3402060101")
TypeDefWeakRef_ReferencedType = 0x0012
TypeDefWeakRef_TargetSet      = 0x0013

TypeDefEnum               = UUID("0d010101-0207-0000-060e-2b3402060101")
TypeDefEnum_ElementType   = 0x0014
TypeDefEnum_ElementValues = 0x0016
TypeDefEnum_ElementNames  = 0x0015

TypeDefFixedArray               = UUID("0d010101-0208-0000-060e-2b3402060101")
TypeDefFixedArray_ElementCount  = 0x0018
TypeDefFixedArray_ElementType   = 0x0017

TypeDefVariableArray             = UUID("0d010101-0209-0000-060e-2b3402060101")
TypeDefVariableArray_ElementType = 0x0019

TypeDefSet             = UUID("0d010101-020a-0000-060e-2b3402060101")
TypeDefSet_ElementType = 0x001A

TypeDefString             = UUID("0d010101-020b-0000-060e-2b3402060101")
TypeDefString_ElementType = 0x001B

TypeDefStream             = UUID("0d010101-020c-0000-060e-2b3402060101")

TypeDefRecord             = UUID("0d010101-020d-0000-060e-2b3402060101")
TypeDefRecord_MemberNames = 0x001D
TypeDefRecord_MemberTypes = 0x001C

TypeDefRename             = UUID("0d010101-020e-0000-060e-2b3402060101")
TypeDefRename_RenamedType = 0x001E

TypeDefExtendibleEnum               = UUID("0d010101-0220-0000-060e-2b3402060101")
TypeDefExtendibleEnum_ElementValues = 0x0020
TypeDefExtendibleEnum_ElementNames  = 0x001F

TypeDefIndirect                 = UUID("0d010101-0221-0000-060e-2b3402060101")
TypeDefOpaque                   = UUID("0d010101-0222-0000-060e-2b3402060101")
TypeDefCharacter                = UUID("0d010101-0223-0000-060e-2b3402060101")
TypeDefGenericCharacter         = UUID("0e040101-0000-0000-060e-2b3402060101")


ClassDef                           = UUID("0d010101-0201-0000-060e-2b3402060101")
ClassDef_ParentClass               = 0x0008
ClassDef_Properties                = 0x0009
ClassDef_IsConcrete                = 0x000A

PropertyDef                        = UUID("0d010101-0202-0000-060e-2b3402060101")
PropertyDef_Type                   = 0x000B
PropertyDef_IsOptional             = 0x000C
PropertyDef_LocalIdentification    = 0x000D
PropertyDef_IsUniqueIdentifier     = 0x000E

typedef_cats= ("ints", "enums", "records", "fixed_arrays", "var_arrays",
               "renames", "strings", "streams", "opaques", "extenums",
               "chars", "generic_chars", "indirects", "sets", "strongrefs", "weakrefs")

root_class = (UUID('b3b398a5-1c90-11d4-8053-080036210804'), None, True, {
    "Header"              : (UUID('0d010301-0102-0100-060e-2b3401010102'), 0x0002, "HeaderStrongRefence", False, False),
    "MetaDictionary"      : (UUID('0d010301-0101-0100-060e-2b3401010102'), 0x0001, "MetaDictionaryStrongReference", False, False),
    })

def read_properties(entry):
    stream = entry.get('properties')
    if stream is None:
        raise Exception("can not find properties")

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

    property_entries = {}
    for pid, format, byte_size in props:
        data = f.read(byte_size)
        property_entries[pid] = data

    return property_entries

def read_reference_properties(cfb):
    f = cfb.open("/referenced properties")

    byte_order = read_u8(f)
    if byte_order != 0x4c:
        raise NotImplementedError("be byteorder")

    path_count = read_u16le(f)
    pid_count = read_u32le(f)

    weakref_table = []
    path = []
    for i in range(pid_count):
        pid = read_u16le(f)
        if pid != 0:
            path.append(pid)
        else:
            weakref_table.append(path)
            path = []
    assert len(weakref_table) == path_count
    return weakref_table

def decode_weakref(data):
    f = BytesIO(data)
    weakref_index = read_u16le(f)
    key_pid = read_u16le(f)
    key_size = read_u8(f)
    assert key_size in (16, 32)
    if key_size == 16:
        ref = UUID(bytes_le=f.read(key_size))
    else:
        ref = key = MobID(bytes_le=f.read(key_size))
    return ref

def decode_auid_array(data):
    f = BytesIO(data)
    result = []

    while True:
        d = f.read(16)
        if not d:
            break

        if len(d) == 16:
            result.append(UUID(bytes_le=d))
        else:
            raise Exception("auid length wrong: %d" % len(d))

    return result

def decode_utf16_array(data):
    start = 0
    data = bytearray(data)
    result = []
    for i in range(0, len(data), 2):
        if data[i] == 0x00 and data[i+1] == 0x00:
            result.append(data[start:i].decode("utf-16le"))
            start = i+2
    return result

def read_set_index(entry):

    s = entry.open('r')
    # read the whole of the index
    f = BytesIO(s.read())

    count = read_u32le(f)
    next_free_key = read_u32le(f)
    last_free_key = read_u32le(f)
    key_pid = read_u16le(f)
    key_size = read_u8(f)
    assert key_size in (16, 32)

    references = []

    for i in range(count):
        local_key = read_u32le(f)
        ref_count = read_u32le(f)

        # not sure if ref count is actually used
        # doesn't apear to be
        assert ref_count == 1

        if key_size == 16:
            key = UUID(bytes_le=f.read(key_size))
        else:
            key = mobid.MobID(bytes_le=f.read(key_size))
        references.append((key, local_key))
        # references[key] = local_key

    return references

def read_weakref_array_index(entry):
    s = entry.open('r')
    # read the whole index
    f = BytesIO(s.read())

    count = read_u32le(f)
    weakref_index = read_u16le(f)
    key_pid = read_u16le(f)
    key_size = read_u8(f)
    assert key_size in (16, 32)
    references = []
    for i in range(count):
        if key_size == 16:
            key = UUID(bytes_le=f.read(key_size))
        else:
            key = key = MobID(bytes_le=f.read(key_size))
        references.append(key)
    return references

def read_typedef(entry, types):
    p  = read_properties(entry)
    name = decode_utf16le(p[NAME_PID])
    identification = UUID(bytes_le=p[IDENTIFICATION_PID])
    types['all'][identification] = name
    # description = decode_utf16le(p[DESCRIPTION_PID])
    # print(name, description)

    data = [identification]

    if entry.class_id == TypeDefInt:
        size = read_u8(BytesIO(p[TypeDefInt_Size]))
        signed = p[TypeDefInt_IsSigned] == b"\x01"
        data.extend([size, signed])
        types['ints'][name] = data

    elif entry.class_id == TypeDefStrongRef:
        ref_type = decode_weakref(p[TypeDefStrongRef_ReferencedType])
        data.extend([ref_type])
        types['strongrefs'][name] = data

    elif entry.class_id == TypeDefWeakRef:
        ref_type = decode_weakref(p[TypeDefWeakRef_ReferencedType])
        target_set = decode_auid_array(p[TypeDefWeakRef_TargetSet])
        data.extend([ref_type, target_set])
        types['weakrefs'][name] = data

    elif entry.class_id  == TypeDefEnum:
        type = decode_weakref(p[TypeDefEnum_ElementType])
        names = decode_utf16_array(p[TypeDefEnum_ElementNames])

        # aafInt64Array
        values = p[TypeDefEnum_ElementValues]
        size = 8
        elements = len(values)//size
        values = unpack('<%dq'% elements, values)

        data.extend([type, dict(zip(values, names))])
        types['enums'][name] = data

    elif entry.class_id == TypeDefFixedArray:
        # aafUInt32
        elements = read_u32le(BytesIO(p[TypeDefFixedArray_ElementCount]))
        type = decode_weakref(p[TypeDefFixedArray_ElementType])
        data.extend([type, elements])
        types['fixed_arrays'][name] = data

    elif entry.class_id == TypeDefVariableArray:
        type = decode_weakref(p[TypeDefVariableArray_ElementType])
        data.extend([type])
        types['var_arrays'][name] = data

    elif entry.class_id == TypeDefSet:
        type = decode_weakref(p[TypeDefSet_ElementType])
        data.extend([type])
        types['sets'][name] = data

    elif entry.class_id == TypeDefString:
        type = decode_weakref(p[TypeDefString_ElementType])
        data.extend([type])
        types['strings'][name] = data

    elif entry.class_id == TypeDefStream:
        types['streams'][name] = data

    elif entry.class_id == TypeDefRecord:
        member_names = decode_utf16_array(p[TypeDefRecord_MemberNames])
        member_index_name = decode_utf16le(p[TypeDefRecord_MemberTypes])
        member_types = read_weakref_array_index(entry.get(member_index_name + " index"))
        data.append(list(zip(member_names, member_types)))
        types['records'][name] = data

    elif entry.class_id == TypeDefRename:
        type = decode_weakref(p[TypeDefRename_RenamedType])
        data.extend([type])
        types['renames'][name] = data

    elif entry.class_id == TypeDefExtendibleEnum:
        element_values = decode_auid_array(p[TypeDefExtendibleEnum_ElementValues])
        element_names = decode_utf16_array(p[TypeDefExtendibleEnum_ElementNames])
        data.extend([dict(zip(element_values, element_names))])
        types['extenums'][name] = data

    elif entry.class_id == TypeDefIndirect:
        types['indirects'][name] = data
    elif entry.class_id == TypeDefOpaque:
        types['opaques'][name] = data
    elif entry.class_id == TypeDefCharacter:
        types['chars'][name] = data
    elif entry.class_id == TypeDefGenericCharacter:
        print(p)
        raise Exception
        types['generic_chars'][name] = data
    else:
        raise ValueError("Unknown TypeDef: " + str(entry.class_id))

def read_propertdef(entry):
    p  = read_properties(entry)
    name = decode_utf16le(p[NAME_PID])
    #hacks for now, should really be property aliases
    if name == 'MediaStreamPluginGUID':
        name = 'MediaContainerGUID'

    if name == 'CommentMarkerUSer':
        name = 'CommentMarkerUser'

    identification = UUID(bytes_le=p[IDENTIFICATION_PID])

    typedef =  UUID(bytes_le=p[PropertyDef_Type])
    is_optional = p[PropertyDef_IsOptional] == b"\x01"
    local_id = read_u16le(BytesIO(p[PropertyDef_LocalIdentification]))

    data = [identification, local_id, typedef, is_optional]

    if PropertyDef_IsUniqueIdentifier in p:
        is_unique = p[PropertyDef_IsUniqueIdentifier]  == b"\x01"
        data.append(is_unique)
    else:
        data.append(False)

    return name, data

def read_classdef(entry):
    p  = read_properties(entry)
    name = decode_utf16le(p[NAME_PID])
    identification = UUID(bytes_le=p[IDENTIFICATION_PID])
    parent_class = decode_weakref(p[ClassDef_ParentClass])
    is_concrete = p[ClassDef_IsConcrete] == b"\x01"
    data = [identification, parent_class, is_concrete]
    properties = {}
    if ClassDef_Properties in p:
        index_name = decode_utf16le(p[ClassDef_Properties])
        property_reference_keys = read_set_index(entry.get(index_name + " index"))
        # print(entry.listdir())
        for key, local_key in property_reference_keys:
            dirname = "%s{%x}" % (index_name, local_key)
            p_name, p_data = read_propertdef(entry.get(dirname))
            properties[p_name] = p_data

    data.append(properties)

    return name, data

def resolve_refs(typedefs, classdefs):

    for name, data in root_class[3].items():
        classdefs['prop_ids'][data[0]] = name

    new_enums  = {}
    for name, data in typedefs['enums'].items():
        typedef_id = data[1]
        typedef_name = typedefs['all'][typedef_id]
        new_enums[name] = (data[0], typedef_id, data[2])
    typedefs['enums'] = new_enums

    new_records = {}
    for name, data in typedefs['records'].items():
        members = []
        for item in data[1]:
            typedef_id = item[1]
            typedef_name = typedefs['all'][typedef_id]
            members.append((item[0], typedef_id))

        new_records[name] = [data[0], members]

    typedefs['records'] = new_records

    new_fixed_arrays = {}
    for name, data in typedefs['fixed_arrays'].items():
        typedef_id = data[1]
        typedef_name = typedefs['all'][typedef_id]
        new_fixed_arrays[name] = (data[0], typedef_id, data[2])
    typedefs['fixed_arrays'] = new_fixed_arrays

    new_var_arrays = {}
    for name, data in typedefs['var_arrays'].items():
        typedef_id = data[1]
        typedef_name = typedefs['all'][typedef_id]
        new_var_arrays[name] = (data[0], typedef_id)
    typedefs['var_arrays'] = new_var_arrays

    new_renames = {}
    for name, data in typedefs['renames'].items():
        typedef_id = data[1]
        typedef_name = typedefs['all'][data[1]]
        new_renames[name] = (data[0], typedef_id)
    typedefs['renames'] = new_renames

    new_strings = {}
    for name, data in typedefs['strings'].items():
        typedef_id = data[1]
        typedef_name = typedefs['all'][typedef_id]
        new_strings[name] = (data[0], typedef_id)
    typedefs['strings'] = new_strings

    new_sets = {}
    for name, data in typedefs['sets'].items():
        typedef_id = data[1]
        typedef_name = typedefs['all'][data[1]]
        new_sets[name] = (data[0], typedef_id)
    typedefs['sets'] = new_sets

    new_strongrefs = {}
    for name, data in typedefs['strongrefs'].items():
        ref_id = data[1]
        ref_name = classdefs['ids'][data[1]]
        new_strongrefs[name] = (data[0], ref_id)
    typedefs['strongrefs'] = new_strongrefs

    new_weakrefs = {}
    for name, data in typedefs['weakrefs'].items():
        ref_id = data[1]
        ref_name = classdefs['ids'][ref_id]

        p_path = []
        for item in data[2]:
            p_name = classdefs['prop_ids'].get(item, item)
            # print((p_name, item), end=",")
            p_path.append(p_name)
        # print()
        new_weakrefs[name] = (data[0], ref_id, data[2])
        # print(name, p_path)

    typedefs['weakrefs'] = new_weakrefs

    new_classdefs = {}
    for name, data in classdefs['names'].items():
        parent_id = data[1]
        parent_name = classdefs['ids'][data[1]]

        if parent_name == name:
            parent_id = None
        propdefs = {}
        for p_name, p_data in data[3].items():
            typedef_id = p_data[2]
            typedef_name = typedefs['all'].get(typedef_id, typedef_id)

            if typedef_name == typedef_id:
                raise ValueError("cannot resolve typedef for %s.%s : " %(name, p_name, str(typedef_id) ))
            #     print(name, p_name, typedef_name)

            new_p_data = (p_data[0], p_data[1], typedef_id, p_data[3], p_data[4])
            propdefs[p_name] = new_p_data

        new_classdefs[name] = (data[0], parent_id, data[2], propdefs)

    classdefs['names'] = new_classdefs

def extract_extensions(typedefs, classdefs):
    from aaf2 import model

    typedef_ext = {}

    model_typedefs = {}
    for cat in typedef_cats:
        for name, data in model.typedefs.__dict__[cat].items():
            if isinstance(data, str):
                type_id = UUID(data)
            else:
                type_id = UUID(data[0])

            model_typedefs[type_id] = (name, data)

    for cat in typedef_cats:
        typedef_ext[cat] = {}
        for name, data in typedefs[cat].items():
            if data[0] in model_typedefs:
                new_extenum_members = {}
                new_enum_members = {}
                if cat == 'extenums':
                    model_data = model_typedefs[data[0]][1]
                    member_data = {}
                    for key, value in model_data[1].items():
                        member_data[UUID(key)] = value
                    for key, value in data[1].items():
                        if key in member_data:
                            continue
                        new_extenum_members[key] = value

                elif cat == 'enums':
                    model_data = model_typedefs[data[0]][1]
                    member_data = model_data[2]
                    for key, value in data[2].items():
                        if key in member_data:
                            continue
                        # raise ValueError("%s %s" % (name, value))
                        new_enum_members[key] = value

                if new_extenum_members:
                    data = [data[0], new_extenum_members]
                elif new_enum_members:
                    data = [data[0], data[1], new_enum_members]
                else:
                    continue

            typedef_ext[cat][name] = data
            # print(cat, name)

    property_defs = {}
    class_ids = {}
    for name, data in model.classdefs.classdefs.items():
        # print(name)
        class_ids[UUID(data[0])] = name
        for p_name, p_data in data[3].items():
            # print ("  ", p_name)
            property_defs[UUID(p_data[0])] = p_name

    classdef_ext = {}
    for name, data in classdefs['names'].items():
        if data[0] not in class_ids:
            classdef_ext[name] = data
            continue

        pdef_ext = {}
        for p_name, p_data in data[3].items():
            p_id = p_data[0]

            if p_id in property_defs:
                continue

            pdef_ext[p_name] = p_data

        if pdef_ext:
            classdef_ext[name] = (data[0], data[1], data[2], pdef_ext)
            # print(name)
            # for key, value in pdef_ext.items():
            #     print("  ", key)

    return typedef_ext, classdef_ext

def PAD(size, name):
    return max((size - len(name)), 0)

def write_typedefs(typedefs, path='typedefs.py'):

    # typedef_cats= ( "", "", "",
    #                "", "", "", "", "")
    with open(path, 'w') as f:

        f.write("ints = {\n")
        for name, data in typedefs['ints'].items():

            pad = PAD(15, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", {}, {}),\n'
            s = s.format(name, ':', data[0], data[1], data[2])
            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("enums = {\n")
        for name, data in typedefs['enums'].items():
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}",'
            s = s.format(name, ':', data[0], data[1])
            s += '{\n'
            for key, value in data[2].items():
                m = '   {:>4} : "{}",\n'.format(key, value)
                s += m
            s += '   }\n),\n'
            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("records = {\n")
        for name, data in typedefs['records'].items():
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", (\n'
            s = s.format(name, ':', data[0],)

            for item in data[1]:
                pad = PAD(20, item[0])
                m = '   ("{}"{:>' + str(pad) +  '}"{}"),\n'
                m = m.format(item[0], ',', item[1])
                s += m
            s += '   ),\n),\n'
            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("fixed_arrays = {\n")
        for name, data in sorted(typedefs['fixed_arrays'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}", {}),\n'
            s = s.format(name, ':', data[0], data[1], data[2])

            print(s, end="")
            f.write(s)

        f.write("}\n\n")

        f.write("var_arrays = {\n")
        for name, data in sorted(typedefs['var_arrays'].items()):
            pad = PAD(50, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}"),\n'
            s = s.format(name, ':', data[0], data[1],)

            print(s, end="")
            f.write(s)

        f.write("}\n\n")

        f.write("renames = {\n")

        for name, data in sorted(typedefs['renames'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}"),\n'
            s = s.format(name, ':', data[0], data[1],)

            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("strings = {\n")
        for name, data in sorted(typedefs['strings'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}"),\n'
            s = s.format(name, ':', data[0], data[1],)

            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("streams = {\n")

        for name, data in sorted(typedefs['streams'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} "{}",\n'
            s = s.format(name, ':', data[0])

            print(s, end="")
            f.write(s)

        f.write("}\n\n")

        f.write("opaques = {\n")
        for name, data in sorted(typedefs['opaques'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} "{}",\n'
            s = s.format(name, ':', data[0])
            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("extenums = {\n")
        for name, data in sorted(typedefs['extenums'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", '
            s = s.format(name, ':', data[0],)
            s += '{\n'

            for key, value in sorted(data[1].items()):
                m = '   "{}"{}"{}",\n'
                m = m.format(key, ' : ', value)
                s += m
            s += '   },\n),\n'
            print(s, end="")
            f.write(s)


        f.write("}\n\n")

        f.write("chars = {\n")
        for name, data in sorted(typedefs['chars'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} "{}",\n'
            s = s.format(name, ':', data[0])
            print(s, end="")
            f.write(s)

        f.write("}\n\n")

        f.write("generic_chars = {\n")
        for name, data in sorted(typedefs['generic_chars'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} "{}",\n'
            s = s.format(name, ':', data[0])
            print(s, end="")
            f.write(s)

        f.write("}\n\n")

        f.write("indirects = {\n")
        for name, data in sorted(typedefs['indirects'].items()):
            pad = PAD(20, name)
            s = '"{}" {:>' + str(pad) + '} "{}",\n'
            s = s.format(name, ':', data[0])
            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("sets = {\n")
        for name, data in sorted(typedefs['sets'].items()):
            pad = PAD(50, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}"),\n'
            s = s.format(name, ':', data[0], data[1],)

            print(s, end="")
            f.write(s)
        f.write("}\n\n")

        f.write("strongrefs = {\n")
        for name, data in sorted(typedefs['strongrefs'].items()):
            pad = PAD(50, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}"),\n'
            s = s.format(name, ':', data[0], data[1],)

            print(s, end="")
            f.write(s)

        f.write("}\n\n")

        f.write("weakrefs = {\n")
        for name, data in sorted(typedefs['weakrefs'].items()):
            pad = PAD(50, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}",\n'
            s = s.format(name, ':', data[0], data[1],)

            m = ', '.join(['"{}"'.format(item) for item in data[2] ])

            s += "    ({})),\n".format(m)
            print(s, end="")
            f.write(s)

        f.write("}\n")

def write_classdefs(classdefs, path='classdefs.py'):

    aliases = {}
    with open(path, 'w') as f:
        f.write("classdefs = {\n")
        for name, data in classdefs.items():
            if name.count(" "):
                aliases[name.replace(" ", '_')] = name
            pad = PAD(40, name)
            s = '"{}" {:>' + str(pad) + '} ("{}", "{}", {}, '
            s = s.format(name, ':', data[0], data[1], data[2])
            s += "{\n"

             # "04020301-0b00-0000-060e-2b3401010108" ,  0x3D2E ,  "aafUInt32" , True ,  False )
            for p_name, p_data in sorted(data[3].items()):
                pad = PAD(40, p_name)
                pid = p_data[1]
                if pid >= 0x8000:
                    pid = None
                else:
                    pid = '0x{:04X}' % pid

                m = '    "{}"{:>' + str(pad) +  '}'
                m +=  ' ("{}", {}, "{}", {}, {}),\n'
                m = m.format(p_name, ':', p_data[0], pid, p_data[2], p_data[3], p_data[4])
                s+=m

            s += "    }\n),\n"

            print(s, end="")
            f.write(s)

        f.write("}\n\n")


        f.write("aliases = {\n")
        for name, value in aliases.items():
            pad = PAD(40, name)
            s = '"{}" {:>' + str(pad) + '} "{}",\n'
            s = s.format(name, ':', value)
            f.write(s)

        f.write("}\n")

def dump_model(path):

    with open(path, 'rb') as f:
        c = cfb.CompoundFileBinary(f, 'rb')

        weakref_table = read_reference_properties(c)
        for i, path in enumerate(weakref_table):
            print(i, ':', end="")
            for item in path:
                print(" 0x%04X, " % item, end="")
            print()

        metadict = None
        for item in c.listdir("/"):
            if item.class_id == MetaDictionary:
                metadict = item
                break
        if not metadict:
            raise Exception("can not find metadict")

        properties = read_properties(metadict)

        index_name = decode_utf16le(properties[CLASSDEFINITIONS_PID])
        class_reference_keys = read_set_index(metadict.get(index_name + " index"))

        index_name = decode_utf16le(properties[TYPEDEFINITIONS_PID])
        type_reference_keys = read_set_index(metadict.get(index_name + " index"))


        #TypeDefinitions
        index_name = mangle_name("TypeDefinitions", TYPEDEFINITIONS_PID, 32-10)

        typedefs = {}
        for key in typedef_cats:
            typedefs[key] = {}

        typedefs['all'] = {}

        for key, local_key in type_reference_keys:
            dirname = "%s{%x}" % (index_name, local_key)
            read_typedef(metadict.get(dirname), typedefs)

        #
        #ClassDefinitions
        index_name = mangle_name("ClassDefinitions", CLASSDEFINITIONS_PID, 32-10)

        classdefs = {'names': {}, 'ids':{}, 'prop_ids': {}}
        for key, local_key in class_reference_keys:
            dirname = "%s{%x}" % (index_name, local_key)
            class_name, class_data = read_classdef(metadict.get(dirname))
            classdefs['names'][class_name] = class_data
            classdefs['ids'][class_data[0]] = class_name

            for p_name, p_data in class_data[3].items():
                classdefs['prop_ids'][p_data[0]] = p_name

        resolve_refs(typedefs, classdefs)
        # for cat in typedef_cats:
        # #     print(cat, "= ")
        # #     pprint.pprint(typedefs[cat])

        # pprint.pprint(classdefs['names'])

        typedef_ext, classdef_ext = extract_extensions(typedefs, classdefs)

        write_typedefs(typedef_ext)

        write_classdefs(classdef_ext)

        # for cat in typedef_cats:
        #     print(cat, "= ")
        #     pprint.pprint(typedef_ext[cat])

        # pprint.pprint(classdef_ext)


if __name__ == "__main__":
    import sys
    dump_model(sys.argv[1])
