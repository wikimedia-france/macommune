#include "db_sqlite3.h"

#include <stdio.h>

#include "log.h"
#include "global.h"

void db_sqlite3_error(sqlite3 *db) {
	log_msg_printf(LOG_ERR, true, "SQLite error: %s", sqlite3_errmsg(db));
}

bool db_sqlite3_open(sqlite3 **db, char const *path) {
	int rc = sqlite3_open(path, db);
	if (rc) {
		db_sqlite3_error(*db);
		sqlite3_close(*db);
	}
	return (rc == SQLITE_OK);
}

int db_sqlite3_load_tree(sqlite3 *db, Tree *tree, char *query) {
	printf("%s...", query);
	fflush(stdout);

	sqlite3_stmt *stmt;
	int res = sqlite3_prepare(db, query, -1, &stmt, NULL);
	if (res != SQLITE_OK) {
		db_sqlite3_error(db);
		return -1;
	}

	int rows = sqlite3_column_count(stmt);
	if (rows < 1) {
		sqlite3_finalize(stmt);
		log_msg_printf(LOG_ERR, true, "Must return at least 1 fields!");
		return -1;
	}

	unsigned int count = 0;
	while ((res = sqlite3_step(stmt)) == SQLITE_ROW) {
		unsigned char const *str = sqlite3_column_text(stmt, 0);
		int value = (rows >= 2) ? sqlite3_column_int(stmt, 1) : 0;
		unsigned char const *str_real = (rows >= 3) ? sqlite3_column_text(stmt, 2) : NULL;
		tree_add(tree, (char const *) str, (char const *) str_real, value);
		count++;
	}
	sqlite3_finalize(stmt);

	printf("=> %i\n", count);
	return count;
}

void db_sqlite3_load_query(sqlite3 *db, char *name, char *query) {
	Tree *tree = global_tree_find_or_create(name);
	if (name) printf("[%s] ", name);
	db_sqlite3_load_tree(db, tree, query);
}

