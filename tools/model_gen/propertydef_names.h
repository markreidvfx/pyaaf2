#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

// string CLASS_ID_Root= "None";

string PROP_ID_RootMetaDictionary = "\"0d010301-0101-0100-060e-2b3401010102\"";
string PROP_ID_RootHeader         = "\"0d010301-0102-0100-060e-2b3401010102\"";

#define AAF_PROPERTY(name, id, tag, type, mandatory, uid, container) \
string PROP_ID_##container##name = id;
