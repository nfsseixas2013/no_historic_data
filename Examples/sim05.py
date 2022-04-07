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

args = [x for x in sys.argv]
args.pop(0)
# Constantes
# ILP
qtd_demanda = 11 * 3
qtd_links = 19
qtd_path = 2
qtd_channel = 1
qtd_frequency_slot = 800
qtd_modulacao = 2
# NET 
topology = [(1,2,10),(1,5,10),(2,3,20),(2,5,25),(3,4,10),(3,6,25),(4,6,10),(5,6,30),(7,1,5),(8,1,5),
            (9,1,5),(10,2,5), (11,2,5),(12,3,5), (13,3,5), (14,6,5), (15,6,5), (16,5,5), (17,5,5)]
switches = [1,2,3,5,6]
actors = [4,7,8,9,10,11,12,13,14,15,16,17]
frequency_slot = 0
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
#eMBB
slices_eMBB = []
lightpaths = []
destination = 7
node_source = 4
factor = 11
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
conf,cost = ILP.solver()
controller.init_energy(cost)
Interface.setting_connections(conf,lightpaths)
env.run(until = 600*144)



## Reports:
## Lightpaths:
main_data = lightpaths[0].get_reports()
for index in range(1,len(lightpaths)):
    main_data = pd.concat([main_data,lightpaths[index].get_reports()], axis = 0)
name = args[0]+"_Lightpaths.csv"

main_data.to_csv("/home/nilton/Arquivos/Resultados/MAX_IA_ULTRA/Lightpaths/"+name)

## Links
links_fragmentation = []
for link in net.links:
    links_fragmentation.append(np.mean(link.fragmentation))
name = args[0]+"_Fragmentation.csv"
fragmentation = [np.mean(links_fragmentation)]
dict_data = {'Fragmentation_mean': fragmentation}
data = pd.DataFrame(dict_data)
data.to_csv("/home/nilton/Arquivos/Resultados/MAX_IA_ULTRA/Links/"+name)
#
data2 = net.links[0].get_report()
for index in range(1,len(net.links)):
    data2 = pd.concat([data2,net.links[index].get_report()], axis = 0)
name = args[0]+"fragmentation_time.csv"
data2.to_csv("/home/nilton/Arquivos/Resultados/MAX_IA_ULTRA/Frag_time/"+name)

### Energy costs:
name = args[0]+"_energy_costs.csv"
controller.get_energy_costs().to_csv("/home/nilton/Arquivos/Resultados/MAX_IA_ULTRA/ILP/"+name)


