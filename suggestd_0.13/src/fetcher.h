#ifndef _FETCHER_H
#define _FETCHER_H


#define FETCHER_LIMIT_DEFAULT 16
#define FETCHER_LIMIT_MAX 512
#define FETCHER_SIZE (FETCHER_LIMIT_MAX * 2)

#include <stdbool.h>

typedef struct {
	char *str;
	int value;
} FetcherItem;

typedef struct {
	int count;
	FetcherItem items[FETCHER_SIZE];
	int min;
	int limit;
	int stop;
} Fetcher;

Fetcher *fetcher_new();
void fetcher_clear(Fetcher *this);
void fetcher_free(Fetcher *this);
void fetcher_init(Fetcher *this);
void fetcher_set_limit(Fetcher *this, int limit);
void fetcher_add(Fetcher *this, char *str, int value);
void fetcher_debug(Fetcher *this);
void fetcher_sort(Fetcher *this);

void fetcher_sorted_add(Fetcher *this, char *str, int value);
void fetcher_sorted_finalize(Fetcher *this);

#endif
