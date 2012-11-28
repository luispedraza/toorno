#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generación de gráficas de resultado con la librería pygal
import pygal 

def draw_chart(type="bar", title="", labels=[], xdata=[], ydata=[]):
	if type=="bar":
		chart = pygal.Bar()
	elif type=="line":
		chart = pygal.Line(show_dots=False)
	chart.title = title
	for i in range(len(labels)):
		chart.add(labels[i], ydata[i])
	
	return chart.render().decode('utf8')