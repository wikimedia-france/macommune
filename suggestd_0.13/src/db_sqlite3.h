#ifndef _DB_SQLITE3
#define _DB_SQLITE3

#include <stdbool.h>
#include <sqlite3.h>

#include "tree.h"

bool db_sqlite3_open(sqlite3 **db, char const *path);
int db_sqlite3_load_tree(sqlite3 *db, Tree *tree, char *query);
void db_sqlite3_load_query(sqlite3 *db, char *name, char *query);

#endif
