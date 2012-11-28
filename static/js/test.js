window.addEventListener("load", initCalendarPagination, false);

currentCalendar = 0
totalCalendars = 0
solutions = []
numbers = []
function initCalendarPagination() {
	solutions = document.getElementsByClassName("calendar")
	numbers = document.getElementsByClassName("bnumber")
	if (solutions.length) {
		totalCalendars = solutions.length
		document.getElementById("control").style.display="block"
		selectCalendar(0)
		document.getElementById("prev-cal").addEventListener("click",
			function(e) {
				changeCalendar(e,-1)
			})
		document.getElementById("next-cal").addEventListener("click",
			function(e) {
				changeCalendar(e,1)
			})
		for (n=0; n<numbers.length; n++) {
			numbers[n].addEventListener("click", selectCalendar)
		}
	}
}

function changeCalendar(e, inc) {
	calendar = currentCalendar + inc
	if (calendar==totalCalendars)
		calendar = 0
	else if (calendar<0)
		calendar=totalCalendars-1
	selectCalendar(calendar)
}

function selectCalendar(number) {
	if (typeof number != 'number')
		number = parseInt(this.innerHTML)
	solutions[currentCalendar].style.display = "none"
	numbers[currentCalendar].style.fontSize = "1em"
	currentCalendar = number
	solutions[currentCalendar].style.display = "block"
	numbers[currentCalendar].style.fontSize = "1.5em"
}