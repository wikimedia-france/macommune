#define _GNU_SOURCE

#include "log.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void log_open() {
	openlog(PACKAGE, LOG_PID, LOG_USER);
}

void log_msg_vprintf(const int level, bool const verbose, const char *fmt, va_list ap) {
	char *msg;
	vasprintf(&msg, fmt, ap);
	log_msg(level, verbose, msg);
	free(msg);	
}

void log_msg_printf(const int level, bool const verbose, const char *fmt, ...) {
	va_list ap;
	va_start(ap, fmt);
	log_msg_vprintf(level, verbose, fmt, ap);
	va_end(ap);
}

void log_msg(const int level, bool const verbose, char const *msg) {
	char urgency_info[5] = "INFO";
	char urgency_warning[8] = "WARNING";
	char urgency_err[6] = "ERROR";
	char urgency_notice[7] = "NOTICE";
	char urgency_debug[6] = "DEBUG";

	char *urgency;
	switch (level) {
	case LOG_INFO:
		urgency = urgency_info;
		break;
	case LOG_WARNING:
		urgency = urgency_warning;
		break;
	case LOG_ERR:
		urgency = urgency_err;
		break;
	case LOG_NOTICE:
		urgency = urgency_notice;
		break;
	case LOG_DEBUG:
		urgency = urgency_debug;
		break;
	default:
		urgency = NULL;
	}

	syslog(level, "[%s] %s", urgency, msg);

	if (verbose || true) {
		if (level == LOG_ERR)
			fprintf(stderr, "[%s] %s\n", urgency, msg);
		else
			fprintf(stdout, "[%s] %s\n", urgency, msg);
	}
}

void log_close() {
	closelog();
}

