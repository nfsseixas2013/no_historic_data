
from Network import network
import Interface
import simpy
from RMSA_ILP import rmsa_ilp
def test_get_candidates():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10)]
    switches = [2,3,4]
    actors = [1,5]
    frequency_slot = 0 # 5GHz
    net = network(topologia,switches,actors,frequency_slot,env)
    print (Interface.get_nodes_candidates(net,1,5))


def test_get_candidates2():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (1,6,5),(6,7,10), (7,5,10)]
    switches = [2,3,4,6,7]
    actors = [1,5]
    frequency_slot = 0 # 5GHz
    net = network(topologia,switches,actors,frequency_slot,env)
    print (Interface.get_nodes_candidates(net,1,5))
    
    
def test_get_candidates3():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
    switches = [2,3,4,5,7,8,9]
    actors = [1,6]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    print (Interface.get_nodes_candidates(net,1,6))
    

def test_get_candidates4():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
    switches = [2,3,4,5,7,8,9]
    actors = [1,6]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    links = Interface.get_nodes_candidates(net,1,6)
    print(Interface.get_weight_links(net, links))
    
def test_ILP():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    print(ILP.mdl)
    
def test_ILP_FILLING_sigma():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    Interface.fill_links([0,1],[0],[0], ILP)
    print(ILP.sigma)
    
def test_ILP_FILLING_gama():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    Interface.fill_gama([0],[0],[0],[0,1],[[(0,2),(0,1)]],ILP)
    Interface.fill_gama([0],[1],[0],[0,1],[[(0,2),(0,1)]],ILP)
    print(ILP.gama)
    
def test_ILP_FILLING_dpm():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    Interface.fill_dpm([0],[0],[0,1],[20,30], ILP)
    Interface.fill_dpm([0],[1],[0,1],[30,40], ILP)
    print(ILP.dpm)
