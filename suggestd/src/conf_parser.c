#include "conf_parser.h"

#include <stdio.h>
#include <string.h>

#include "log.h"

#define BUFFER_SIZE 4096

XML_Char *conf_parser_get_attr(XML_Char const **attr, XML_Char const *name) {
	int i;
	for (i = 0; attr[i]; i += 2) {
		if (strcmp(attr[i], name) == 0)
			return (XML_Char *) attr[i + 1];
	}
	return NULL;
}

void conf_parser_element_start(void *data, XML_Char const *name, XML_Char const **attr) {
	ConfParser *this = (ConfParser *) data;
	//<mysql>
	if (strcmp(name, "mysql") == 0 && this->context == context_none) {
		this->context = context_mysql;
		char *host = conf_parser_get_attr(attr, "host");
		char *user = conf_parser_get_attr(attr, "user");
		char *passwd = conf_parser_get_attr(attr, "passwd");
		char *db = conf_parser_get_attr(attr, "db");
		if (host && user && passwd && db) {
			this->connected = db_mysql_open(&this->mysql_handle, host, user, passwd, db);
			if (!this->connected)
				log_msg_printf(LOG_ERR, true, "Could not connect to mysql db (host: %s, user: %s, passwd: %s, db: %s)", host, user, passwd, db);
		}
		else {
			log_msg_printf(LOG_ERR, true, "Mysql attributes are mendatory (host: %s, user: %s, passwd: %s, db: %s)", host, user, passwd, db);
		}
	}

	//<sqlite3>
	else if (strcmp(name, "sqlite3") == 0 && this->context == context_none) {
		this->context = context_sqlite3;
		char *path = conf_parser_get_attr(attr, "path");
		if (path) {
			this->connected = db_sqlite3_open(&this->sqlite3_handle, path);
			if (!this->connected)
				log_msg_printf(LOG_ERR, true, "Could not connect to sqlite3 db (path: %s)", path);
		}
		else {
			log_msg_printf(LOG_ERR, true, "Sqlite3 attributes \"path\" is mendatory");
		}
	}

	//<query />
	else if (strcmp(name, "query") == 0 && this->context != context_none && this->connected) {
		char *target = conf_parser_get_attr(attr, "target");
		char *str = conf_parser_get_attr(attr, "str");
		if (str) {
			if (this->context == context_mysql)
				db_mysql_load_query(&this->mysql_handle, target, str);
			else if (this->context == context_sqlite3)
				db_sqlite3_load_query(this->sqlite3_handle, target, str);
		}
		else {
			log_msg_printf(LOG_ERR, true, "Query string is mendatory", target, str);
		}
	}

	//<param />
	else if (strcmp(name, "param") == 0) {
		char *name = conf_parser_get_attr(attr, "name");
		char *value = conf_parser_get_attr(attr, "value");
		if (name && value) {
			StringListItem *item = stringlistitem_new(name, strdup(value));
			stringlist_push_back(this->params, item);
		}
		else {
			log_msg_printf(LOG_ERR, true, "Attributes 'name' and 'value' are mendatory (name: %s, value: %s)", name, value);
		}
	}
}

void conf_parser_element_end(void *data, XML_Char const *name) {
	ConfParser *this = (ConfParser *) data;

	//</mysql>
	if (this->context == context_mysql && strcmp(name, "mysql") == 0) {
		this->context = context_none;
		if (this->connected) {
			mysql_close(&this->mysql_handle);
			this->connected = false;
		}
	}

	//</sqlite3>
	else if (this->context == context_sqlite3 && strcmp(name, "sqlite3") == 0) {
		this->context = context_none;
		if (this->connected) {
			sqlite3_close(this->sqlite3_handle);
			this->connected = false;
		}
	}
}

void conf_parser_error_print(ConfParser *this) {
	int code = XML_GetErrorCode(this->handle);
	log_msg_printf(LOG_ERR, true, "Expat error (%i): %s\n", code, XML_ErrorString(code));
}

void conf_parser_init(ConfParser *this) {
	this->connected = false;
	this->handle = XML_ParserCreate("utf-8");
	XML_SetUserData(this->handle, this);
	XML_SetElementHandler(this->handle, conf_parser_element_start, conf_parser_element_end);
	this->params = stringlist_new();
}

void conf_parser_clear(ConfParser *this) {
	this->connected = false;
	XML_ParserFree(this->handle);
	stringlist_free(this->params, true);
}

ConfParser *conf_parser_new() {
	ConfParser *this = malloc(sizeof(ConfParser));
	conf_parser_init(this);
	return this;
}

void conf_parser_free(ConfParser *this) {
	conf_parser_clear(this);
	free(this);
}

char *conf_parser_param(ConfParser *this, char *name) {
	StringListItem *item = stringlist_find(this->params, name);
	return (item) ? item->data : NULL;
}

void conf_parser_debug(ConfParser *this) {
	StringListItem *it;
	for (it = this->params->first; it != NULL; it = it->next) {
		printf("PARAM %s %s\n", it->str, (char *) it->data);
	}
}

bool conf_parser_read(ConfParser *this, char const *path) {
	FILE *f = fopen(path, "rb");
	if (f == NULL) {
		log_msg_printf(LOG_ERR, true, "Could not read input file");
		return false;
	}

	void *buffer = malloc(BUFFER_SIZE);
	for (;;) {
		size_t readen = fread(buffer, 1, BUFFER_SIZE, f);
		int last = readen != BUFFER_SIZE ? 1 : 0;

		if (XML_Parse(this->handle, buffer, readen, last) == 0) {
			conf_parser_error_print(this);

			free(buffer);
			fclose(f);
			return false;
		}
		if (last)
			break;
	}

	fclose(f);
	free(buffer);
	return true;
}

