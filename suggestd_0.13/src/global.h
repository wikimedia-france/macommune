#ifndef _GLOBAL_H
#define _GLOBAL_H

#include "stringlist.h"
#include "tree.h"

#define OUTPUT_MODE_XML 0
#define OUTPUT_MODE_PHP 1
#define OUTPUT_MODE_JSON 2
#define OUTPUT_MODE_TEXT 3
#define OUTPUT_MODE_DEFAULT OUTPUT_MODE_XML

typedef struct {
	Tree *main_tree;
	StringList *trees;
	char *charset;
	int output_mode;
} Global;

void global_init(char *charset, int output_mode);
void global_free();
int global_output_mode(char const *str);
char *global_output_mode_name(int mode);
Tree *global_tree_find(char const *name);
Tree *global_tree_find_or_create(char const *name);

#ifdef _GLOBAL_C
Global global;
#else
extern Global global;
#endif

#endif

