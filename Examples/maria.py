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

# topology
topology = [(1,2,10),(2,3,10), (3,4,5)]
switches = [2,3] # optical transponders
actors = [1,4] # senders and receivers of lightpaths
frequency_slot = 2 # 0-> ultra-dense EON, 1 -> reduced EON, 2-> EON

# setting up ILP
qtd_demanda = 2 
qtd_links = len(topology)
qtd_path = 2
qtd_channel = 1
qtd_frequency_slot = 320 ## Quantity of frequency slots for EON
qtd_modulacao = 2

ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
# ENV
env = simpy.Environment()
# NET
net = network(topology,switches,actors,frequency_slot,env)
# IA module ##
brain = IA()
## Setting controller
controller = control(env,net,ILP)

source = 1
destination = 4
modulation = [0,1]

# Creating lightpaths
id_lightpath_1 = 0 # The id's must start with 0 and so on.
id_lightpath_2 = 1
traffic = [10] # poisson with lambda = 10 Gbps
service = 'eMBB'
parameter_of_evaluation = 'max' # max traffic value for adjustment
# brain is the IA for traffic prediction
# controller of network
# radio_block metric for blocked service related to functional splitting
lightpaths = []
latency_constraint = 0.00025

lightpath_1 = lightpath(env,id_lightpath_1,modulation,source,destination,traffic,net,service,parameter_of_evaluation, brain,controller, 'RADIO_BLOCK')
lightpath_2 = lightpath(env,id_lightpath_2,modulation,source,destination,traffic,net,service,parameter_of_evaluation, brain,controller, 'RADIO_BLOCK')

lightpath_1.set_ILP(traffic[0],latency_constraint,ILP)
lightpath_2.set_ILP(traffic[0],latency_constraint,ILP)

lightpaths.append(lightpath_1)
lightpaths.append(lightpath_2)

conf,cost = ILP.solver()
controller.init_energy(cost)
Interface.setting_connections(conf,lightpaths)
env.run(until = 50)

## Generation of report

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
