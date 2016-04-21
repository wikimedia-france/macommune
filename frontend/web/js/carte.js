document.createElementSVG = function(name) {
	return document.createElementNS("http://www.w3.org/2000/svg", name);
};

var Carte = function(node, cb) {
	this.node = node;
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
	node.setAttribute("stroke", "#ffffff");
	node.setAttribute("fill", "#808080");
	node.setAttribute("style", "cursor: pointer;");
	node.setAttribute("stroke-width", "1.5");

	var title = node.getAttribute("title");
	if (title) {
		var el = document.createElementNS("http://www.w3.org/2000/svg", "title");
		el.appendChild(document.createTextNode(title));
		node.appendChild(el); 
	}


	node.onmouseenter = function() {
		node.setAttribute("fill", "#ffffa0");
	}
	node.onmouseleave = function() {
		node.setAttribute("fill", "#808080");
	}
	node.onclick = function() {
		region = node.getAttribute("region");
		self.cb(node);
	}
}

