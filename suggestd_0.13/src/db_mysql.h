#ifndef _DB_MYSQL_H
#define _DB_MYSQL_H

#include <stdbool.h>
#include <mysql.h>

#include "tree.h"

bool db_mysql_open(MYSQL *mysql, char *host, char *user, char *passwd, char *db);
int db_mysql_load_tree(MYSQL *mysql, Tree *tree, char *query);
void db_mysql_load_query(MYSQL *mysql, char *name, char *query);
bool db_mysql_load_queries(char *host, char *user, char *passwd, char *db, int queries_count, char *queries[]);

#endif
