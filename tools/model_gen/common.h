#include <iostream>
#include <iomanip>
#include <string.h>
#include <stdio.h>
#include <vector>
#include <map>


#define QUOTE(name) "\"" #name "\""

#define PAD(size, name) setw(size - string(name).length())

std::string auid_to_str(int l, int w1, int w2, int b1, int b2, int b3, int b4, int b5, int b6, int b7, int b8 )
{
  char buf[1024];
  snprintf(buf, 1024, "\"%08x-%04x-%04x-%02x%02x-%02x%02x%02x%02x%02x%02x\"", l, w1, w2,  b1, b2, b3, b4, b5, b6, b7, b8);
  return  std::string(buf);
}

std::string python_bool(bool value)
{
  if (value)
    return "True";
  return "False";
}
