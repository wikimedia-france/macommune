#ifndef _ITEM_H
#define _ITEM_H

typedef struct {
	char *str;
	int value;
} Item;

Item *item_new(char const *str, int value);
void item_set(Item *this, char const *str, int value);
void item_inc(Item *this, char const *str, int n);
void item_init(Item *this);
void item_clear(Item *this);
void item_free(Item *this);

#endif
