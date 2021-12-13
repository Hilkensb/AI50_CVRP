#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import random
import copy
from collections import Counter

# Other Library
import numpy

def create_pop(pop, pop_size):
    """
    create_pop()
    
    Function to create a new population
    
    :param pop: List of customers
    :type pop: List[int]
    :param pop_size: Size of the population
    :param pop_size: int
    :return: New population
    :rtype: List of int
    """

    new_population = numpy.zeros((pop_size,len(pop)), dtype=int)
    for i in range(pop_size):
        random.shuffle(pop)
        new_population[i, :] = pop
    return new_population

def cal_pop_fitness(distance, pop):
    """
    cal_pop_fitness()
    
    Function to compute the fitness
    
    :param pop: Population of the GA
    :type pop: List[int]
    :param distance: Distance matrix
    :param distance: List[[int, int]]
    :return: List of fitness
    :rtype: List of int
    """

    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    fitness = numpy.zeros(len(pop[:,0]))
    for i in range(len(pop[:,0])):
        for j in range(len(pop[0,:])-1):
            fitness[i] += distance[pop[i,j],pop[i,j+1]]
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    """
    select_mating_pool()
    
    Selection function 
    
    :param pop: Population of the GA
    :type pop: List[int]
    :param fitness: Fitness of the population
    :type fitness: List[int]
    :param num_parents: Number of chromosome to select
    :type num_parents: int
    """

    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    fitness2 = fitness
    for parent_num in range(num_parents):
        min_fitness_idx = numpy.where(fitness2 == numpy.min(fitness2))
        min_fitness_idx = min_fitness_idx[0][0]
        parents[parent_num, :] = pop[min_fitness_idx, :]
        fitness2[min_fitness_idx] = 99999999999999
    return parents

def crossover(parents, offspring_size):
    """
    crossover()
    
    Crossover function
    
    :param parents: Population of the GA
    :type parents: List[int]
    :param offspring_size: Size of the childs
    :type offspring_size: Tuple[int]
    """

    offspring = numpy.empty((offspring_size[0],parents.shape[1]))
    #print("offspring_size : ", offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover, num_mutations=1):
    """
    mutation()
    
    Mutation function using swaps
    
    :param offspring_crossover: Population of the GA
    :type offspring_crossover: List[int]
    :param num_mutations: number of mutation to do
    :type num_mutations: int
    """
    
    for i in range(num_mutations):
        # Choose randomly the allele to mutate
        int_random_valeur = random.sample(population=list(range(len(offspring_crossover[1]))), k=2)

        # Choose randomly to add or remove one
        min_val=int(min(int_random_valeur))
        max_val=int(max(int_random_valeur))
        offspring_crossover[i, min_val], offspring_crossover[i, max_val] = offspring_crossover[i, max_val], offspring_crossover[i, min_val]

    return offspring_crossover
    
def correct(solution):
    """
    Function to correct an incorrect gene
    
    :param gene: gene to correct
    :type gene: np.ndarray
    :return: The corrected gene
    :rtype: np.ndarray
    """
    
    # Convert gene to list
    solution_list = solution.tolist()
    # Corrected gene
    corrected = copy.copy(solution_list)
    
    counter_nodes = Counter(solution_list)
    non_valid_cities = [
        city for city in counter_nodes.keys()
        if counter_nodes[city] > 1
    ]
    insert_cities = list(set(range(len(solution_list))) - set(solution_list)) 

    # While there's non 0 values index to look for
    while len(insert_cities) > 0:
        # Get the index of an object
        value_to_change = random.choice(non_valid_cities)
        index = corrected.index(value_to_change)
        counter_nodes[value_to_change] -= 1
        
        if counter_nodes[value_to_change] <= 1:
            non_valid_cities.remove(value_to_change)
        
        insert_value = random.choice(insert_cities)
        insert_cities.remove(insert_value)
        
        # Add the object if it's respecting the capacity constraints
        corrected[corrected.index(value_to_change)] = insert_value

    # Return the corrected one
    return numpy.array(corrected)

