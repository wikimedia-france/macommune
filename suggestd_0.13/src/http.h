#ifndef _HTTP_H
#define _HTTP_H

#include <stdbool.h>
#include <time.h>

typedef struct {
	unsigned int suggest;
	unsigned int set;
	unsigned int inc;
	unsigned int index_html;
	unsigned int stats;
} HttpStats;

typedef struct {
	bool embeded_index;
	HttpStats stats;
	time_t started_at;
} Http;

Http *http_new(bool embeded_index);
void http_free(Http *this);
void http_start(Http *this, char const *addr, int port);

#endif
