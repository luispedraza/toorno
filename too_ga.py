#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A simple genetic algorithm, based on: http://goo.gl/ykMPX
import random
import copy
import logging

DEFAULT_DAYS = 30
DEFAULT_SHIFTS = 3
DEFAULT_PEOPLE = 10

DEFAULT_POPULATION = 30
DEFAULT_MAXITER = 20

ALLELES = (False, True)

P_C = 0.8	# crossover prob.
P_M = 0.05	# mutation prob.


class Individual(object):
	# Init function
	def __init__(self, 
			ndays=DEFAULT_DAYS, 
			nshifts=DEFAULT_SHIFTS, 
			npeople=DEFAULT_PEOPLE, 
			chromosomes=None, ):
		self.ndays = ndays
		self.nshifts = nshifts
		self.npeople = npeople
		self.length_chromo = ndays*nshifts
		self.fitness = 0
		self.chromosomes = chromosomes or self.make_chromosomes()
		
	# Chromosomes random generation:
	def make_chromosomes(self):
		return [[random.choice(ALLELES) for gene in range(self.length_chromo)]
			for chromo in range(self.npeople)]
	# Fitness evaluation
	def evaluate(self, constraints):
		self.fitness = 0
		for i in range(self.npeople):
			for j in range(self.length_chromo):
				if not constraints.chromosomes[i][j] and self.chromosomes[i][j]:
					self.fitness -= 1
				else:
					self.fitness += 1
	# fornicación
	def crossover(self, couple, prob=P_C):
		if random.random() > prob:
			return self, couple
		cpoint = random.randrange(1, self.length_chromo)
		cross1 = copy.deepcopy(self.chromosomes)
		cross2 = copy.deepcopy(couple.chromosomes)
		for i in range(self.npeople):
			cross1[i][:cpoint] = couple.chromosomes[i][:cpoint]
			cross2[i][:cpoint] = self.chromosomes[i][:cpoint]
		return Individual(chromosomes=cross1), Individual(chromosomes=cross2)
	# rollo http://goo.gl/YXuqI
	def mutate(self, prob=P_M):
		for i in range(self.npeople):
			for j in range(self.length_chromo):
				if random.random() < prob:
					self.chromosomes[i][j] = not self.chromosomes[i][j]
		return self

class GeneticAlgorithm(object):
	def __init__(self, 
			ndays=DEFAULT_DAYS,
			nshifts=DEFAULT_SHIFTS,
			npeople=DEFAULT_PEOPLE,
			npop=DEFAULT_POPULATION,
			nmaxiter=DEFAULT_MAXITER,
			constraints=None):
		self.ndays=ndays
		self.nshifts=nshifts
		self.npeople=npeople
		self.npop = npop
		self.nmaxiter = nmaxiter
		self.niter = 0
		self.init_population()
		self.fitness = [0]*npop
		self.fitnessSum = [0]*npop
		self.fitnessBest = 0
		self.constraints = constraints or self.init_constraints()
	def roulette(self):
		nrand = random.random()*self.fitnessSum[-1]
		for i in range(self.npop):
			if self.fitnessSum[i] > nrand:
				return i
	def goal(self):
		return self.niter > self.nmaxiter
	def run(self):
		newpop = [None]*self.npop
		while not self.goal():
			self.compute_fitness()
			logging.info("*=============================*")
			logging.info("# iter: ", self.niter)
			logging.info("best: ", self.fitnessBest)
			for i in range(0, self.npop, 2):
				indi1 = self.population[self.roulette()]
				indi2 = self.population[self.roulette()]
				indi1, indi2 = indi1.crossover(indi2)
				indi1.mutate()
				indi2.mutate()
				newpop[i] = indi1
				newpop[i+1] = indi2
			self.population = newpop
			self.niter += 1
	def init_population(self):
		self.population = []
		for p in range(self.npop):
			self.population.append(Individual(
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
		self.fitnessBest = 0
		for i in range(self.npop):
			self.population[i].evaluate(self.constraints)
			self.fitness[i] = max(0, self.population[i].fitness)
			fitness_sum += self.fitness[i]
			self.fitnessSum[i] = fitness_sum
			if self.fitness[i] > self.fitnessBest:
				self.fitnessBest = self.fitness[i]
		return self.fitness

# Zona de pruebas
# gen = GeneticAlgorithm()
# gen.run()