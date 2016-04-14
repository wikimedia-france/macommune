#ifndef _JSON_H
#define _JSON_H

#include <string.h>

const char *json_escape_char(char c);
char *json_escape(const char *str);

#endif
