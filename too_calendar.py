#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import re
from xml.dom import minidom
CAL = calendar.HTMLCalendar()

days = ["noday", "mon", "tue", "wed", "thu", "fri", "sat", "sun"]

## Generación de HTML para un calendario
def get_calendar_html(year, month, shifts, prefs=[], schedule=[]):
	# obtengo el html del calendario
	cal_html = 	CAL.formatmonth(year, month)
	# limpio el html:
	cal_html = re.sub("&nbsp;|\n", "", cal_html)
	# creamos el árbol dom
	dom = minidom.parseString(cal_html)
	days = dom.getElementsByTagName("td")
	shift_id = 0	# utilizados si prefs y schedule
	for day in days:
		if day.getAttribute("class") != "noday":
			day_id = "day-"+day.firstChild.nodeValue
			day.setAttribute("id", day_id)
			toos = dom.createElement("div")
			toos.setAttribute("class", "toos")
			day.appendChild(toos)
			toos_list = [("too-"+str(i)) for i in range(1,shifts+1)]
			for t in toos_list:
				too_class = "too "+t
				too_text = ""
				if prefs:
					if prefs[shift_id]:
						too_class = too_class +" selected"
					elif schedule:
						if schedule[shift_id]:
							too_class = too_class + " error"
				if schedule:
					if schedule[shift_id]:
						too_text = "X"
				
				too = dom.createElement("div")
				too.setAttribute("id", day_id+"_" + t)
				too.setAttribute("class", too_class)
				txt = dom.createTextNode(too_text)
				too.appendChild(txt) 
				toos.appendChild(too)
				shift_id += 1
	return dom.toprettyxml()



