# -*- coding: utf-8 -*-
"""
This is the open source code of the paper "Multi-Objective Optimization for Football Team Member Selection"
If you have any questions, please contact the author of the paper
"""

import random
import copy


def crossover(population,pc):
    populationSize = len(population)
   # random.shuffle(population)
    newPopulation = copy.deepcopy(population)
    x_num = len(population[0])
    for i in range(0,populationSize,2):
        if pc < random.random():
            continue
        for j in range(x_num):
            if random.random() >= 0.5:
                if population[i][j] in newPopulation[i+1] or population[i+1][j] in newPopulation[i]:
                    continue
                newPopulation[i][j] = population[i+1][j]
                newPopulation[i+1][j] = population[i][j]
                
        temp = newPopulation[i][2:]
        temp.sort()
        newPopulation[i][2:] = temp
        
        temp = newPopulation[i+1][2:]
        temp.sort()
        newPopulation[i+1][2:] = temp
    return newPopulation
