window.addEventListener("load", init, false);

function init() {
	toos = document.getElementsByClassName("too");
	console.log(toos);
	for (i=0; i<toos.length; i++) {
		console.log("tetas");
		toos[i].addEventListener("click", tooClicked)
	}
}

function tooClicked() {
	if (hasClass(this, "selected")) {
		removeClass(this, "selected");
	}
	else {
		addClass(this, "selected");
	}	
}


// Funciones auxiliares
function hasClass(ele,cls) {
	return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}
 
function addClass(ele,cls) {
	if (!hasClass(ele,cls)) ele.className += " "+cls;
}
 
function removeClass(ele,cls) {
	if (hasClass(ele,cls)) {
    	var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
		ele.className=ele.className.replace(reg,' ');
	}
}