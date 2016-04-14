#include "db_mysql.h"

#include <stdio.h>
#include <string.h>

#include "global.h"
#include "stringlist.h"
#include "log.h"

bool db_mysql_open(MYSQL *mysql, char *host, char *user, char *passwd, char *db) {
	mysql_init(mysql);
	mysql_options(mysql, MYSQL_READ_DEFAULT_GROUP, PACKAGE);

	if (!mysql_real_connect(mysql, host, user, passwd, db, 0, NULL, 0)) {
		log_msg_printf(LOG_ERR, true, "Could not connect to database. Error: %s", mysql_error(mysql));
		return false;
	}

	if (mysql_set_character_set(mysql, global.charset) != 0) {
		log_msg_printf(LOG_ERR, true, "Could not set charset name: %s", global.charset);
	}

	return true;
}

int db_mysql_load_tree(MYSQL *mysql, Tree *tree, char *query) {
	printf("%s...", query);
	fflush(stdout);

	int res = mysql_query(mysql, query);
	if (res != 0) {
		log_msg_printf(LOG_ERR, true, "Could not execute query. Error: %s", mysql_error(mysql));
		return -1;
	}
	
	MYSQL_RES *result = mysql_use_result(mysql);
	int rows = mysql_num_fields(result);
	if (rows < 1) {
		mysql_free_result(result);
		log_msg_printf(LOG_ERR, true, "Must return at least 1 fields!");
		return -1;
	}

	MYSQL_ROW row;
	unsigned int count = 0;
	while ((row = mysql_fetch_row(result))) {
		char *str = row[0];
		int value = (rows >= 2) ? atoi(row[1]) : 0;
		char *str_real = (rows >= 3) ? row[2] : NULL;
		tree_add(tree, str, str_real, value);
		count++;
	}
	mysql_free_result(result);
	printf("=> %i\n", count);
	return count;
}

void db_mysql_load_query(MYSQL *mysql, char *name, char *query) {
	Tree *tree = global_tree_find_or_create(name);
	if (name) printf("[%s] ", name);
	db_mysql_load_tree(mysql, tree, query);
}

bool db_mysql_load_queries(char *host, char *user, char *passwd, char *db, int queries_count, char *queries[]) {
	MYSQL mysql;
	if (!db_mysql_open(&mysql, host, user, passwd, db)) {
		log_msg_printf(LOG_ERR, true, "Could not connect to mysql db");
		return false;
	}

	int i;
	for (i = 1; i < queries_count; i += 2) {
		db_mysql_load_query(&mysql, queries[i - 1], queries[i]);
	}

	mysql_close(&mysql);
	return true;
}

