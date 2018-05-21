#include "common.h"

using namespace std;

string parse_parent(string name)
{
    if (name == "Root") {
        return "None";
    }
    return "\"" + name + "\"";
}

int main()
{
    std::string indent("    ");

#include "typedefs_names.h"
#include "AAFMetaDictionary.h"

#include "classdefs_names.h"
#include "AAFMetaDictionary.h"

#define AAF_LITERAL_AUID(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8) \
auid_to_str(l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8)

#define AAF_TABLE_BEGIN() \
    cout << "classdefs = {" << endl;

#define AAF_CLASS(name, id, parent, concrete) \
    cout <<  QUOTE(name) <<  PAD(25, #name)<< " : ("; \
    cout << id <<  ", " ; \
    cout << CLASS_ID_##parent << ", " << python_bool(concrete)  <<", {"<< endl;

#define AAF_PROPERTY(name, id, tag, type, mandatory, uid, container) \
    cout << indent << QUOTE(name) <<  PAD(25, #name) ; \
    cout << ": (" << id << ", " <<  #tag <<", "; \
    cout << type << ", " << python_bool(!mandatory) << ", " << python_bool(uid) <<")," << endl;

#define AAF_CLASS_SEPARATOR() \
    cout << "    }"<< endl << ")," << endl;

#define AAF_TABLE_END() \
    cout << "    }"<< endl << ")}" << endl << endl;

#define AAF_TYPE(name) ID_##name
#define AAF_REFERENCE_TYPE(type, target) ID_##target##type

#include "AAFMetaDictionary.h"

#define AAF_ALIAS_TABLE_BEGIN()
    cout << "aliases = {" << endl;

#define AAF_CLASS_ALIAS(name, alias) \
    cout << QUOTE(alias) << PAD(25, #alias) << " : "  << QUOTE(name) << "," <<endl;

#define AAF_ALIAS_TABLE_END() \
    cout << "}" << endl;

#include "AAFMetaDictionary.h"
}