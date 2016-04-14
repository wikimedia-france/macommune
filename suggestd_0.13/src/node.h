#ifndef _NODE_H
#define _NODE_H

#include <stdlib.h>
#include <stdbool.h>

#include "item.h"

typedef Item *NodeDataType;
#define NODE_DATA_NULL NULL

typedef struct Node_ {
	unsigned char value;
	union {
		struct Node_ *node;
		NodeDataType data;
	} child;
	struct Node_ *next;
} Node;

typedef void (*NodeSuffixesFetchCb)(char *str, NodeDataType data, void *cb_data);

Node *node_new(char const value);
void node_free(Node *this);
bool node_data_set(Node *this, NodeDataType data);
NodeDataType node_data_get(Node *this);
void node_childs_add(Node *this, Node *child);
void node_childs_insert_sorted(Node *node, Node *child);
Node *node_childs_find(Node *this, unsigned char const value);
void node_childs_show(Node *node);
void node_show(Node *this, int const level);
Node *node_suffixes_add(Node *this, char const *str, bool *is_new);
Node *node_suffixes_find(Node *this, char *str);
void node_suffixes_printf(Node *node, char *buf, size_t bufsize, size_t len);
void node_suffixes_fetch(Node *node, char *buf, size_t buf_size, size_t len, char **target, NodeDataType *target_data, unsigned int target_size, unsigned int *count);
void node_suffixes_fetch_data(Node *node, NodeDataType *target, unsigned int target_size, unsigned int *count);
void node_suffixes_fetch_fct(Node *node, char *buf, size_t buf_size, size_t len, NodeSuffixesFetchCb fct, void *cb_data, int *stop);
unsigned int node_suffixes_count(Node *node);

#endif
