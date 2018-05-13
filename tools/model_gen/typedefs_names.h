#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define MY_AAF_TYPE(name, id, type_name) \
    string ID_##name = id; \
    string NAME_##name = "\""  #type_name "\"" ;
    // std::cerr << #name << "=" << NAME_##name << '\n';

#define MY_AAF_TYPE2(name, id) \
    string ID_##name = id; \
    string NAME_##name = "\""  "kAAFTypeID_" #name "\"";
    // std::cerr << #name << "=" << NAME_##name << '\n';


#define AAF_TYPE_DEFINITION_INTEGER(name, id, size, signed) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_ENUMERATION(name, id, type) \
   MY_AAF_TYPE(name, id, name)
#define AAF_TYPE_DEFINITION_FIXED_ARRAY(name, id, type, count) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_VARYING_ARRAY(name, id, type) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_RECORD(name, id) \
   MY_AAF_TYPE(name, id, name)
#define AAF_TYPE_DEFINITION_RENAME(name, id, type) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_STRING(name, id, type) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_EXTENDIBLE_ENUMERATION(name, id) \
   MY_AAF_TYPE(name, id, name)
#define AAF_TYPE_DEFINITION_CHARACTER(name, id) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_SET(name, id, type) \
   MY_AAF_TYPE(name, id, name)
#define AAF_TYPE_DEFINITION_STRONG_REFERENCE(name, id, type) \
   MY_AAF_TYPE2(name, id)
#define AAF_TYPE_DEFINITION_STRONG_REFERENCE_SET(name, id, type) \
   MY_AAF_TYPE2(name, id)
#define AAF_TYPE_DEFINITION_STRONG_REFERENCE_VECTOR(name, id, type) \
   MY_AAF_TYPE2(name, id)
#define AAF_TYPE_DEFINITION_WEAK_REFERENCE(name, id, type) \
   MY_AAF_TYPE(name, id, name)
#define AAF_TYPE_DEFINITION_WEAK_REFERENCE_SET(name, id, type) \
   MY_AAF_TYPE2(name, id)
#define AAF_TYPE_DEFINITION_WEAK_REFERENCE_VECTOR(name, id, type) \
   MY_AAF_TYPE2(name, id)
#define AAF_TYPE_DEFINITION_STREAM(name, id) \
   MY_AAF_TYPE(name, id, name)
#define AAF_TYPE_DEFINITION_INDIRECT(name, id) \
   MY_AAF_TYPE(name, id, aaf##name)
#define AAF_TYPE_DEFINITION_OPAQUE(name, id) \
   MY_AAF_TYPE(name, id, aaf##name)

#define AAF_TYPE(name) name
#define AAF_REFERENCE_TYPE_NAME(type, target) target##type
