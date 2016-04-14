#ifndef _LOG_H
#define _LOG_H

#include <syslog.h>
#include <stdarg.h>
#include <stdbool.h>

void log_open();
void log_msg_printf(const int level, bool const verbose, const char *fmt, ...);
void log_msg(const int level, bool const verbose, char const *msg);
void log_close();

#endif
