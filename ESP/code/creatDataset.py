#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the open source code of the paper "Multi-Objective Optimization for Football Team Member Selection"
If you have any questions, please contact the author of the paper
"""


import pandas as pd
import numpy as np
import os


read_path = '*Please enter your path here*'
os.chdir(read_path)
OriginData = pd.read_csv('players_20.csv')

OriginData = OriginData.fillna('0')

AttackAttributelist = ['ls','st','rs','lw','lf','cf','rf','rw','lam','cam','ram','lm','lcm','cm','rcm','rm']
DefendAttributelist = ['lwb','ldm','cdm','rdm','rwb','lb','lcb','cb','rcb','rb','lm','lcm','cm','rcm','rm']
GKAttributelist = ['goalkeeping_diving','goalkeeping_handling','goalkeeping_kicking','goalkeeping_positioning','goalkeeping_reflexes']

for i in AttackAttributelist:
    OriginData[i] = OriginData[i].apply(lambda x:x[:2])
for i in DefendAttributelist:
    OriginData[i] = OriginData[i].apply(lambda x:x[:2])

AttackAttribute = OriginData[AttackAttributelist]
DefendAttribute = OriginData[DefendAttributelist]
OriginData[AttackAttributelist] = OriginData[AttackAttributelist].astype('float')
OriginData[DefendAttributelist] = OriginData[DefendAttributelist].astype('float')
OriginData["attackscore"]=OriginData[AttackAttributelist].mean(axis=1)
OriginData["defencescore"]=OriginData[DefendAttributelist].mean(axis=1)

GKAttribute = OriginData[GKAttributelist]
OriginData[GKAttributelist] = OriginData[GKAttributelist].astype('float')
OriginData["GKscore"]=OriginData[GKAttributelist].mean(axis=1)

usingindex = ['short_name','overall','potential','wage_eur','attackscore','defencescore','player_positions','GKscore']
data_output = OriginData[usingindex]

data_output=data_output[~data_output['wage_eur'].isin([0])]

data_output.reset_index(drop = True,inplace = True)

data_output.to_csv('fifa20.csv')



