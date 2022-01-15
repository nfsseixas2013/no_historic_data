
from Network import network
import Interface
import simpy
from RMSA_ILP import rmsa_ilp
from Lightpath import lightpath

'''
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

def test_get_link_ref_lists():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
    switches = [2,3,4,5,7,8,9]
    actors = [1,6]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,1,'DL',1,6,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    print(Interface.get_links_ref_list(slice1.links_candidates,net))

def test_get_template():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
    switches = [2,3,4,5,7,8,9]
    actors = [1,6]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,1,'DL',1,6,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    links = Interface.get_links_ref_list(slice1.links_candidates,net)
    template = Interface.get_template(links[0],0)
    print(template)
    
def test_allocation():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
    switches = [2,3,4,5,7,8,9]
    actors = [1,6]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,1,'DL',1,6,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    links = Interface.get_links_ref_list(slice1.links_candidates,net)
    template = Interface.get_template(links[0],0)
    print(Interface.test_allocation(template,Interface.get_number_slots(60,0,net)))
'''    

def test_get_template():
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic1 = [60,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic1,net)
    slice1.get_links_candidates()
    slice1.get_links_refs()
    slice1.get_links_ids()
    slice1.get_links_costs()
    template = slice1.get_templates()
    for i in template:
        print(i.template[0][1])
                       #      # link
        print("\n \n \n")
    


def test_get_template2():
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic1 = [60,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic1,net)
    slice1.get_links_candidates()
    slice1.get_links_refs()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slices = slice1.get_slices_indices(100)
    print(slice1.links_ref[0][0].shadow[1])
    print("\n \n ******** \n ")
    print(slices)
