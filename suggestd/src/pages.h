#ifndef PAGES_H
#define PAGES_H

#define PAGE_JS \
"var myAjax = ajax(); \n" \
"var suggestInput = null;\n" \
"var suggestTree = null;\n" \
"var suggestDiv = null;\n" \
"var suggestAsChanged = false;\n" \
"var suggestFocused = false;\n" \
"\n" \
"function ajax() {\n" \
"	var ajax = null;\n" \
"	if (window.XMLHttpRequest) {\n" \
"		try {\n" \
"			ajax = new XMLHttpRequest();\n" \
"		}\n" \
"		catch(e) {}\n" \
"	}\n" \
"	else if (window.ActiveXObject) {\n" \
"		try {\n" \
"			ajax = new ActiveXObject(\"Msxm12.XMLHTTP\");\n" \
"		}\n" \
"		catch (e){\n" \
"			try{\n" \
"				ajax = new ActiveXObject(\"Microsoft.XMLHTTP\");\n" \
"			}\n" \
"			catch (e) {}\n" \
"		}\n" \
"	}\n" \
"	return ajax;\n" \
"}\n" \
"\n" \
"function suggestInit() {\n" \
"	suggestDiv = document.getElementById('suggest');\n" \
"	suggestInput = document.getElementById('str');\n" \
"	suggestTree = document.getElementById('tree');\n" \
"	suggestInput.focus();\n" \
"}\n" \
"\n" \
"function suggestShowResults(list) {\n" \
"	suggestDiv.innerHTML = '';\n" \
"\n" \
"	if (list.length == 0) {\n" \
"		suggestVisible(false);\n" \
"		return;\n" \
"	}\n" \
"\n" \
"	var ul = document.createElement(\"UL\");\n" \
"	suggestDiv.appendChild(ul);\n" \
"\n" \
"	for (i in list) {\n" \
"		var li = document.createElement(\"LI\");\n" \
"		li.innerHTML = \"<a onclick='suggestSelect(this.firstChild.data)'>\" + list[i][0] + \"<div class='cardinality'>\" +  + list[i][1] + \"</div></a>\";\n" \
"		ul.appendChild(li);\n" \
"	}\n" \
"	suggestVisible(true);\n" \
"}\n" \
"\n" \
"function suggestGetResults(xmlDoc) {\n" \
"	var nodes = xmlDoc.getElementsByTagName('item');\n" \
"	var list = new Array();\n" \
"	for (var i = 0; i < nodes.length; i++) {\n" \
"		var cardinality = nodes[i].getAttribute('value');\n" \
"		var str = nodes[i].firstChild.data;\n" \
"		list.push(new Array(str, cardinality));\n" \
"	}\n" \
"	return list;\n" \
"}\n" \
"\n" \
"function suggestRequestCallback() {\n" \
"	if (myAjax.readyState == 4 && myAjax.responseXML != null) {\n" \
"		var list = suggestGetResults(myAjax.responseXML);\n" \
"		suggestShowResults(list);\n" \
"	}\n" \
"	else {\n" \
"		suggestVisible(false);\n" \
"	}\n" \
"}\n" \
"\n" \
"function suggestRequestSend(str, tree) {\n" \
"	if (!str) {\n" \
"		suggestVisible(false);\n" \
"		suggestDiv.innerHTML = '';\n" \
"		return;\n" \
"	}\n" \
"	var url = \"suggest?mode=xml&size=20&str=\" + str;\n" \
"	if (tree) url += \"&tree=\" + tree;\n" \
"	myAjax.open(\"GET\", url);\n" \
"	myAjax.onreadystatechange = suggestRequestCallback;\n" \
"	myAjax.setRequestHeader(\"Content-type\", \"application/x-www-form-urlencoded\");\n" \
"	myAjax.send(null);\n" \
"}\n" \
"\n" \
"function suggestVisible(state) {\n" \
"	suggestDiv.style.visibility = (state) ? \"visible\" : \"hidden\";\n" \
"}\n" \
"\n" \
"function suggestChanged() {\n" \
"	suggestAsChanged = true;\n" \
"}\n" \
"\n" \
"function suggestSetFocused(state) {\n" \
"	suggestFocused = state;\n" \
"	if (state) {\n" \
"		suggestMainLoop();\n" \
"	}\n" \
"	else {\n" \
"		setTimeout(\"suggestVisible(false)\", 300);\n" \
"	}\n" \
"}\n" \
"\n" \
"function suggestSelect(str, tree) {\n" \
"	suggestInput.value = str;\n" \
"	suggestVisible(false);\n" \
"	suggestInput.focus();\n" \
"}\n" \
"\n" \
"function suggestMainLoop() {\n" \
"	if (suggestFocused) {\n" \
"		if (suggestAsChanged) {\n" \
"			suggestAsChanged = false;\n" \
"			suggestRequestSend(suggestInput.value, suggestTree.value);\n" \
"		}\n" \
"		setTimeout(\"suggestMainLoop()\", 200);\n" \
"	}\n" \
"	return true;\n" \
"}\n"

#define PAGE_CSS \
"div.suggest {\n" \
"	background-color: #fff;\n" \
"	border: 1px solid #aaa;\n" \
"	position: absolute;\n" \
"	margin: 1px;\n" \
"	padding: 2px; \n" \
"}\n" \
"\n" \
"div.suggest ul {\n" \
"	margin: 0;\n" \
"	padding: 2;\n" \
"	list-style: none;\n" \
"	border-left: 5px solid #ddd;\n" \
"}\n" \
"\n" \
"div.suggest .cardinality{\n" \
"	color: #888;\n" \
"	position: absolute;\n" \
"	top: 0;\n" \
"	right: 0;\n" \
"}\n" \
"\n" \
"div.suggest a {\n" \
"	color: #000;\n" \
"	display: block;\n" \
"	min-width: 284px;\n" \
"	cursor: pointer;\n" \
"	padding: 1px 3px;\n" \
"	text-decoration: none;\n" \
"	position: relative;\n" \
"}\n" \
"\n" \
"div.suggest a:hover{\n" \
"	background-color: #ddd;\n" \
"	background-image: none;\n" \
"}\n"

#define PAGE_INDEX_HTML \
"<html>\n" \
"<head>\n" \
"<style type=\"text/css\">\n" \
PAGE_CSS \
"</style>\n" \
"</head>\n" \
"\n" \
"<body onload=\"suggestInit()\">\n" \
"<script language=\"javascript\"> \n" \
PAGE_JS \
"</script> \n" \
"<form method=\"get\">\n" \
"tree: <input id=\"tree\" name=\"tree\" value=\"\"/><br/>\n" \
"str: <input id=\"str\" name=\"str\" value=\"\" autocomplete=\"off\" onkeyup=\"suggestChanged();\" onFocus=\"suggestSetFocused(true);\" onBlur=\"suggestSetFocused(false);\"/>\n" \
"<div id=\"suggest\" class=\"suggest\" style=\"visibility: hidden;\"></div>\n" \
"</form>\n" \
"</body>\n"

#endif
