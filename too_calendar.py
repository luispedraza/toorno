#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import re
from xml.dom import minidom
CAL = calendar.HTMLCalendar()

days = ["noday", "mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def get_calendar():
	# obtengo el html del calendario
	cal_html = 	CAL.formatmonth(2012, 11)
	# limpio el html:
	cal_html = re.sub("&nbsp;|\n", "", cal_html)
	# creamos el árbol dom
	dom = minidom.parseString(cal_html)
	days = dom.getElementsByTagName("td")
	for day in days:
		if day.getAttribute("class") != "noday":
			day_id = "day-"+day.firstChild.nodeValue
			day.setAttribute("id", day_id)
			toos = dom.createElement("div")
			toos.setAttribute("class", "toos")
			day.appendChild(toos)
			for i in ["too-1", "too-2", "too-3"]:
				too = dom.createElement("div")
				too.setAttribute("id", day_id+"_" + i)
				too.setAttribute("class", "too "+i)
				txt = dom.createTextNode("")
				too.appendChild(txt) 
				toos.appendChild(too)
	return dom.toprettyxml()



