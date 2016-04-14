#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <getopt.h>

#include "global.h"
#include "args.h"
#include "db_mysql.h"
#include "http.h"
#include "conf_parser.h"

#define CONF_PARSER_GET_PARAM(parser, name, var, fct) { \
	char *value = conf_parser_param(parser, name); \
	if (value) var = fct(value); \
}

#define CONF_PARSER_GET_PARAM_STR(parser, name, var) { \
	char *value = conf_parser_param(parser, name); \
	if (value) { \
		if (var) free(var); \
		var = strdup(value); \
	} \
}

#define CONF_PARSER_GET_PARAM_INT(parser, name, var) \
	CONF_PARSER_GET_PARAM(parser, name, var, atoi)

#define CONF_PARSER_GET_PARAM_BOOL(parser, name, var) { \
	char *value = conf_parser_param(parser, name); \
	if (value) var = (strcmp(value, "1") == 0); \
}

void conf_parse(Args *args, char *filename) {
	ConfParser *parser = conf_parser_new();
	conf_parser_read(parser, filename);
	CONF_PARSER_GET_PARAM_BOOL(parser, "embeded-index", args->embeded_index);
	CONF_PARSER_GET_PARAM_STR(parser, "listen-host", args->listen_host);
	CONF_PARSER_GET_PARAM_INT(parser, "listen-port", args->listen_port);
	CONF_PARSER_GET_PARAM_STR(parser, "charset", args->charset);
	CONF_PARSER_GET_PARAM(parser, "output-mode", args->output_mode, global_output_mode);

	conf_parser_free(parser);
}

int main(int argc, char *argv[]) {
	Args *args = args_new();
	args_parse(args, argc, argv);

	global_init(args->charset, args->output_mode);

	//Init data from command line
	if (args->mysql_host && args->mysql_user && args->mysql_passwd && args->mysql_db) {
		if (!db_mysql_load_queries(args->mysql_host, args->mysql_user, args->mysql_passwd, args->mysql_db, argc - optind, &argv[optind])) {
			return 1;
		}
	}

	//Init data from configuration file
        if (args->conf) {
		conf_parse(args, args->conf);
	}

	//Start server
	Http *http = http_new(args->embeded_index);
	http_start(http, args->listen_host, args->listen_port);
	http_free(http);

	global_free();
	args_free(args);
	return 0;
}
