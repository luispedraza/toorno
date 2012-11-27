#!/usr/bin/env python
# -*- coding: utf-8 -
## @package too_simulator
# Implementa funcionalidades para probar los algoritmos de optimización:
# - too_ga para optimización mediante algoritmo genético

from too_base import *
from too_ga import *		# algoritmo genético
from too_charts import *	# generación de gráficas
from too_calendar import *
from calendar import monthrange


class Simulator(BaseHandler):
	def get(self):
		self.render("test.html")
	def post(self):
		year=int(self.request.get("year"))
		month=int(self.request.get("month"))
		nshifts=int(self.request.get("shifts"))
		ndays=calendar.monthrange(year,month)[1]
		npeople=int(self.request.get("people"))
		npop=int(self.request.get("npop"))
		nmaxiter=int(self.request.get("nmaxiter"))
		ga = GeneticAlgorithm(ndays=ndays,
			nshifts=nshifts,
			npeople=npeople,
			npop=npop,
			nmaxiter=nmaxiter)
		ga.run()
		chart = draw_chart(type="line",
			title="Simulation results",
			labels=["Best", "Worst"],
			ydata=[ga.fitnessBest, ga.fitnessWorst])		
		#calendar=get_calendar_html(year, month, shifts)
		self.render("test.html",
			chart_fitness=chart,
			#calendar=calendar
			)