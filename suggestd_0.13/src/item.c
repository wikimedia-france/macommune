#include "item.h"

#include <stdlib.h>
#include <string.h>

Item *item_new(char const *str, int value) {
	Item *this = malloc(sizeof(Item));
	item_init(this);
	item_set(this, str, value);
	return this;
}

void item_set(Item *this, char const *str, int value) {
	this->value = value;

	if (!(this->str && str && strcmp(this->str, str) == 0)) {
		if (this->str) free(this->str);
		this->str = (str) ? strdup(str) : NULL;
	}
}

void item_inc(Item *this, char const *str, int n) {
	item_set(this, str, this->value + n);
}

void item_init(Item *this) {
	this->str = NULL;
	this->value = 0;
}

void item_clear(Item *this) {
	if (this->str)
		free(this->str);
	item_init(this);
}

void item_free(Item *this) {
	item_clear(this);
	free(this);
}
