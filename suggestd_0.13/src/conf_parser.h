#ifndef _CONF_PARSER_H
#define _CONF_PARSER_H

#include <expat.h>
#include <stdbool.h>

#include "db_mysql.h"
#include "db_sqlite3.h"

typedef struct {
	XML_Parser handle;
	MYSQL mysql_handle;
	sqlite3 *sqlite3_handle;
	bool connected;
	enum {context_none, context_sqlite3, context_mysql} context;
	StringList *params;
} ConfParser;


ConfParser *conf_parser_new();
void conf_parser_free(ConfParser *this);
void conf_parser_debug(ConfParser *parser);
bool conf_parser_read(ConfParser *this, char const *path);
char *conf_parser_param(ConfParser *this, char *name);

#endif
