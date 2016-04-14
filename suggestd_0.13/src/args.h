#ifndef _ARGS_H
#define _ARGS_H

#include <stdbool.h>

typedef struct {
	char *conf;
	char *listen_host;
	int listen_port;
	bool embeded_index;
	char *mysql_host;
	char *mysql_user;
	char *mysql_passwd;
	char *mysql_db;
	char *charset;
	int output_mode;
} Args;

Args *args_new();
void args_free(Args *this);
void args_init(Args *this);
void args_clear(Args *args);
void args_parse(Args *this, int argc, char *argv[]);

#endif
