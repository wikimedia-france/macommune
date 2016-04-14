var Suggest = function(inputNode, baseurl) {
	this.baseurl = baseurl;
	this.ajax = null;
	this.node = document.createElement("ul");
	this.inputNode = inputNode;
	this.init();
}

Suggest.prototype.updatePosition = function() {
	var rect = this.inputNode.getBoundingClientRect();
	this.node.style.left = rect.left + "px";
	this.node.style.top = rect.bottom + "px";
	this.node.style.width = (rect.right - rect.left) + "px";
}

Suggest.prototype.init = function() {
	this.node.className = "suggest";
	this.ajax = this.initAjax();
	this.setVisibility(false);
	var obj = this;
	this.inputNode.onkeyup = function() {
		obj.update(this.value);
	}
	this.inputNode.parentNode.appendChild(this.node);
};

Suggest.prototype.initAjax = function() {
	var ajax = null;
	if (window.XMLHttpRequest) {
		try {
			ajax = new XMLHttpRequest();
		}
		catch(e) {}
	}
	else if (window.ActiveXObject) {
		try {
			ajax = new ActiveXObject("Msxm12.XMLHTTP");
		}
		catch (e){
			try{
				ajax = new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch (e) {}
		}
	}
	return ajax;
}

Suggest.prototype.clear = function() {
	while (this.node.firstChild) this.node.removeChild(this.node.firstChild);
}

Suggest.prototype.hide = function() {
	this.clear();
	this.setVisibility(false);
}

Suggest.prototype.setVisibility = function(value) {
	this.node.style.display = value ? null : "none";
}

Suggest.prototype.showItems = function(list) {
	this.clear();
	if (list.length == 0) {
		this.setVisibility(false);
		return;
	}

	for (var i = 0; i < list.length; i++) {
		var widget = new SuggestItem(this, list[i]);
		this.node.appendChild(widget.node);
	}
	this.setVisibility(true);
	this.updatePosition();
}


Suggest.prototype.update = function(str) {
	if (!str) {
		this.hide();
		return;
	}
	var url = this.baseurl + str;
	this.ajax.open("GET", url);
	var obj = this;
	this.ajax.onreadystatechange = function() {
		if (this.readyState == 4) {
			var list = JSON.parse(this.responseText);
			obj.showItems(list);
		}
		else {
			obj.hide();
		}
	};
	this.ajax.send(null);
}

Suggest.prototype.set = function(item) {
	this.inputNode.value = item.str;
	this.hide();
}

var SuggestItem = function(suggest, item) {
	this.suggest = suggest;
	this.item = item;
	this.node = document.createElement("li");
	this.init();
};

SuggestItem.prototype.init = function() {
	this.node.appendChild(document.createTextNode(this.item.str));
	var obj = this;
	this.node.onclick = function() {
		obj.onclick();
	}
}

SuggestItem.prototype.onclick = function() {
	this.suggest.set(this.item);
}
