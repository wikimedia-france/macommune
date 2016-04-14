#include "args.h"

#include <stdlib.h>
#include <stdio.h>
#include <getopt.h>
#include <string.h>

#include "global.h"

Args *args_new() {
	Args *this = malloc(sizeof(Args));
	args_init(this);
	return this;
}

void args_free(Args *this) {
	args_clear(this);
	free(this);
}

void args_init(Args *this) {
	this->conf = NULL;
	this->listen_host = strdup("0.0.0.0");
	this->listen_port = 8080;
	this->embeded_index = false;
	this->mysql_host = NULL;
	this->mysql_user = NULL;
	this->mysql_passwd = NULL;
	this->mysql_db = NULL;
	this->charset = strdup("utf8");
	this->output_mode = OUTPUT_MODE_DEFAULT;
}

void args_clear(Args *this) {
	if (this->conf) free(this->conf);
	if (this->listen_host) free(this->listen_host);
	if (this->mysql_host) free(this->mysql_host);
	if (this->mysql_user) free(this->mysql_user);
	if (this->mysql_db) free(this->mysql_db);
	if (this->charset) free(this->charset);
	args_init(this);
}

#define GET_ARG(var, fct) \
	this->var = fct(optarg);

#define GET_ARG_STR(var) \
	if (this->var) free(this->var); \
	GET_ARG(var, strdup)

#define GET_ARG_INT(var) \
	GET_ARG(var, atoi)

#define GET_ARG_BOOL(var) \
	this->var = true;

void args_help() {
	printf("Usage:\n");
	printf("  " PACKAGE " [OPTION...] target1 query1 target2 query2... \n\n");
	printf(PACKAGE " Options:\n");
	printf("  -c, --conf             Set path of configuration file\n");
	printf("  -h, --listen-host      Set listening host (default is 0.0.0.0)\n");
	printf("  -p, --listen-port      Set listening port (default is 8080)\n");
	printf("  -i, --embeded-index    Embed or not test page \"index.html\"\n");
	printf("  -H, --mysql-host       Set Mysql host\n");
	printf("  -U, --mysql-user       Set Mysql user\n");
	printf("  -P, --mysql-passwd     Set Mysql password\n");
	printf("  -D, --mysql-db         Set Mysql database\n");
	printf("  -C, --charset          Set default charset\n");
	printf("  -m, --output-mode      Set default output-mode (xml/php/json/text)\n");
	printf("  -?, --help             Show help options and exit\n");
	printf("  -v, --version          Show the version number and exit\n");
}

void args_version() {
	printf(PACKAGE " " VERSION "\n");
}

void args_parse(Args *this, int argc, char *argv[]) {
	struct option long_options[] = {
		{ "conf", 1, NULL, 'c' },
		{ "listen-host", 1, NULL, 'h' },
		{ "listen-port", 1, NULL, 'p' },
		{ "embeded-index", 0, NULL, 'i' },
		{ "mysql-host", 1, NULL, 'H' },
		{ "mysql-user", 1, NULL, 'U' },
		{ "mysql-passwd", 1, NULL, 'P' },
		{ "mysql-db", 1, NULL, 'D' },
		{ "charset", 1, NULL, 'C' },
		{ "output-mode", 1, NULL, 'm' },
		{ "help", 0, NULL, '?' },
		{ "version", 0, NULL, 'v' },
		{ NULL, 0, NULL, 0 }
	};

	int option_index, c;
	while ((c = getopt_long(argc, argv, "c:h:p:iH:U:P:D:C:m:?v", long_options, &option_index)) != -1) {
		switch (c) {
			case 'c': 
				GET_ARG_STR(conf);
				break;
			case 'h':
				GET_ARG_STR(listen_host);
				break;
			case 'p':
				GET_ARG_INT(listen_port);
				break;
			case 'i':
				GET_ARG_BOOL(embeded_index);
				break;
			case 'H':
				GET_ARG_STR(mysql_host);
				break;
			case 'U':
				GET_ARG_STR(mysql_user);
				break;
			case 'P':
				GET_ARG_STR(mysql_passwd);
				break;
			case 'D':
				GET_ARG_STR(mysql_db);
				break;
			case 'C':
				GET_ARG_STR(charset);
				break;
			case 'm':
				GET_ARG(output_mode, global_output_mode);
				break;
			case '?':
				args_help();
				exit(0);
				break;
			case 'v':
				args_version();
				exit(0);
				break;
		}
        }
}

