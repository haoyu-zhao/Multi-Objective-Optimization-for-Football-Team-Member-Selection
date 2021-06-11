# -*- coding: utf-8 -*-
"""
This is the open source code of the paper "Multi-Objective Optimization for Football Team Member Selection"
If you have any questions, please contact the author of the paper
"""
import random
import copy

def get_GK(data):
    GK_tag = data[data['attackscore']==0]['Tag']
    player_tag = data[data['attackscore']!=0]['Tag']
    return GK_tag,player_tag

def mutation(population, pm, eta_m, minmax):
    populationSize = len(population)
    newPopulation = copy.deepcopy(population)
    x_num = len(population[0])
    
    for i in range(populationSize):
        for j in range(x_num):
            r=random.random()
            y=population[i][j]
            if r<=pm:
                ylow,yup = minmax[j]
                delta1=1.0*(y-ylow)/(yup-ylow)
                delta2=1.0*(yup-y)/(yup-ylow)
                #delta=min(delta1, delta2)
                r=random.random()
                mut_pow=1.0/(eta_m+1.0)
                if r<=0.5:
                    xy=1.0-delta1
                    val=2.0*r+(1.0-2.0*r)*(xy**(eta_m+1.0))
                    deltaq=val**mut_pow-1.0
                else:
                    xy=1.0-delta2
                    val=2.0*(1.0-r)+2.0*(r-0.5)*(xy**(eta_m+1.0))
                    deltaq=1.0-val**mut_pow
                y=y+deltaq*(yup-ylow)
                y=round(y)
                y=min(yup, max(y, ylow))
                if y in newPopulation[i]:
                    continue
                newPopulation[i][j]=y
                
        temp = newPopulation[i][1:]
        temp.sort()
        newPopulation[i][1:] = temp
        
    return newPopulation                