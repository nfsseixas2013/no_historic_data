#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:15:48 2022

@author: nilton
"""

import sys
sys.path.append("../")

from Network import network
import Interface
import simpy
from RMSA_ILP import rmsa_ilp
from Lightpath import lightpath
import pandas as pd
from IA.IA import IA
from Control import control
import pandas as pd

# Constantes
# ILP
qtd_demanda = 14 * 3
qtd_links = 22
qtd_path = 2
qtd_channel = 1
qtd_frequency_slot = 800
qtd_modulacao = 2
# NET 
topology = [(1,2,10),(1,5,10),(2,3,20),(2,5,25),(3,4,10),(3,6,25),(4,6,10),(5,6,30),(7,1,5),(8,1,5),
            (9,1,5),(10,1,5), (11,2,5),(12,2,5),(13,2,5),(14,2,5),(15,3,5),(16,3,5),(17,3,5),(18,3,5),
            (19,6,5),(20,5,5)]
switches = [1,2,3,5,6]
actors = [4,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
frequency_slot = 0
# Traffic indexes
indexes = [5161, 5059, 5262, 5758, 5162, 5061, 5956, 6064, 5458, 5259, 4452, 5161,4452,5160]# duplicando os dois últimos

## Traffic
ds = pd.read_csv("../Examples/traffic_sim.csv")
def get_traffic(data,indice,lista,kind):
    if kind == 'eMBB':
        return list(ds[ds['Square_id'].isin([lista[indice]])]['eMBB'])
    elif kind == 'mMTC':
        return list(ds[ds['Square_id'].isin([lista[indice]])]['mMTC'])
    else:
        return list(ds[ds['Square_id'].isin([lista[indice]])]['URLLC'])

traffic_eMBB = []
for i in range(0, len(indexes)):
    traffic = get_traffic(ds,i,indexes,'eMBB')
    traffic_eMBB.append(traffic)
traffic_URLLC = []
for i in range(0, len(indexes)):
    traffic = get_traffic(ds,i,indexes,'URLLC')
    traffic_URLLC.append(traffic)
traffic_mMTC = []
for i in range(0, len(indexes)):
    traffic = get_traffic(ds,i,indexes,'mMTC')
    traffic_mMTC.append(traffic)

## Setting Up sim
# ILP
ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
# ENV
env = simpy.Environment()
# NET
net = network(topology,switches,actors,frequency_slot,env)
# IA module ##
brain = IA()
## Setting controller
controller = control(env,net,ILP)

## Setting slices:
#eMBB
slices_eMBB = []
lightpaths = []
destination = 7
node_source = 4
factor = 14
i = 0
while i < factor:
   new = lightpath(env,i,[0,1],node_source,destination,traffic_eMBB[i],net,'eMBB','max', brain,controller)
   new.set_ILP(traffic_eMBB[i][0],0.002,ILP)
   slices_eMBB.append(new)
   lightpaths.append(new)
   i += 1
   destination += 1

slices_URLLC = []
i = 0
destination = 7
while i < factor:
    new = lightpath(env,i+factor,[0,1],node_source,destination,traffic_URLLC[i],net,'URLLC','max', brain,controller)
    new.set_ILP(traffic_URLLC[i][0],0.00025,ILP)
    slices_URLLC.append(new)
    lightpaths.append(new)
    i += 1
    destination += 1
    
slices_mMTC = []
i = 0
destination = 7
while i < factor:
    new = lightpath(env,i+(factor*2),[0,1],node_source,destination,traffic_mMTC[i],net,'mMTC','max', brain,controller)
    new.set_ILP(traffic_mMTC[i][0],0.002,ILP)
    slices_mMTC.append(new)
    lightpaths.append(new)
    i += 1
    destination += 1
    
## 
conf = ILP.solver()
Interface.setting_connections(conf,lightpaths)
env.run(until = 600*144)


