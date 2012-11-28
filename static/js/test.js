window.addEventListener("load", initCalendarPagination, false);

currentCalendar = 0
totalCalendars = 0
solutions = []
function initCalendarPagination() {
	solutions = document.getElementsByClassName("calendar")
	if (solutions.length) {
		totalCalendars = solutions.length
		document.getElementById("control").style.display="block"
		solutions[0].style.display="block"
		document.getElementById("prev-cal").addEventListener("click",
			function(e) {
				changeCalendar(e,-1)
			})
		document.getElementById("next-cal").addEventListener("click",
			function(e) {
				changeCalendar(e,1)
			})
	}
}

function changeCalendar(event, inc) {
	solutions[currentCalendar].style.display = "none"
	currentCalendar += inc
	if (currentCalendar==totalCalendars)
		currentCalendar = 0
	else if (currentCalendar<0)
		currentCalendar=totalCalendars-1
	solutions[currentCalendar].style.display = "block"
}