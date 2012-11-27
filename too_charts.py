#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generación de gráficas de resultado con la librería pygal
import pygal 

def draw_chart(title="", labels=[], data=[]):
	bar_chart = pygal.Bar()                                            # Then create a bar graph object
	bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
	return bar_chart.render().decode('utf8')