# -*- coding: utf-8 -*-
"""
This is the open source code of the paper "Multi-Objective Optimization for Football Team Member Selection"
If you have any questions, please contact the author of the paper
"""
import random


def get_GK(data):
    GK_tag = data[data['attackscore']==0].index
    player_tag = data[data['attackscore']!=0].index
    return GK_tag,player_tag


def constraintViolation(data,var_vector,budget):
    index = [i for i in var_vector]
    totalCost = data.iloc[index]['value_eur'].sum()/10000
    CV = max(0,(totalCost-budget)/budget)
    return CV


def populationInit(populationSize,data,budget):
    GK_tag,player_tag = get_GK(data)
    population = [[] for i in range(populationSize)]
    count = 0
    while count < populationSize:
        code_vector = [0 for k in range(11)]
        var_vector = [0 for k in range(11)]
        GK_num = len(GK_tag)
        player_num = len(player_tag)
        code_vector[0] = random.randint(1, GK_num)
        temp = random.sample(range(1,player_num), 10)
        temp.sort()
        code_vector[1:] = temp
        for j in range(11):
            if j== 0:
                var_vector[j] = GK_tag[code_vector[j]-1]
            else:
                var_vector[j] = player_tag[code_vector[j]-1]
        if constraintViolation(data, var_vector, budget) == 0:
            population[count] = code_vector
            count += 1
    return population