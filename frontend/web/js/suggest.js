var Suggest = function(inputNode, baseurl) {
	this.baseurl = baseurl;
	this.ajax = null;
	this.node = document.createElement("ul");
	this.inputNode = inputNode;
	this.init();
}

Suggest.prototype.init = function() {
	this.node.className = "suggest";
	this.ajax = this.initAjax();
	var obj = this;
	this.inputNode.onkeyup = function() {
		obj.update(this.value);
	}
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
		var item = list[i];
		var li = document.createElement("li");
		li.appendChild(document.createTextNode(item.str));
		this.node.appendChild(li);
	}
	this.setVisibility(true);
}


Suggest.prototype.update = function(str) {
	console.log(str);
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

