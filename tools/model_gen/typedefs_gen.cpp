#include "common.h"

using namespace std;


int main()
{
    std::string indent("    ");


#include "typedefs_names.h"
#include "AAFMetaDictionary.h"

#include "classdefs_names.h"
#include "AAFMetaDictionary.h"

#include "propertydef_names.h"
#include "AAFMetaDictionary.h"

// TypeDefInt            = UUID("0d010101-0204-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define MY_TYPE_NAME(name) QUOTE(aaf##name)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "ints = {" << endl;

#define AAF_TYPE_DEFINITION_INTEGER(name, id, size, signed) \
    cout << MY_TYPE_NAME(name) << PAD(16, MY_TYPE_NAME(name)) << " : (" ; \
    cout << id << ", ";                     \
    cout << size << ", ";                   \
    cout << #signed << ", ";                \
    cout <<  ")," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefEnum           = UUID("0d010101-0207-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE(name) ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "enums = {" << endl;

#define AAF_TYPE_DEFINITION_ENUMERATION(name, id, type) \
    cout << QUOTE(name) << PAD(30, QUOTE(name)) << ": ("; \
    cout << id << ", "; \
    cout << type << ", {"; \
    cout << endl;

#define AAF_TYPE_DEFINITION_ENUMERATION_MEMBER(name, value, container) \
    cout <<  "   " << #value << PAD(5, #value) <<  ": " << QUOTE(name) << "," << endl;

#define AAF_TYPE_DEFINITION_ENUMERATION_END(name, id, type) \
    cout << "   " << "}" << endl; \
    cout << ")," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefRecord         = UUID("0d010101-020d-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE(name) ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "records = {" << endl;

#define AAF_TYPE_DEFINITION_RECORD(name, id) \
    cout << QUOTE(name) << PAD(10, #name) <<  ": ("; \
    cout << id << ", (" << endl;

#define AAF_TYPE_DEFINITION_RECORD_FIELD(name, type, parent) \
    cout << indent  << "("<< QUOTE(name) << PAD(20, #name); \
    cout << ", " << type << ")," << endl;

#define AAF_TYPE_DEFINITION_RECORD_END(name, id) \
    cout << indent << ")" << endl; \
    cout << ")," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefFixedArray     = UUID("0d010101-0208-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE(name) ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "fixed_arrays = {" << endl;

#define AAF_TYPE_DEFINITION_FIXED_ARRAY(name, id, type, count) \
    cout << QUOTE(aaf##name) << PAD(18, QUOTE(name)) << ": ("; \
    cout <<  id << ", " << type << ", " << count << "),"; \
    cout << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefVariableArray  = UUID("0d010101-0209-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE(name) ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "var_arrays = {" << endl;

#define AAF_TYPE_DEFINITION_VARYING_ARRAY(name, id, type) \
    cout << QUOTE(aaf##name) << PAD(30, QUOTE(name)) << ": ("; \
    cout <<  id << ", " << type << "),"; \
    cout << endl;

#include "AAFMetaDictionary.h"

// StrongRefVector

#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(kAAFTypeID_##target##type)
#define AAF_TYPE(name) ID_##name##StrongReference

#define AAF_TYPE_DEFINITION_STRONG_REFERENCE_VECTOR(name, id, type) \
    cout << name << PAD(60, name) << " : ("; \
    cout << id << ", "; \
    cout << type; \
    cout << " )," <<endl;

#include "AAFMetaDictionary.h"

// WeakRefVector

#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(kAAFTypeID_##target##type)
#define AAF_TYPE(name) ID_##name##WeakReference

#define AAF_TYPE_DEFINITION_WEAK_REFERENCE_VECTOR(name, id, type) \
    cout << name << PAD(55, name) << " : ("; \
    cout << id << ", "; \
    cout << type; \
    cout << " )," <<endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefRename         = UUID("0d010101-020e-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE(name) ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "renames = {" << endl;

#define AAF_TYPE_DEFINITION_RENAME(name, id, type) \
    cout << QUOTE(aaf##name) << PAD(20, #name) <<  ": ("; \
    cout << id << ", " << AAF_TYPE(type) <<")," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefString         = UUID("0d010101-020b-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "strings = {" << endl;

#define AAF_TYPE_DEFINITION_STRING(name, id, type) \
    cout << QUOTE(aaf##name) << PAD(20, #name) <<  ": ("; \
    cout  << id << ", " << ID_##type <<")," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefStream         = UUID("0d010101-020c-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "streams = {" << endl;

#define AAF_TYPE_DEFINITION_STREAM(name, id) \
    cout << QUOTE(name) << " : " << id <<  ','<< endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefOpaque         = UUID("0d010101-0222-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "opaques = {" << endl;

#define AAF_TYPE_DEFINITION_OPAQUE(name, id) \
    std::cout << QUOTE(aaf##name) << " : " << id << "," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefExtendibleEnum = UUID("0d010101-0220-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "extenums = {" << endl;

#define AAF_TYPE_DEFINITION_EXTENDIBLE_ENUMERATION(name, id) \
    cout << NAME_##name << PAD(20, #name) <<  ": (" << id << ", {" << endl;

#define AAF_TYPE_DEFINITION_EXTENDIBLE_ENUMERATION_MEMBER(name, auid, container) \
    cout << indent << auid <<  " : " << QUOTE(name) << "," << endl;

#define AAF_TYPE_DEFINITION_EXTENDIBLE_ENUMERATION_END(name, id) \
    cout << indent << "}" << endl; \
    cout << ")," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

/* this is pretty broken in the new header ugh */
// TypeDefCharacter      = UUID("0d010101-0223-0000-060e-2b3402060101")
// #define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
// auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

// #define AAF_TYPE_TABLE_BEGIN() \
//     cout << "chars = {" << endl;

// #define AAF_TYPE_DEFINITION_CHARACTER(name, id) \
//     std::cout << QUOTE(aaf##name) << " : " << id << "," << endl;

// #define AAF_TYPE_TABLE_END() \
//     cout << "}" << endl << endl;

// #include "AAFMetaDictionary.h"

cout << "chars = {" << endl;
cout << "\"aafCharacter\" : \"01100100-0000-0000-060e-2b3401040101\"," << endl;

cout << "}" << endl << endl;


cout << "generic_chars = {" << endl;
cout << "\"aafChar\" : (\"01100300-0000-0000-060e-2b3401040101\", 1),"   << endl;
cout << "}" << endl << endl;

// TypeDefIndirect       = UUID("0d010101-0221-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "indirects = {" << endl;

#define AAF_TYPE_DEFINITION_INDIRECT(name, id) \
    std::cout << QUOTE(aaf##name) << " : " << id << "," << endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefSet            = UUID("0d010101-020a-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TYPE(name) ID_##name

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(kAAFTypeID_##target##type)

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "sets = {" << endl;

#define AAF_TYPE_DEFINITION_SET(name, id, type) \
    cout << NAME_##name << ": ("; \
    cout <<  id << ", " << type << "),"; \
    cout << endl;

#include "AAFMetaDictionary.h"

// StrongRefSet

#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(kAAFTypeID_##target##type)
#define AAF_TYPE(name) ID_##name##StrongReference

#define AAF_TYPE_DEFINITION_STRONG_REFERENCE_SET(name, id, type) \
    cout << name << PAD(60, name) << " : ("; \
    cout << id << ", "; \
    cout << type; \
    cout << " )," <<endl;

#include "AAFMetaDictionary.h"

// WeakRefSet

#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(kAAFTypeID_##target##type)
#define AAF_TYPE(name) ID_##name##WeakReference

#define AAF_TYPE_DEFINITION_WEAK_REFERENCE_SET(name, id, type) \
    cout << name << PAD(55, name) << " : ("; \
    cout << id << ", "; \
    cout << type; \
    cout << " )," <<endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefStrongRef      = UUID("0d010101-0205-0000-060e-2b3402060101")

#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(kAAFTypeID_##target##type)
#define AAF_TYPE(name) CLASS_ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "strongrefs = {" << endl;

#define AAF_TYPE_DEFINITION_STRONG_REFERENCE(name, id, type) \
    cout << name << PAD(55, name) << " : ("; \
    cout << id << ", "; \
    cout << type; \
    cout << " )," <<endl;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

// TypeDefWeakRef        = UUID("0d010101-0206-0000-060e-2b3402060101")
#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_REFERENCE_TYPE_NAME(type, target) QUOTE(target##type)
#define AAF_TYPE(name) CLASS_ID_##name

#define AAF_TYPE_TABLE_BEGIN() \
    cout << "weakrefs = {" << endl;

#define AAF_TYPE_DEFINITION_WEAK_REFERENCE(name, id, type) \
    cout << name << PAD(45, name) << ": ("; \
    cout << id << ", "; \
    cout << type << ","; \
    cout << endl << "   (";

#define AAF_TYPE_DEFINITION_WEAK_REFERENCE_MEMBER(name, parent, container) \
    cout << PROP_ID_##parent##name << ", ";

#define AAF_TYPE_DEFINITION_WEAK_REFERENCE_END(name, id, type) \
    cout << ")"<< endl << ")," << endl;;

#define AAF_TYPE_TABLE_END() \
    cout << "}" << endl << endl;

#include "AAFMetaDictionary.h"

}
