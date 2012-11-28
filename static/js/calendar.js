window.addEventListener("load", initToos, false);

function initToos() {
	toos = document.getElementsByClassName("too");
	console.log(toos);
	for (i=0; i<toos.length; i++) {
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

