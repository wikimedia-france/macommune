AC_INIT
AM_INIT_AUTOMAKE(suggestd, 0.13)

AC_PROG_CC
AC_PROG_INSTALL

PKG_CHECK_MODULES(SQLITE3, [sqlite3])

AC_CHECK_LIB(event, evhttp_new, [], [
	echo "Error! You need libevent >= 1.4."
	exit -1
])

AC_CHECK_LIB(expat, XML_ParserCreate, [], [
	echo "Error! You need libexpat."
	exit -1
])

AC_OUTPUT(Makefile src/Makefile doc/Makefile)


