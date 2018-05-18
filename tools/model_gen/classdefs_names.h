#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

string CLASS_ID_Root= "None";

#define AAF_CLASS(name, id, parent, concrete) \
string CLASS_ID_##name = id;
