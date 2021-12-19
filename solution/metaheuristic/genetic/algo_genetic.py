#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import random
import copy
import json

# Other Library
import numpy

# Other Modules
import solution.metaheuristic.genetic.ga as ga
from gui.config import redis_server, SOLUTION_TOPIC
from utils.redisutils import isRedisAvailable


def genetic(
    number_conductor: int, number_node: int, vehicle_capacity: int,
    customer_demand: List[int], distance: List[int, int],
    topic: str = SOLUTION_TOPIC, sol_per_pop: int = 8, num_parents_mating: int = 4,
    num_generations: int = 20
):
    """
    genetic()
    
    Function to run the genetic algorithm
    
    :param number_conductor: Number of route to solve teh cvrp
    :type number_conductor: int
    :param number_node: Number of customerss
    :type number_node: int
    :param vehicle_capacity: Vehicle capacity
    :type vehicle_capacity: int
    :param customer_demand: Demands fo customer
    :type customer_demand: List[int]
    :param distance: Distance matrix
    :type distance: List[int, int]
    :param sol_per_pop: Solution per generation, default to 8 (opt.)
    :type sol_per_pop: int
    :param num_parents_mating: Number of chromosome to select per generation, default to 4 (opt.)
    :type num_parents_mating: int
    :param num_generations: Number of generation, default to 20 (opt.)
    :type num_generations: int
    :param topic: Redis topic, default to SOLUTION_TOPIC (opt.)
    :type topic: str
    """

    number_node_per_conductor = numpy.uint8(number_node/number_conductor)
    
    # Defining the population size.
    pop_size = (sol_per_pop, number_node) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.

    #Creating the initial population. numpy.zeros(pop_size, dtype=int)
    x = list(range(0,number_node))
    new_population = ga.create_pop(x, sol_per_pop)
    
    # List to store solution
    best_outputs = []
    best_sols = []

    # for every generation
    for generation in range(num_generations):
    
        # print("Generation : ", generation)
        # if redis is on
        if isRedisAvailable():
            # Create the data
            json_data = {
                "algorithm_name": "Genetic Algorithm", "cost": "",
                "iteration": generation,
                "graph": ""
            }
            # Publish
            redis_server.publish(topic, json.dumps(json_data))
        
        # Create a list for the fitness
        fitness = numpy.zeros(sol_per_pop)
        
        # Search for route
        for pop_local in range(sol_per_pop):
        
            population_copy = copy.copy(new_population[pop_local]).tolist()
            current_index = 0

            population_conducteur = numpy.empty(0)
            fitness_conductor = numpy.zeros(number_conductor)
            
            # Search the right order of customers in the route
            for i in range (number_conductor):
            
                # If there's no more customer
                if len(population_copy)==0:
                    continue

                # Create route
                population_conducteur = population_conducteur.tolist()
                population_copy, population_conducteur_temp = createSubRoute(population_copy, vehicle_capacity, customer_demand)
                population_conducteur.append(population_conducteur_temp)
                population_conducteur = numpy.array(population_conducteur, dtype=object)
                
                # 
                y = population_conducteur[-1]
                population_local = ga.create_pop(y, sol_per_pop)
                
                num_generation_local = 20
                for generation_local in range(num_generation_local):

                    # Measuring the fitness of each chromosome in the population.
                    fitness_local = ga.cal_pop_fitness(distance, population_local)
                    #print("fitness local : ", fitness_local)
                    
                    # Selecting the best parents in the population for mating.
                    parents_local = ga.select_mating_pool(population_local, fitness_local, num_parents_mating)
                    
                    # Generating next generation using crossover.
                    offspring_crossover_local = ga.crossover(parents_local, offspring_size=(pop_size[0]-parents_local.shape[0], number_node_per_conductor))
                    
                    # Adding some variations to the offspring using mutation.
                    # offspring_mutation = ga.mutation(offspring_crossover, num_mutations=2)
                    
                    # Creating the new population based on the parents and offspring.
                    population_local[0:parents_local.shape[0], :] = parents_local
                    population_local[parents_local.shape[0]:, :] = offspring_crossover_local
                
                fitness_conductor[i] = numpy.min(fitness_local)
                best_match_idx_local = numpy.where(fitness_local == numpy.min(fitness_local))

                #print("b : ",best_match_idx_local[0][0])
                population_conducteur[i]=population_local[best_match_idx_local[0][0],:]
                
                new_population[pop_local].tolist()[current_index:current_index+len(population_conducteur[i])] = population_conducteur[i]
                current_index+=len(population_conducteur[i])
               
            for index in range(len(new_population)):
                new_population[index] = ga.correct(new_population[index])

            # Measuring the fitness of each chromosome in the population.
            fitness[pop_local] = numpy.sum(fitness_conductor)

        best_outputs.append(numpy.min(fitness))
        best_fits_sols = [pop for pop in range(len(fitness)) if fitness[pop]==best_outputs[-1]]
        best_sols.append(new_population[best_fits_sols])
        # The best result in the current iteration.
        #print("Best result : ", numpy.min(numpy.sum(new_population*equation_inputs, axis=1)))
        
        # Selecting the best parents in the population for mating.
        parents = ga.select_mating_pool(new_population, fitness, num_parents_mating)
        # print("Parents")
        # print(parents)

        # Generating next generation using crossover.
        offspring_crossover = ga.crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], number_node))
        #print("Crossover")
        #print(offspring_crossover)

        # Adding some variations to the offspring using mutation.
        # offspring_mutation = ga.mutation(offspring_crossover, num_mutations=2)
        #print("Mutation")
        #print(offspring_mutation)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_crossover

    # Getting the best solution after iterating finishing all generations.
    #At first, the fitness is calculated for each solution in the final generation.
    fitness = ga.cal_pop_fitness(distance, new_population)
    # Then return the index of that solution corresponding to the best fitness.
    best_match_idx = numpy.where(fitness == numpy.min(fitness))
    
#    print("Best solution : ",  best_sols[best_outputs.index(numpy.min(best_outputs))])
#    print("Best solution fitness : ",numpy.min(best_outputs))
#    print("best outpout : ", best_outputs)

#    import matplotlib.pyplot
#    matplotlib.pyplot.plot(best_outputs)
#    matplotlib.pyplot.xlabel("Iteration")
#    matplotlib.pyplot.ylabel("Fitness")
#    matplotlib.pyplot.show()
    
    return numpy.min(best_outputs),  best_sols[best_outputs.index(numpy.min(best_outputs))][0].tolist()

def createSubRoute(population, vehicle_capacity, customer_demand):
    """
    createSubRoute()
    
    Function to create route from the population returned by the genetic algorithm
    
    :param population: Population generated by the genetic algorithm
    :type population: List[int]
    :param vehicle_capacity: Capacity of vehicles
    :type vehicle_capacity: int
    :param customer_demand: Demand of the customers
    :type customer_demand: List[int]
    :return: The updated population and the builded route
    :rtype: Tuple[List[SolutionCvrp], List[int]]
    """
    
    # The demand supplied
    demand_supplied: int = vehicle_capacity
    
    # Store teh customers
    result: List = []
    
    # Copy the population
    population_copy: List = copy.copy(population)

    # For every customers that are still in the population
    for customer in population:
        # If the capacity constraint is respected
        if (demand_supplied - customer_demand[customer] > 0):
            demand_supplied -= customer_demand[customer]
            # Add the customer to the route
            result.append(customer)
            population_copy.remove(customer)
            
    return population_copy, result

