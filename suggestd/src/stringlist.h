#ifndef _STRING_LIST_H
#define _STRING_LIST_H

#include <stdbool.h>

typedef struct StringListItem_ {
	char *str;
	void *data;
	struct StringListItem_ *next;
	struct StringListItem_ *previous;
} StringListItem;


typedef struct {
	StringListItem *first;
	StringListItem *last;
} StringList;

StringListItem *stringlistitem_new(char const *str, void *data);
void stringlistitem_free(StringListItem *this, bool free_data);
void stringlistitem_swap(StringListItem *a, StringListItem *b);

StringList *stringlist_new();
void stringlist_free(StringList *this, bool free_data);
void stringlist_push_back(StringList *this, StringListItem *item);
void stringlist_push_front(StringList *this, StringListItem *item);
void stringlist_insert_after(StringList *this, StringListItem *previous, StringListItem *item);
void stringlist_insert_before(StringList *this, StringListItem *next, StringListItem *item);
void stringlist_delete(StringList *this, StringListItem *item, bool free_data);
void stringlist_clear(StringList *this, bool free_data);
StringListItem *stringlist_find(StringList *this, char const *str);
unsigned int stringlist_size(StringList *this);
bool stringlist_empty(StringList *this);
void stringlist_swap(StringList *this, StringListItem *a, StringListItem *b);
void stringlist_printf(StringList *this);
void stringlist_printf_inversed(StringList *this);

#endif

