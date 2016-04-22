var Carte = function(node, titles, cb) {
	this.node = node;
	this.titles = titles;
	this.cb = cb;
	this.init();
}

Carte.prototype.init = function() {
	for(var i = 0; i < this.node.childNodes.length; i++) {
		var child = this.node.childNodes[i];
		if ("tagName" in child && child.tagName == "path") {
			this.initRegion(child);
		}
	}
}

Carte.prototype.initRegion = function(node) {
	var self = this;

	var ref = node.getAttribute("ref");
	if (ref && ref in this.titles) {
		var title = this.titles[ref];
		var el = document.createElementNS("http://www.w3.org/2000/svg", "title");
		el.appendChild(document.createTextNode(title));
		node.appendChild(el); 
	}

	node.onmouseenter = function() {
		node.setAttribute("style", "fill: #8080ff;");
	}
	node.onmouseleave = function() {
		node.setAttribute("style", "");
	}
	node.onclick = function() {
		self.cb(node);
	}
}

