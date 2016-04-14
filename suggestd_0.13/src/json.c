#include "json.h"

#include <stdio.h>
#include <stdlib.h>

const char *json_escape_char(char c) {
	switch (c) {
		case '\\':
			return "\\\\";
		case '/':
			return "\\/";
		case '"':
			return "\\\"";
		case '\b':
			return "\\b";
		case '\f':
			return "\\f";
		case '\t':
			return "\\t";
		case '\n':
			return "\\n";
		case '\r':
			return "\\r";
		default:
			break;
	}
	return NULL;
}

char *json_escape(const char *str) {
	const char *replaced;
	char const *it;

	size_t size = 1;
	for (it = str; *it != '\0'; it++) {
		replaced = json_escape_char(*it);
		size += replaced ? strlen(replaced) : 1;
	}

	char *escaped = malloc(size);
	char *cursor = escaped;

	for (it = str; *it != '\0'; it++) {
		replaced = json_escape_char(*it);

		if (replaced) {
			strcpy(cursor, replaced);
			cursor += strlen(replaced);
		}
		else {
			*cursor = *it;
			cursor++;
		}
	}
	*cursor = '\0';
	return escaped;
}

