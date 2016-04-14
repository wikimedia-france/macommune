#ifndef _TREE_H
#define _TREE_H

#include "node.h"
#include "stringlist.h"
#include "fetcher.h"

typedef struct {
	Node *main;
	unsigned int count;
} Tree;

Tree *tree_new();
void tree_free(Tree *this);
void tree_add(Tree *this, char const *str, char const *str_real, int const value);
void tree_printf(Tree *this);
void tree_find(Tree *this, char *str, Fetcher *fetcher, bool sort);

#endif

