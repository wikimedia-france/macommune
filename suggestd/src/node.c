#include "node.h"

#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

Node *node_new(char const value) {
	Node *this = (Node*) malloc(sizeof(Node));
	this->child.node = NULL;
	this->next = NULL;
	this->value = value;
	return this;
}

void node_free(Node *this) {
	if (this->value != '\0')
		node_free(this->child.node);
	if (this->next != NULL)
		node_free(this->next);
	free(this);
}

NodeDataType node_data_get(Node *this) {
	return (this->value == '\0') ? this->child.data : NODE_DATA_NULL;
}

bool node_data_set(Node *this, NodeDataType data) {
	if (this->value != '\0')
		return false;
	this->child.data = data;
	return true;
}

void node_childs_add(Node *this, Node *child) {
	if (this->child.node == NULL) {
		this->child.node = child;
		return;
	}

	Node *it = this->child.node;
	while (it->next != NULL)
		it = it->next;
	it->next = child;
}

void node_childs_insert_sorted(Node *node, Node *child) {
	if (node->child.node == NULL) {
		node->child.node = child;
		return;
	}

	Node *first = node->child.node;
	if (child->value < first->value) {
		node->child.node = child;
		child->next = first;
		return;
	}

	Node *it = first;
	while (it->next != NULL && it->next->value < child->value) {
		it = it->next;
	}

	child->next = it->next;
	it->next = child;
}

Node *node_childs_find(Node *this, unsigned char const value) {
	Node *it;
	for (it = this->child.node; it != NULL; it = it->next)
		if (it->value == value)
			return it;
	return NULL;
}

void node_childs_show(Node *this) {
	Node *it;
	for (it = this->child.node; it != NULL; it = it->next) {
		if (it->value == '\0')
			printf("\"\n");
		else
			printf("%c\n", it->value);
	}
}

void node_show(Node *this, int const level) {
	int l;
	for (l = 0; l < level; l++)
		printf(" ");

	if (this->value == '\0')
		printf("\"\n");
	else
		printf("%c\n", this->value);

	Node *it;
	for (it = this->child.node; it != NULL; it = it->next)
		node_show(it, level + 1);
}

Node *node_suffixes_find(Node *this, char *str) {
	if (str[0] == '\0')
		return this;

	Node *child = node_childs_find(this, str[0]);
	if (child == NULL)
		return NULL;

	return node_suffixes_find(child, str + 1);
}

Node *node_suffixes_add(Node *this, char const *str, bool *is_new) {
	Node *child = node_childs_find(this, str[0]);
	if (child == NULL) {
                *is_new = true;
		child = node_new(str[0]);
		node_childs_insert_sorted(this, child);
	}
	return (str[0] != '\0') ? node_suffixes_add(child, str + 1, is_new) : child;
}

void node_suffixes_printf(Node *node, char *buf, size_t buf_size, size_t len) {
	if (node->child.node == NULL)
		return;

	if (len >= buf_size)
		return;

	Node *it;
	for (it = node->child.node; it != NULL; it = it->next) {
		buf[len] = it->value;
		if (it->value == '\0') {
			fwrite(buf, 1, len, stdout);
			printf("\n");
		}
		else {
			node_suffixes_printf(it, buf, buf_size, len + 1);
		}
	}
}

void node_suffixes_fetch(Node *node, char *buf, size_t buf_size, size_t len, char **target, NodeDataType *target_data, unsigned int target_size, unsigned int *count) {
	if (node->child.node == NULL)
		return;

	if (len >= buf_size)
		return;

	Node *it;
	for (it = node->child.node; it != NULL; it = it->next) {
		if (*count >= target_size)
			return;

		buf[len] = it->value;
		if (it->value == '\0') {
			target[*count] = malloc(len + 1);
			memcpy(target[*count], buf, len + 1);
			if (target_data != NULL)
				target_data[*count] = it->child.data;
			(*count)++;
		}
		else {
			node_suffixes_fetch(it, buf, buf_size, len + 1, target, target_data, target_size, count);
		}
	}
}

void node_suffixes_fetch_data(Node *node, NodeDataType *target, unsigned int target_size, unsigned int *count) {
	if (node->child.node == NULL)
		return;

	Node *it;
	for (it = node->child.node; it != NULL; it = it->next) {
		if (*count >= target_size)
			return;

		if (it->value == '\0') {
			target[*count] = it->child.data;
			(*count)++;
		}
		else {
			node_suffixes_fetch_data(it, target, target_size, count);
		}
	}
}

void node_suffixes_fetch_fct(Node *node, char *buf, size_t buf_size, size_t len, NodeSuffixesFetchCb fct, void *cb_data, int *stop) {
	if (node->child.node == NULL)
		return;

	if (len >= buf_size)
		return;

	Node *it;
	for (it = node->child.node; it != NULL && *stop != 1; it = it->next) {
		buf[len] = it->value;
		if (it->value == '\0') {
			fct(buf, it->child.data, cb_data);
		}
		else {
			node_suffixes_fetch_fct(it, buf, buf_size, len + 1, fct, cb_data, stop);
		}
	}
}

unsigned int node_suffixes_count(Node *node) {
	if (node->child.node == NULL)
		return 0;

	unsigned int count = 0;
	Node *it;
	for (it = node->child.node; it != NULL; it = it->next) {
		if (it->value == '\0')
			count++;
		else
			count += node_suffixes_count(it);
	}
	return count;
}


