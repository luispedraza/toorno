#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A simple genetic algorithm, based on: http://goo.gl/ykMPX

## @package too_ga
# Optimización simple mediante Algoritmo Genético
#
# El paquete implementa clases y funciones para la opcimización 
# del problemas mediante la utilización de un algoritmo genético
# Cada undividuo representa una posible solución al problema
# utilizando la siguiente codificación cromosómica

import random
import copy
import logging

## Tamaño por defecto de la población del Genético
DEFAULT_POPULATION = 30
## Número máximo de iteraciones por defecto
DEFAULT_MAXITER = 20
## Posibles valores de un gen
ALLELES = (False, True)

## Probabilidad de cruce por defecto
P_C = 0.7
## Probabilidad de mutación por defecto
P_M = 0.01	# mutation prob.
## Opción elitista: los descendientes sustituyen a los padres cuando son mejores
ELITISM = True

## Cada uno de los individuos del algoritmo genético
# Su carga genética indica una solución de asignación propuesta
# Está implementado como una lista de DEFAULT_PEOPLE listas,
# cada una de las cuales es la asignación de días y turnos para
# una personas. Siendo d=persona, d=día, t=turno:
#	chromosomes: [	p_1[t_1_1,t_1_2,…,t_1_nshits,t_2_1,t_2_2,…,t_2_nshifts,…,t_ndays_1,t_ndays_2,…,t_ndays_nshifts],
#					p_2[t_1_1,t_1_2,…,t_1_nshits,t_2_1,t_2_2,…,t_2_nshifts,…,t_ndays_1,t_ndays_2,…,t_ndays_nshifts],
#					…
#					p_npeople[t_1_1,t_1_2,…,t_1_nshits,t_2_1,t_2_2,…,t_2_nshifts,…,t_ndays_1,t_ndays_2,…,t_ndays_nshifts],
#				]
class Individual(object):
	## El constructor de la clase
	# @param ndays Número de días del calendario
	# @param nshifts Número de turnos que hay que cubrir cada día
	# @param npeople Número de personas disponibles para cubrir los turnos
	# @param chromosomes El individuo puede ser inicializado con una carga genética
	def __init__(self, 
			ndays, 
			nshifts, 
			npeople, 
			chromosomes=None):
		self.ndays = ndays
		self.nshifts = nshifts
		self.npeople = npeople
		self.length_chromo = ndays*nshifts
		self.fitness = 0
		self.chromosomes = chromosomes or self.make_chromosomes()
		
	## Generación aleatoria de carga genética
	def make_chromosomes(self):
		return [[random.choice(ALLELES) for gene in range(self.length_chromo)]
			for chromo in range(self.npeople)]
	## Cálculo del desempeño del individuo.
	# Requiere indicar una estructura de restricciones
	# @param constraints Restricciones a emplear en el cálculo del fitness
	def evaluate(self, constraints):
		self.fitness = 0
		for i in range(self.npeople):
			for j in range(self.length_chromo):
				if not constraints.chromosomes[i][j] and self.chromosomes[i][j]:
					self.fitness -= 1
				else:
					self.fitness += 1
		self.fitness = max(1, self.fitness)	# ha de ser positivo, no nulo
		return self.fitness
	## Función de fornicación.
	# Cruza a un individuo con otro indicado como parámetro, con una cierta probabilidad
	# @param couple Individuo con el cuál realizar el cruce
	# @param prob Probabilidad de que el coito prospere :) 
	def crossover(self, couple, prob=P_C):
		if random.random() > prob:
			return self, couple
		cpoint = random.randrange(1, self.length_chromo)
		cross1 = copy.deepcopy(self.chromosomes)
		cross2 = copy.deepcopy(couple.chromosomes)
		for i in range(self.npeople):
			cross1[i][:cpoint] = couple.chromosomes[i][:cpoint]
			cross2[i][:cpoint] = self.chromosomes[i][:cpoint]
		return (Individual(ndays=self.ndays,nshifts=self.nshifts,npeople=self.npeople,chromosomes=cross1), 
			Individual(ndays=self.ndays,nshifts=self.nshifts,npeople=self.npeople,chromosomes=cross2))
	# rollo http://goo.gl/YXuqI
	def mutate(self, prob=P_M):
		for i in range(self.npeople):
			for j in range(self.length_chromo):
				if random.random() < prob:
					self.chromosomes[i][j] = not self.chromosomes[i][j]
		return self

## Clase sencilla que implementa un algoritmo genético
# para optimizar la asignación de turnos
#
# Los individuos de la población vienen modelados por la clase Individual
#
class GeneticAlgorithm(object):
	## El constructor de la clase algoritmo genético (GA)
	# @param ndays Número de días del mes de trabajo.
	# @param nshifts Número de turnos por día de trabajo.
	# @param npeople Número de personas que deben cubrir los turnos.
	# @param npop Tamaño de la población utilizada por el GA. Por defecto DEFAULT_POPULATION
	# @param nmaxiter Númer máximo de iteraciones. Por defecto DEFAULT_MAXITER
	# @param constraints Son las restricciones a utilizar. Si no se indican, la clase genera unas aleatorias
	def __init__(self, 
			ndays,
			nshifts,
			npeople,
			npop=DEFAULT_POPULATION,
			nmaxiter=DEFAULT_MAXITER,
			constraints=None):
		self.ndays = ndays
		self.nshifts = nshifts
		self.npeople = npeople
		if (npop%2):
			npop+=1	# debe ser un número par
		self.npop = npop
		self.nmaxiter = nmaxiter
		self.niter = 0
		self.init_population()
		self.fitness = [0]*npop
		self.fitness_sum = [0]*npop				# para selección por ruleta
		self.fitness_best = [0]*nmaxiter		# histórico de mejor fitness
		self.fitness_worst = [0]*nmaxiter		# histórico de peor fitness
		self.fitness_ranking = [0]*npop			# clasificación de individuos
		self.constraints = constraints or self.init_constraints()
	def roulette(self):
		nrand = random.random()*self.fitness_sum[-1]
		for i in range(self.npop):
			if self.fitness_sum[i] > nrand:
				return i
	def goal(self):
		return self.niter >= self.nmaxiter
	## Función principal de ejecución del algoritmo
	def run(self):
		newpop = [None]*self.npop
		self.niter = 0
		while not self.goal():
			self.compute_fitness()
			# Cruce y mutación:
			for i in range(0, self.npop, 2):
				if ELITISM and i<3: # dejamos pasar a la mejor pareja
					newpop[i] = copy.deepcopy(self.population[self.fitness_ranking[0][0]])
					newpop[i+1] = copy.deepcopy(self.population[self.fitness_ranking[1][0]])
				else:
					# elección de dos candidatos
					indi1 = copy.deepcopy(self.population[self.roulette()])
					indi2 = copy.deepcopy(self.population[self.roulette()])
					# cruce
					indi1, indi2 = indi1.crossover(indi2)
					# mutación
					indi1.mutate()
					indi2.mutate()
					newpop[i] = indi1
					newpop[i+1] = indi2
			self.population = newpop
			self.niter += 1
	def init_population(self):
		self.population = [None]*self.npop
		for p in range(self.npop):
			self.population[p] = (Individual(
				ndays=self.ndays,
				nshifts=self.nshifts,
				npeople=self.npeople))
		return self.population
	def init_constraints(self):
		# por el momento las restricciones se simulan
		# como un individuo que indica turnos válidos
		self.constraints = Individual(
				ndays=self.ndays,
				nshifts=self.nshifts,
				npeople=self.npeople)
		return self.constraints
	def compute_fitness(self):
		fitness_sum = 0
		for i in range(self.npop):
			self.fitness[i] = self.population[i].evaluate(self.constraints)
			self.fitness_ranking[i] = (i, self.fitness[i])
			fitness_sum += self.fitness[i]
			self.fitness_sum[i] = fitness_sum
		# construimos el ranking de individuos:
		self.fitness_ranking.sort(key=lambda indi: -indi[1])
		self.fitness_best[self.niter] = self.fitness_ranking[0][1]
		self.fitness_worst[self.niter] = self.fitness_ranking[-1][1]
		return self.fitness

# ndays= 30
# nshifts=2
# npeople=10
# npop=20
# nmaxiter=50
# ga = GeneticAlgorithm(ndays=ndays, nshifts=nshifts, npeople=npeople, npop=npop,nmaxiter=nmaxiter)
# ga.run()