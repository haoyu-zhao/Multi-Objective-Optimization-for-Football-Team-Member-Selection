# -*- coding: utf-8 -*-
"""
This is the open source code of the paper "Multi-Objective Optimization for Football Team Member Selection"
If you have any questions, please contact the author of the paper
"""

import pandas as pd
import copy
from populationInit import populationInit
from crossover import crossover
from mutation import mutation
from NSGA2Selection import NSGA2Selection
from NSGA2Selection import plotResult
from NSGA2Selection import get_GK
from NSGA2Selection import code2var
import matplotlib.pyplot as plt


data = pd.read_csv('fifa20player.csv')


populationSize = 400
generation = 300
pm = 0.1
pc = 0.7
eta_c = 10  
eta_m = 30 
budget = 10000 


population  = populationInit(populationSize,data,budget)
GK_tag,player_tag = get_GK(data)
minmax = [[1,len(player_tag)] for k in range(11)]
minmax[0] = [1,len(GK_tag)]

selectedPopulation = copy.deepcopy(population) 

for i in range(generation):
    offspring = crossover(selectedPopulation,pc)
    offspring = mutation(offspring,pm,eta_m,minmax)
    selectPopulation = selectedPopulation + offspring
    selectedPopulation,NDF_rank = NSGA2Selection(selectPopulation,populationSize,data,budget)
    print(i)
firstFront = [selectPopulation[j] for j in NDF_rank[0]]

best_solution = []
for i in selectedPopulation:
    if i not in best_solution:
        best_solution.append(i)
FF_solution = []
for i in firstFront:    
    if i not in FF_solution:
        FF_solution.append(i)
        
plotResult(selectPopulation,data,'b','.','Solution')
plotResult(best_solution,data,'r','^','Pareto Solution')
plt.legend()
plt.savefig('with150m.png', dpi = 500)


var_best = code2var(best_solution,data)
var_rand = code2var(population,data)
print(data.iloc[var_best[0]].mean())
print(data.iloc[var_rand[0]].mean())
