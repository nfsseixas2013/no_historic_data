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
import numpy as np
from Split import split

args = [x for x in sys.argv]
args.pop(0)


# NET 
topology = [(1,2,10),(1,5,10),(2,3,20),(2,18,15),(3,4,10),(3,18,15),(4,6,10),(5,6,30), (6,18,15), (5,18,15),(7,1,5),(8,1,5),
            (9,1,5),(10,2,5), (11,2,5),(12,3,5), (13,3,5), (14,6,5), (15,6,5), (16,5,5), (17,5,5)]
switches = [1,2,3,5,6]
actors = [4,7,8,9,10,11,12,13,14,15,16,17,18]
frequency_slot = 0
# Constantes
# ILP
qtd_demanda = 11 * 4 # 11 from eMBB, 11 from mMTC, 11 from URLLC and 11 from the split of URLLC
qtd_links = len(topology)
qtd_path = 2
qtd_channel = 1
qtd_frequency_slot = 800
qtd_modulacao = 2

# Traffic indexes
indexes = [4452, 4653, 5061, 5160, 5162, 5262, 5458, 5758, 5955, 5956, 6064] # duplicando os dois últimos

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
#eMBB######
slices_eMBB = []
lightpaths = []
RU = 7
CU = 4
factor = 11
DU = 18
i = 0
while i < factor:
   new = lightpath(env,i,[0,1],CU,RU,traffic_eMBB[i],net,'eMBB','max', brain,controller, 'RADIO_BLOCK')
   new.set_ILP(traffic_eMBB[i][0],0.00025,ILP)
   slices_eMBB.append(new)
   lightpaths.append(new)
   i += 1
   RU += 1
##########
### URLLC ###
slices_URLLC = []
i = 0

while i < factor:
    new = lightpath(env,i+factor,[0,1],CU,DU,traffic_URLLC[i],net,'URLLC','max', brain,controller,'SLA_VIOLATION')
    new.set_ILP(traffic_URLLC[i][0],0.002,ILP)
    slices_URLLC.append(new)
    lightpaths.append(new)
    i += 1

i = 0
RU = 7
indice = 11
while i < factor:
    new = split(env,i+(2*factor),[0,1],DU,RU,traffic_URLLC[i],net,'URLLC','max', brain,controller,'RADIO_BLOCK')
    new.set_ILP(traffic_URLLC[i][0],0.00025,ILP)
    slices_URLLC.append(new)
    lightpaths.append(new)
    lightpaths[indice].set_splits(new)
    i += 1
    RU += 1
    indice += 1
###############

    
slices_mMTC = []
i = 0
RU = 7
while i < factor:
    new = lightpath(env,i+(factor*3),[0,1],CU,RU,traffic_mMTC[i],net,'mMTC','max', brain,controller,'SLA_VIOLATION')
    new.set_ILP(traffic_mMTC[i][0],0.00025,ILP)
    slices_mMTC.append(new)
    lightpaths.append(new)
    i += 1
    RU += 1
    
## 
conf,cost = ILP.solver()
controller.init_energy(cost)
Interface.setting_connections(conf,lightpaths)
env.run(until = 600*144)



## Reports:
## Lightpaths:
dir = "/home/nilton/Arquivos/Resultados/MAX_NOT_HISTORIC/"
main_data = lightpaths[0].get_reports()
for index in range(1,len(lightpaths)):
    main_data = pd.concat([main_data,lightpaths[index].get_reports()], axis = 0)
name = args[0]+"_Lightpaths.csv"

main_data.to_csv(dir+"Lightpaths/"+name)

## Links
links_fragmentation = []
for link in net.links:
    links_fragmentation.append(np.mean(link.fragmentation))
name = args[0]+"_Fragmentation.csv"
fragmentation = [np.mean(links_fragmentation)]
dict_data = {'Fragmentation_mean': fragmentation}
data = pd.DataFrame(dict_data)
data.to_csv(dir+"Links/"+name)
#
data2 = net.links[0].get_report()
for index in range(1,len(net.links)):
    data2 = pd.concat([data2,net.links[index].get_report()], axis = 0)
name = args[0]+"fragmentation_time.csv"
data2.to_csv(dir+"Frag_time/"+name)

### Energy costs:
name = args[0]+"_energy_costs.csv"
controller.get_energy_costs().to_csv(dir+"ILP/"+name)

##
main_data2 = lightpaths[0].get_reports_2()
for index in range(1,len(lightpaths)):
    main_data2 = pd.concat([main_data2,lightpaths[index].get_reports_2()], axis = 0, sort=True)
name = args[0]+"_Interruptions.csv"
main_data2.to_csv(dir+"Interruptions/"+name)

data_decision = controller.get_time_decision()
name = args[0]+"_Time_decision.csv"
data_decision.to_csv(dir+"Time_Decision/"+name)


