var Suggest = function(inputNode, tree) {
	this.tree = tree;
	this.ajax = ajax();
	this.node = document.createElement("ul");
	this.inputNode = inputNode;
}

Suggest.prototype.ajax = function() {
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
	while (this.node.firstChild) this.removeChild(this.node.firstChild);
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
		var item = list[i];
		var li = document.createElement("li");
		li.appendChild(document.createTextNode(item.str));
		this.node.appendChild(li);
	}
	this.setVisibility(true);
}

Suggest.update = function(str) {
	if (!str) {
		this.hide();
		return;
	}
	var url = "suggest?mode=json&size=20&str=" + str;
	if (this.tree) url += "&tree=" + this.tree;
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
//	this.ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	this.ajax.send(null);
}

