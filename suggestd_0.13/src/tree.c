#define _TREE_C

#include "tree.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

Tree *tree_new() {
	Tree *this = malloc(sizeof(Tree));
	this->main = node_new('\0');
	this->count = 0;
	return this;
}

void tree_free(Tree *this) {
	node_free(this->main);
	free(this);
}

void tree_add(Tree *this, char const *str, char const *str_real, int const value) {
	if (strcmp(str, "") == 0)
		return;

	bool is_new = false;
	Node *node = node_suffixes_add(this->main, str, &is_new);
	if (is_new) {
		if (str_real && strcmp(str, str_real) == 0)
			str_real = NULL;
		Item *item = item_new(str_real, value);
		node_data_set(node, item);
		this->count++;
	}
}

void tree_set(Tree *this, char const *str, char const *str_real, int const value) {
	if (strcmp(str, "") == 0)
		return;

	if (str_real && strcmp(str, str_real) == 0)
		str_real = NULL;

	bool is_new = false;
	Node *node = node_suffixes_add(this->main, str, &is_new);

	if (is_new) {
		this->count++;
		Item *item = item_new(str_real, value);
		node_data_set(node, item);
	} 
	else {
		Item *item = node_data_get(node);
		item_set(item, str_real, value);
	}
}

void tree_inc(Tree *this, char const *str, char const *str_real, int const n) {
	if (strcmp(str, "") == 0)
		return;

	if (str_real && strcmp(str, str_real) == 0)
		str_real = NULL;

	bool is_new = false;
	Node *node = node_suffixes_add(this->main, str, &is_new);

	if (is_new) {
		this->count++;
		Item *item = item_new(str_real, n);
		node_data_set(node, item);
	} 
	else {
		Item *item = node_data_get(node);
		item_inc(item, str_real, n);
	}
}

void tree_find_sorted_cb(char *str, Item *item, void *cb_data) {
	fetcher_sorted_add((Fetcher *) cb_data, item->str != NULL ? item->str : str, item->value);
}

void tree_find_cb(char *str, Item *item, void *cb_data) {
	Fetcher *fetcher = (Fetcher *) cb_data;
	fetcher_add(fetcher, item->str != NULL ? item->str : str, item->value);
	if (fetcher->count == fetcher->limit)
		fetcher->stop = 1;
}

void tree_find(Tree *this, char *str, Fetcher *fetcher, bool sort) {
	if (str == NULL)
		return;

	Node *node = node_suffixes_find(this->main, str);
	if (node == NULL)
		return;

	char buf[256];
	strncpy(buf, str, sizeof(buf));

	if (sort) {
		node_suffixes_fetch_fct(node, buf, sizeof(buf), strlen(str), tree_find_sorted_cb, fetcher, &fetcher->stop);
		fetcher_sorted_finalize(fetcher);
	}
	else {
		node_suffixes_fetch_fct(node, buf, sizeof(buf), strlen(str), tree_find_cb, fetcher, &fetcher->stop);
	}
}

void tree_printf(Tree *this) {
}

