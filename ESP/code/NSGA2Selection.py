# -*- coding: utf-8 -*-
"""
This is the open source code of the paper "Multi-Objective Optimization for Football Team Member Selection"
If you have any questions, please contact the author of the paper
"""

import pandas as pd 
import copy
import matplotlib.pyplot as plt


def get_GK(data):
    GK_tag = data[data['attackscore']==0].index
    player_tag = data[data['attackscore']!=0].index
    return GK_tag,player_tag


def overallAvg(data,var_vector):
    index = [i for i in var_vector]
    overallAvg= data.iloc[index]['overall'].mean()
    return overallAvg


def potentialAvg(data,var_vector):
    index = [i for i in var_vector]
    potentialAvg = data.iloc[index]['potential'].mean()
    return potentialAvg


def attackScore(data,var_vector):
    index = [i for i in var_vector]
    index = index[1:]
    attackScore = data.iloc[index]['attackscore'].mean()
    return attackScore


def defenceScore(data,var_vector):
    index = [i for i in var_vector]
    index = index[1:]
    defenceScore = data.iloc[index]['defencescore'].mean()
    return defenceScore


def gkScore(data,var_vector):
    index = var_vector[0]
    gkScore = data.iloc[index]['GKscore']
    return gkScore

def constraintViolation(data,var_vector,budget):
    index = [i for i in var_vector]
    totalCost = data.iloc[index]['value_eur'].sum()/10000
    CV = max(0,(totalCost-budget)/budget)
    return CV




def constraintViolationSet(population,data,budget):
    populationSize = len(population)
    valueList=[0 for i in range(populationSize)]
    for i in range(populationSize):
        valueList[i]=constraintViolation(data,population[i],budget)
    return valueList
    


def code2var(code_population,data):
    populationSize = len(code_population)
    var_population = copy.deepcopy(code_population)
    GK,PL = get_GK(data)
    for i in range(populationSize):
        for j in range(11):
            if j== 0:
                var_population[i][j] = GK[code_population[i][j]-1]
            else:
                var_population[i][j] = PL[code_population[i][j]-1]
    return var_population


def objectiveValueSet(population,fun,data):
    populationSize = len(population)
    valueList=[0 for i in range(populationSize)]
    for i in range(populationSize):
        valueList[i]=fun(data,population[i])
    return valueList



def constraint_NDSort(population,populationSize,data,budget):

    objectiveValue = []
    
    overallAvgList=objectiveValueSet(population,overallAvg,data)
    objectiveValue.append(overallAvgList)
    
    potentialAvgList=objectiveValueSet(population,potentialAvg,data)
    objectiveValue.append(potentialAvgList)
    
    attackScoreList=objectiveValueSet(population,attackScore,data)
    objectiveValue.append(attackScoreList)
    
    defenceScoreList=objectiveValueSet(population,defenceScore,data)
    objectiveValue.append(defenceScoreList)
    
    constraintViolationList = constraintViolationSet(population, data, budget)
    gkScoreList=objectiveValueSet(population,gkScore,data)
    objectiveValue.append(gkScoreList)
    
    dominateList=[[] for i in range(populationSize)]
    
    dominatedNumList=[0 for i in range(populationSize)]
    
    for i in range(populationSize):
        ai = [objectiveValue[k][i] for k in range(len(objectiveValue))]
        for j in range(populationSize):
            if j == i:
                continue
            aj = [objectiveValue[k][j] for k in range(len(objectiveValue))]
            if constraintViolationList[i] == 0 and  constraintViolationList[j] > 0:
                dominateList[i].append(j)
                continue
            elif constraintViolationList[i] > 0 and  constraintViolationList[j] == 0:
                dominatedNumList[i] += 1
                continue
            elif constraintViolationList[i] > 0 and constraintViolationList[j] > 0:
                if constraintViolationList[i] < constraintViolationList[j]:
                    dominateList[i].append(j)
                    continue
                else:
                    dominatedNumList[i] += 1
                    continue
            less = 0 
            equal = 0 
            greater = 0
            for k in range(len(ai)):
                if aj[k] < ai[k]:
                    less += 1
                elif aj[k] > ai[k]:
                    greater += 1
                else:
                    equal += 1
            if greater == 0 and less != 0:
                dominateList[i].append(j)
            elif less == 0 and greater != 0:
                dominatedNumList[i] += 1
                
    NDF_rank=[0 for i in range(populationSize)]
    NDFSet=[]
    rank = 1
    front = [i for i,x in enumerate(dominatedNumList) if x == 0] 
    NDFSet.append(front)
    for i in front:
        NDF_rank[i] = rank
    while True:
        front = []
        for i in NDFSet[rank-1]:
            for j in dominateList[i]:
                dominatedNumList[j] -= 1
                if dominatedNumList[j] == 0:
                    front.append(j)
        if len(front) == 0:
            break
        rank += 1
        NDFSet.append(front)
        for k in front:
            NDF_rank[k] = rank                      
    return NDF_rank,NDFSet

def crowdedDistance(population,Front,data):
    distance=pd.Series([float(0) for i in range(len(Front))], index=Front)
    FrontSet=[]
    for i in Front:
        FrontSet.append(population[i])

    objectiveValue = []
    overallAvgList = objectiveValueSet(FrontSet,overallAvg,data)
    potentialAvgList = objectiveValueSet(FrontSet,potentialAvg,data)
    attackScoreList = objectiveValueSet(FrontSet, attackScore, data)
    defenceScoreList = objectiveValueSet(FrontSet, defenceScore, data)
    gkScoreList = objectiveValueSet(FrontSet, gkScore, data)
    
    objectiveValue.append(overallAvgList)
    objectiveValue.append(potentialAvgList)
    objectiveValue.append(attackScoreList)
    objectiveValue.append(defenceScoreList)
    objectiveValue.append(gkScoreList)
    
    minmax = [[] for i in range(len(objectiveValue))]
    for i in range(len(objectiveValue)):
        minmax[i] = [min(objectiveValue[i]),max(objectiveValue[i])]
        
    overallAvgSer = pd.Series(overallAvgList,index=Front)
    potentialAvgSer = pd.Series(potentialAvgList,index=Front)
    attackScoreSer = pd.Series(attackScoreList,index=Front)
    defenceScoreSer = pd.Series(defenceScoreList,index=Front)
    gkScoreSer = pd.Series(gkScoreList,index=Front)

    overallAvgSer.sort_values(ascending=False,inplace=True)
    potentialAvgSer.sort_values(ascending=False,inplace=True)
    attackScoreSer.sort_values(ascending=False,inplace=True)
    defenceScoreSer.sort_values(ascending=False,inplace=True)
    gkScoreSer.sort_values(ascending=False,inplace=True)

    distance[overallAvgSer.index[0]]=10000
    distance[overallAvgSer.index[-1]]=10000
    distance[potentialAvgSer.index[0]]=10000
    distance[potentialAvgSer.index[-1]]=10000
    distance[attackScoreSer.index[0]]=10000
    distance[attackScoreSer.index[-1]]=10000
    distance[defenceScoreSer.index[0]]=10000
    distance[defenceScoreSer.index[-1]]=10000
    distance[gkScoreSer.index[0]]=10000
    distance[gkScoreSer.index[-1]]=10000
    
    for i in range(1,len(Front)-1):
        distance[overallAvgSer.index[i]]+=(overallAvgSer[overallAvgSer.index[i-1]]-overallAvgSer[overallAvgSer.index[i+1]])/(minmax[0][1]-minmax[0][0])
        distance[potentialAvgSer.index[i]]+=(potentialAvgSer[potentialAvgSer.index[i-1]]-potentialAvgSer[potentialAvgSer.index[i+1]])/(minmax[1][1]-minmax[1][0])
        distance[attackScoreSer.index[i]]+=(attackScoreSer[attackScoreSer.index[i-1]]-attackScoreSer[attackScoreSer.index[i+1]])/(minmax[2][1]-minmax[2][0])
        distance[defenceScoreSer.index[i]]+=(defenceScoreSer[defenceScoreSer.index[i-1]]-defenceScoreSer[defenceScoreSer.index[i+1]])/(minmax[3][1]-minmax[3][0])
        distance[gkScoreSer.index[i]]+=(gkScoreSer[gkScoreSer.index[i-1]]-gkScoreSer[gkScoreSer.index[i+1]])/(minmax[4][1]-minmax[4][0])
       
    distance.sort_values(ascending=False,inplace=True)
    return distance

def crowdedCompareOperator(population,populationSize,NDFSet,data):
    newPopulation=[]
    var_popu = code2var(population, data)
    count=0
    number=0
    while count<populationSize:            
        if count + len(NDFSet[number])<=populationSize:
            if number==0:
                fFront = NDFSet[number]
            for i in NDFSet[number]:
                newPopulation.append(population[i])
            count += len(NDFSet[number])
            number+=1
        else:
            if number==0:
                fFront=NDFSet[number]
            n=populationSize-count
            distance=crowdedDistance(var_popu,NDFSet[number],data)
            for i in range(n):
                newPopulation.append(population[distance.index[i]])
            number+=1
            count+=n
    return newPopulation
  

def NSGA2Selection(population,populationSize,data,budget):
    var_population = code2var(population,data)
    NDF_rank,NDFSet=constraint_NDSort(var_population,populationSize*2,data,budget)
    newPopulation=crowdedCompareOperator(population,populationSize,NDFSet,data)
    return newPopulation,NDFSet

def plotResult(code_population,data,color,marker = '*',label = ''):
    var = code2var(code_population, data)
    defenceScoreList=objectiveValueSet(var, defenceScore,data)
    attackScoreList=objectiveValueSet(var,attackScore,data)
    
    x = [-i for i in defenceScoreList]
    y = [-i for i in attackScoreList]
    plt.scatter(x, y, color=color, marker=marker,label = label)
    plt.xlabel('Defence Score',fontdict={'size':12})
    plt.ylabel('Attack Score',fontdict={'size':12})