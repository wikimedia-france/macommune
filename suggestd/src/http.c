#define _GNU_SOURCE

#include "http.h"

#include <sys/queue.h>
#include <stdlib.h>
#include <stdio.h>
#include <evhttp.h>
#include <string.h>
#include <unistd.h>

#include "log.h"
#include "global.h"
#include "tree.h"
#include "pages.h"
#include "stringlist.h"
#include "fetcher.h"
#include "json.h"

#define MIN(a,b) ((a) < (b) ? (a) : (b))

#define PARSE_REQUEST(request, params) { \
	char const *uri = evhttp_request_uri(request); \
	log_msg_printf(LOG_NOTICE, true, "GET %s", uri); \
	char *uri_decoded = evhttp_decode_uri(uri); \
	evhttp_parse_query(uri_decoded, &params); \
	free(uri_decoded); \
}

Http *http_new(bool embeded_index) {
	Http *this = malloc(sizeof(Http));
	this->started_at = 0;
	this->embeded_index = embeded_index;
	this->stats.suggest = 0;
	this->stats.inc = 0;
	this->stats.set = 0;
	this->stats.index_html = 0;
	this->stats.stats = 0;
	return this;
}

void http_free(Http *this) {
	free(this);
}

void http_callback_default(struct evhttp_request *request, void *data) {
	evhttp_send_error(request, HTTP_NOTFOUND, "Service not found");
}

void http_send_header(struct evkeyvalq *output_headers, char *type) {
	char *header;
	(void) asprintf(&header, "%s; charset=%s", type, global.charset);
	evhttp_add_header(output_headers, "Content-Type", header);
	free(header);
}

#define HOSTNAME_BUFFER_SIZE 128
void http_stats_query(Http *this, struct evhttp_request *request) {
	this->stats.stats++;

	//prepare output
	struct evbuffer *buffer = evbuffer_new();

	//hostname 
	char hostname_buffer[HOSTNAME_BUFFER_SIZE];
	if (gethostname(hostname_buffer, HOSTNAME_BUFFER_SIZE) == 0) {
		hostname_buffer[HOSTNAME_BUFFER_SIZE - 1] = '\0';
		evbuffer_add_printf(buffer, "HOSTNAME %s\n", hostname_buffer);
	}

	evbuffer_add_printf(buffer, "VERSION %s\n", VERSION);
	evbuffer_add_printf(buffer, "UPTIME %li\n", time(NULL) - this->started_at);
	evbuffer_add_printf(buffer, "CHARSET %s\n", global.charset);
	evbuffer_add_printf(buffer, "OUTPUT_MODE %s\n", global_output_mode_name(global.output_mode));

	if (this->embeded_index) evbuffer_add_printf(buffer, "PAGE /index.html %i\n", this->stats.index_html);
	evbuffer_add_printf(buffer, "PAGE /suggest %i\n", this->stats.suggest);
	evbuffer_add_printf(buffer, "PAGE /inc %i\n", this->stats.inc);
	evbuffer_add_printf(buffer, "PAGE /set %i\n", this->stats.set);
	evbuffer_add_printf(buffer, "PAGE /stats %i\n", this->stats.stats);

	evbuffer_add_printf(buffer, "MAINTREE %i\n", global.main_tree->count);
	StringListItem *it;
	for (it = global.trees->first; it != NULL; it = it->next) {
		Tree *tree = it->data;
		evbuffer_add_printf(buffer, "TREE %s %i\n", it->str, tree->count);
	}

	//send
	http_send_header(request->output_headers, "text");
	evhttp_send_reply(request, HTTP_OK, "", buffer);

	evbuffer_free(buffer);
}

void http_stats_callback(struct evhttp_request *request, void *data) {
	http_stats_query((Http *) data, request);
}

void http_set_query(Http *this, struct evhttp_request *request, struct evkeyvalq *params_get) {
	this->stats.set++;

	//tree
	char const *arg_tree = evhttp_find_header(params_get, "tree");
	Tree *tree = global_tree_find_or_create(arg_tree);

	//str
	char const *arg_str = evhttp_find_header(params_get, "str");
	if (!arg_str || strlen(arg_str) < 1) {
		evhttp_send_error(request, HTTP_NOTFOUND, "'str' is mendator");
		return;
	}

	//str_real
	char const *arg_str_real = evhttp_find_header(params_get, "str_real");

	//value
	int value = 0;
	char const *arg_value = evhttp_find_header(params_get, "value");
	if (arg_value) 
		value = atoi(arg_value);


	tree_set(tree, arg_str, arg_str_real, value);

	struct evbuffer *buffer = evbuffer_new();
	evbuffer_add_printf(buffer, "OK\n");
	http_send_header(request->output_headers, "text");
	evhttp_send_reply(request, HTTP_OK, "", buffer);
	evbuffer_free(buffer);
}

void http_set_callback(struct evhttp_request *request, void *data) {
	struct evkeyvalq params_get;
	PARSE_REQUEST(request, params_get);

	http_set_query((Http *) data, request, &params_get);

	evhttp_clear_headers(&params_get);
}

void http_inc_query(Http *this, struct evhttp_request *request, struct evkeyvalq *params_get) {
	this->stats.inc++;

	//tree
	char const *arg_tree = evhttp_find_header(params_get, "tree");
	Tree *tree = global_tree_find_or_create(arg_tree);

	//str
	char const *arg_str = evhttp_find_header(params_get, "str");
	if (!arg_str || strlen(arg_str) < 1) {
		evhttp_send_error(request, HTTP_NOTFOUND, "'str' is mendator");
		return;
	}

	//str_real
	char const *arg_str_real = evhttp_find_header(params_get, "str_real");

	//value
	int value = 0;
	char const *arg_value = evhttp_find_header(params_get, "value");
	if (arg_value) 
		value = atoi(arg_value);


	tree_inc(tree, arg_str, arg_str_real, value);

	struct evbuffer *buffer = evbuffer_new();
	evbuffer_add_printf(buffer, "OK\n");
	http_send_header(request->output_headers, "text");
	evhttp_send_reply(request, HTTP_OK, "", buffer);
	evbuffer_free(buffer);
}

void http_inc_callback(struct evhttp_request *request, void *data) {
	struct evkeyvalq params_get;
	PARSE_REQUEST(request, params_get);

	http_inc_query((Http *) data, request, &params_get);

	evhttp_clear_headers(&params_get);
}

#define DEFAULT_SIZE (FETCHER_SIZE / 2)

void http_suggest_query(Http *this, struct evhttp_request *request, struct evkeyvalq *params_get) {
	this->stats.suggest++;

	//str
	char const *arg_str = evhttp_find_header(params_get, "str");
	if (!arg_str) {
		evhttp_send_error(request, HTTP_NOTFOUND, "'str' is mendator");
		return;
	}

	//tree
	char const *arg_tree = evhttp_find_header(params_get, "tree");
	Tree *tree = global_tree_find(arg_tree);
	if (!tree) {
		evhttp_send_error(request, HTTP_NOTFOUND, "Unknown tree");
		return;
	}

	//size
	char const *arg_size = evhttp_find_header(params_get, "size");
	size_t size = DEFAULT_SIZE;
	if (arg_size != NULL) {
		size = atoi(arg_size);
	}

	//sort
	char const *arg_sort = evhttp_find_header(params_get, "sort");
	bool sort = (arg_sort != NULL);

	//mode
	char const *arg_mode = evhttp_find_header(params_get, "mode");
	int mode = global_output_mode(arg_mode);

	//prepare output
	Fetcher *fetcher = fetcher_new();
	fetcher_set_limit(fetcher, size);
	tree_find(tree, (char *) arg_str, fetcher, sort);
	struct evbuffer *buffer = evbuffer_new();
	int count = MIN(size, fetcher->count);

	//xml output
	if (mode == OUTPUT_MODE_XML) {
		evbuffer_add_printf(buffer, "<?xml version=\"1.0\" encoding=\"%s\"?>\n<items>\n", global.charset);
		int i;
		for (i = 0; i < count; i++) {
			char *str_escaped = evhttp_htmlescape(fetcher->items[i].str);
			int value = fetcher->items[i].value;
			evbuffer_add_printf(buffer, "\t<item value=\"%i\">%s</item>\n", value, str_escaped);
			free(str_escaped);
		}
		evbuffer_add_printf(buffer, "</items>\n");
		http_send_header(request->output_headers, "text/xml");
	}

	//php output
	else if (mode == OUTPUT_MODE_PHP) {
		evbuffer_add_printf(buffer, "a:%i:{", count);
		int i;
		for (i = 0; i < count; i++) {
			char *str = fetcher->items[i].str;
			int value = fetcher->items[i].value;
			evbuffer_add_printf(buffer, "i:%i;a:2:{s:3:\"str\";s:%zi:\"%s\";s:5:\"value\";i:%i;}", i, strlen(str), str, value);
		}
		evbuffer_add_printf(buffer, "}");
		http_send_header(request->output_headers, "text");
	}

	//json output
	else if (mode == OUTPUT_MODE_JSON) {
		evbuffer_add_printf(buffer, "[");
		int i;
		for (i = 0; i < count; i++) {
			char *str_escaped = json_escape(fetcher->items[i].str);
			int value = fetcher->items[i].value;
			char *delim = (i == 0) ? "" : ",";
			evbuffer_add_printf(buffer, "%s{\"str\":\"%s\",\"value\":%i}", delim, str_escaped, value);
			free(str_escaped);
		}
		evbuffer_add_printf(buffer, "]");
		http_send_header(request->output_headers, "text");
	}

	//text output
	else if (mode == OUTPUT_MODE_TEXT) {
		int i;
		for (i = 0; i < count; i++) {
			char *str = fetcher->items[i].str;
			int value = fetcher->items[i].value;
			evbuffer_add_printf(buffer, "%s\t%i\n", str, value);
		}
		http_send_header(request->output_headers, "text");
	}

	//free data
	fetcher_free(fetcher);

	//send
	evhttp_send_reply(request, HTTP_OK, "", buffer);
	evbuffer_free(buffer);
}

void http_suggest_callback(struct evhttp_request *request, void *data) {
	struct evkeyvalq params_get;
	PARSE_REQUEST(request, params_get);

	http_suggest_query((Http *) data, request, &params_get);

	evhttp_clear_headers(&params_get);
}

void http_page_index_callback(struct evhttp_request *request, void *data) {
	Http *this = (Http *) data;
	this->stats.index_html++;

	struct evbuffer *buffer = evbuffer_new();
	evbuffer_add_printf(buffer, PAGE_INDEX_HTML);
	http_send_header(request->output_headers, "text/html");
	evhttp_send_reply(request, HTTP_OK, "", buffer);
	evbuffer_free(buffer);
}

void http_start(Http *this, char const *addr, int port) {
	log_msg_printf(LOG_NOTICE, true, "Start HTTP server (%s:%i)", addr, port);

	this->started_at = time(NULL);

	struct event_base *base = event_init();
	struct evhttp *server = evhttp_new(base);
	int res = evhttp_bind_socket(server, addr, port);
	if (res != 0) {
		log_msg_printf(LOG_ERR, true, "Could not start http server!");
		return;
	}

	evhttp_set_gencb(server, http_callback_default, this);
	evhttp_set_cb(server, "/suggest", http_suggest_callback, this);
	evhttp_set_cb(server, "/add", http_set_callback, this);
	evhttp_set_cb(server, "/set", http_set_callback, this);
	evhttp_set_cb(server, "/inc", http_inc_callback, this);
	evhttp_set_cb(server, "/stats", http_stats_callback, this);
	if (this->embeded_index) evhttp_set_cb(server, "/index.html", http_page_index_callback, this);

	event_base_dispatch(base);
}
