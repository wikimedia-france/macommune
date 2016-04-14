#define _GLOBAL_C

#include "global.h"

#include <string.h>

#include "log.h"
#include "stringlist.h"

static char *mode_names[4] = {"xml", "php", "json", "text"};

char *global_output_mode_name(int mode) {
	return (mode < OUTPUT_MODE_XML || mode > OUTPUT_MODE_TEXT)
		? NULL
		: mode_names[mode];
}

int global_output_mode(char const *str) {
	if (str) { 
		int i;
		for (i = OUTPUT_MODE_XML; i <= OUTPUT_MODE_TEXT; i++)
			if (strcmp(str, mode_names[i]) == 0)
				return i;
	}
	return global.output_mode;
}

void global_init(char *charset, int output_mode) {
	global.charset = strdup(charset);
	global.main_tree = tree_new();
	global.trees = stringlist_new();
	global.output_mode = output_mode;

	log_msg_printf(LOG_NOTICE, true, "Initialize data (charset is: %s)", charset);
}

void global_free() {
	free(global.charset);
	tree_free(global.main_tree);

	StringListItem *it;
	for (it = global.trees->first; it != NULL; it = it->next) {
		tree_free(it->data);
	}
	stringlist_free(global.trees, false);
}

Tree *global_tree_find(char const *name) {
	if (!name)
		return global.main_tree;

	StringListItem *item = stringlist_find(global.trees, name);
	if (!item)
		return NULL;
	
	return item->data;
}

Tree *global_tree_find_or_create(char const *name) {
	Tree *tree = global_tree_find(name);
	if (!tree) {
		tree = tree_new();
		stringlist_push_back(global.trees, stringlistitem_new(name, tree));
	}
	return tree;		
}
