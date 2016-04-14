bin_PROGRAMS = suggestd

suggestd_SOURCES = \
	suggestd.c \
	args.c \
	args.h \
	global.c \
	global.h \
	log.c \
	log.h \
	item.c \
	item.h \
	http.c \
	http.h \
	json.c \
	json.h \
	conf_parser.c \
	conf_parser.h \
	db_mysql.c \
	db_mysql.h \
	db_sqlite3.c \
	db_sqlite3.h \
	node.c \
	node.h \
	tree.c \
	tree.h \
	stringlist.c \
	stringlist.h \
	fetcher.c \
	fetcher.h \
	pages.h

AM_CFLAGS = -I/usr/include/mysql -DUNIV_LINUX -DUNIV_LINUX @SQLITE3_CFLAGS@
suggestd_LDADD = -L/usr/lib/mysql -lmysqlclient -lz -lcrypt -lnsl -lm @SQLITE3_LIBS@
suggestd_LDFLAGS = -rdynamic

