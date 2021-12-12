#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 12:54:08 2021

@author: stephane
"""
import numpy
import solution.metaheuristic.genetic.ga as ga
import random
import copy


number_conductor = 5
number_node = 50

#Create random distance matrixe
distance = numpy.random.uniform(low=10, high=50, size=(number_node,number_node))
distance[0,0]=0
for i in range(number_node):
    for j in range(i):
        distance[i,i]=0
        distance[i,j]=distance[j,i]






"""
Genetic algorithm parameters:
    Mating pool size
    Population size
"""






def genetic(number_conductor, number_node, vehicle_capacity, customer_demand, distance, sol_per_pop = 8, num_parents_mating = 4):
    number_node_per_conductor = numpy.uint8(number_node/number_conductor)
    
    # Defining the population size.
    pop_size = (sol_per_pop, number_node) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.

    #Creating the initial population. numpy.zeros(pop_size, dtype=int)
    x = list(range(0,number_node))
    new_population = ga.create_pop(x, sol_per_pop)

    print(new_population)
    
    """
    new_population[0, :] = [2.4,  0.7, 8, -2,   5,   1.1]
    new_population[1, :] = [-0.4, 2.7, 5, -1,   7,   0.1]
    new_population[2, :] = [-1,   2,   2, -3,   2,   0.9]
    new_population[3, :] = [4,    7,   12, 6.1, 1.4, -4]
    new_population[4, :] = [3.1,  4,   0,  2.4, 4.8,  0]
    new_population[5, :] = [-2,   3,   -7, 6,   3,    3]
    """
    best_outputs = []
    best_sols = []
    num_generations = 20
    for generation in range(num_generations):
        print("Generation : ", generation)
        fitness = numpy.zeros(sol_per_pop)
        for pop_local in range(sol_per_pop):
        
            population_copy = copy.copy(new_population[pop_local]).tolist()
            current_index = 0

            population_conducteur = numpy.empty(0)
            fitness_conductor = numpy.zeros(number_conductor)
            for i in range (number_conductor):
                if len(population_copy)==0:
                    continue

                population_conducteur = population_conducteur.tolist()
                population_copy, population_conducteur_temp = createSubRoute(population_copy, vehicle_capacity, customer_demand)
                population_conducteur.append(population_conducteur_temp)
                population_conducteur = numpy.array(population_conducteur)
                
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
                new_population[index] = ga.correct(new_population[i])

            # Measuring the fitness of each chromosome in the population.
            fitness[pop_local] = numpy.sum(fitness_conductor)
            # print("Fitness")
            # print(fitness)
                

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
    """
    
    # The demand supplied
    demand_supplied: int = vehicle_capacity
    
    # Store teh customers
    result: List = []
    
    # Copy the population
    population_copy: List = copy.copy(population)

    for customer in population:
        if (demand_supplied - customer_demand[customer] > 0):
            demand_supplied -= customer_demand[customer]
            result.append(customer)
            population_copy.remove(customer)
            
    return population_copy, result

