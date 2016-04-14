#include "stringlist.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

StringListItem *stringlistitem_new(char const *str, void *data) {
	StringListItem *this = malloc(sizeof(StringListItem));
	this->next = NULL;
	this->previous = NULL;
	this->str = strdup(str);
	this->data = data;
	return this;
}

void stringlistitem_free(StringListItem *this, bool free_data) {
	if (free_data)
		free(this->data);

	free(this->str);
	free(this);
}

void stringlistitem_swap(StringListItem *a, StringListItem *b) {
	void* a_data = a->data;
	char *a_str = a->str;
	a->data = b->data;
	a->str = b->str;
	b->data = a_data;
	b->str = a_str;
}

StringList *stringlist_new() {
	StringList *this = malloc(sizeof(StringList));
	this->first = NULL;
	this->last = NULL;
	return this;
}

void stringlist_free(StringList *this, bool free_data) {
	stringlist_clear(this, free_data);
	free(this);
}

void stringlist_push_back(StringList *this, StringListItem *item) {
	item->previous = this->last;

	if (item->previous != NULL) {
		item->previous->next = item;
	}

	if (this->first == NULL) {
		this->first = item;
	}

	this->last = item;
}

void stringlist_push_front(StringList *this, StringListItem *item) {
	item->next = this->first;

	if (item->next != NULL) {
		item->next->previous = item;
	}

	if (this->last == NULL) {
		this->last = item;
	}

	this->first = item;
}

void stringlist_insert_after(StringList *this, StringListItem *previous, StringListItem *item) {
	item->next = previous->next;
	item->previous = previous;
	previous->next = item;
	if (item->next != NULL)
		item->next->previous = item;
	if (previous == this->last)
		this->last = item;
}

void stringlist_insert_before(StringList *this, StringListItem *next, StringListItem *item) {
	item->previous = next->previous;
	item->next = next;
	next->previous = item;
	if (item->previous != NULL)
		item->previous->next = item;
	if (next == this->first)
		this->first = item;
}

void stringlist_clear(StringList *this, bool free_data) {
	StringListItem *it;
	for (it = this->first; it != NULL; it = it->next) {
		stringlistitem_free(it, free_data);
	}
	this->first = this->last = NULL;
}

void stringlist_delete(StringList *this, StringListItem *item, bool free_data) {
	if (item->previous != NULL)
		item->previous->next = item->next;
	if (item->next != NULL)
		item->next->previous = item->previous;
	if (this->first == item)
		this->first = item->next;
	if (this->last == item)
		this->last = item->previous;
	stringlistitem_free(item, free_data);
}

StringListItem *stringlist_find(StringList *this, char const *str) {
	StringListItem *it;
	for (it = this->first; it != NULL; it = it->next) {
		if (strcmp(str, it->str) == 0)
			return it;
	}
	return NULL;
}

unsigned int stringlist_size(StringList *this) {
	unsigned size = 0;
	StringListItem *it;
	for (it = this->first; it != NULL; it = it->next) {
		size++;
	}
	return size;
}

bool stringlist_empty(StringList *this) {
	return (this->first == NULL);
}

void stringlist_printf(StringList *this) {
	StringListItem *it;
	for (it = this->first; it != NULL; it = it->next) {
		printf("%s\n", it->str);
	}
}

void stringlist_printf_inversed(StringList *this) {
	StringListItem *it;
	for (it = this->last; it != NULL; it = it->previous) {
		printf("%s\n", it->str);
	}
}

