#include "fetcher.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

Fetcher *fetcher_new() {
	Fetcher *this = malloc(sizeof(Fetcher));
	fetcher_init(this);
	return this;
}

void fetcher_init(Fetcher *this) {
	this->count = 0;
	this->min = -1;
	this->stop = 0;
	this->limit = FETCHER_LIMIT_DEFAULT;
}

void fetcher_clear(Fetcher *this) {
	int i;
	for (i = 0; i < this->count; i++) {
		free(this->items[i].str);
	}
	fetcher_init(this);
}

void fetcher_set_limit(Fetcher *this, int limit) {
	this->limit = (limit < FETCHER_LIMIT_MAX) ? limit : FETCHER_LIMIT_MAX;
}

void fetcher_resize(Fetcher *this, int size) {
	if (size >= this->count)
		return;

	int i;
	for (i = size; i < this->count; i++) {
		free(this->items[i].str);
	}
	this->count = size;
}

void fetcher_free(Fetcher *this) {
	fetcher_clear(this);
	free(this);
}

void fetcher_add_item(Fetcher *this, char *str, int value) {
	if (this->count >= FETCHER_SIZE)
		return;

	this->items[this->count].str = strdup(str);
	this->items[this->count].value = value;
	this->count++;
}

void fetcher_add(Fetcher *this, char *str, int value) {
	if (this->count >= this->limit)
		return;

	fetcher_add_item(this, str, value);
}

void fetcher_sorted_add(Fetcher *this, char *str, int value) {
	if (this->count == FETCHER_SIZE) {
		fetcher_sort(this);
		fetcher_resize(this, FETCHER_LIMIT_MAX);
		this->min = this->items[this->count - 1].value;
	}

	if (value > this->min)
		fetcher_add_item(this, str, value);
}

void fetcher_sorted_finalize(Fetcher *this) {
	fetcher_sort(this);
	fetcher_resize(this, this->limit);
}

void fetcher_debug(Fetcher *this) {
	printf("** Fetcher items: **\n");
	printf("min: %i\n", this->min);
	int i;
	for (i = 0; i < this->count; i++) {
		printf("%s - %i\n", this->items[i].str, this->items[i].value);
	}
}

void fetcher_items_swap(FetcherItem *a, FetcherItem *b) {
	FetcherItem t = *a; *a = *b; *b = t;
}

void fetcher_sort_part(Fetcher *this, int beg, int end) {
	if (end > beg + 1) {
		int piv = this->items[beg].value, l = beg + 1, r = end;
		while (l < r) {
			if (this->items[l].value >= piv)
				l++;
			else
				fetcher_items_swap(&this->items[l], &this->items[--r]);
		}
		fetcher_items_swap(&this->items[--l], &this->items[beg]);
		fetcher_sort_part(this, beg, l);
		fetcher_sort_part(this, r, end);
	}
}

void fetcher_sort(Fetcher *this) {
	fetcher_sort_part(this, 0, this->count);
}
