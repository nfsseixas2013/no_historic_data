#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 09:30:16 2022

@author: nilton
"""
from Network import network
import Interface
import simpy
from Lightpath import lightpath
from RMSA_ILP import rmsa_ilp
'''

def test_get_links():
    env = simpy.Environment()
    topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
    switches = [2,3,4,5,7,8,9]
    actors = [1,6]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,1,'DL',1,6,traffic,net)
    slice1.get_links_candidates()
  #  print(slice1.links_candidates)

def test_links_ids():
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
  #  print(slice1.links_ids)
    
def test_links_costs():
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
   # print(slice1.links_costs)
    
    
def test_links_exp():
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,1,'DL',1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    print(slice1.links_candidates)
    print(slice1.links_ids)
    print(slice1.links_costs)
    
def test_fill_edp():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(ILP)
    print(ILP.sigma)

def test_fill_dpm():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(ILP)
    print(ILP.dpm)

    
def test_get_slice_indices():
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    print(slice1.get_slices_indices())
    
def test_get_slice_indices2():
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [60,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    print(slice1.get_slices_indices())
    
def test_get_slice_indices3():
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [40,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    print(slice1.get_slices_indices())
    
def test_fill_gama():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [40,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(ILP)
    print(ILP.gama)
    
def test_set_spectrum_01():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [40,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(ILP)
    print(slice1.links_ref[0][0].control[0])
    print(slice1.links_ref[0][0].control[1])

    
def test_set_spectrum_02():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0],100,ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0],100,ILP)
  #  print(slice1.links_ref[0][0].control[0])
  #  print(slice1.links_ref[0][0].control[1])

def test_set_spectrum_update():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0], 100,ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0], 100,ILP)
    ##
    slice2.path = 0
    slice2.modulation = 0
    slice2.update_connection(100)
  #  print(slice1.links_ref[0][0].control[0])
    #print(slice1.links_ref[0][0].control[1])


def test_ldp():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0],100,[50,200],ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0], 200,[50,200],ILP)
    ##
    slice2.path = 0
    slice2.modulation = 0
    slice2.update_connection(100)
    print(ILP.latencia)
    print(ILP.ldp)

def test_ILP_solver():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0],100,[50,200],ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0], 200,[50,200],ILP)
    ##
    slice2.path = 0
    slice2.modulation = 0
    slice2.update_connection(100)
    print(ILP.latencia)
    print(ILP.ldp)
    ILP.solver()
  
def test_ILP_solver_conf():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0],100,[50,200],ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0], 200,[50,200],ILP)
    ##
    slice2.path = 0
    slice2.modulation = 0
    slice2.update_connection(100)
    print(ILP.latencia)
    print(ILP.ldp)
    conf = ILP.solver()
    print(conf)
    

def test_conf_lightpath():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0],100,[50,200],ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0], 200,[50,200],ILP)
    ##
    slice2.path = 0
    slice2.modulation = 0
    slice2.update_connection(100)
    print(ILP.latencia)
    print(ILP.ldp)
    conf = ILP.solver()
    print(conf)
    Interface.setting_connections(conf,[slice1,slice2])
    #print("path: {} modulation: {}".format(slice1.path, slice1.modulation))
    print(slice2.links_ref[0][0].control[0])
    print("\n")
    print(slice2.links_ref[0][0].control[1])
    
def test_get_nodes():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.get_links_candidates()
    slice1.get_links_ids()
    slice1.get_links_costs()
    slice1.set_ILP(traffic[0],100,[50,200],ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.get_links_candidates()
    slice2.get_links_ids()
    slice2.get_links_costs()
    slice2.set_ILP(traffic[0], 200,[50,200],ILP)
    ##
    conf = ILP.solver()
    Interface.setting_connections(conf,[slice1,slice2])
    slice1.get_nodes_chosen()
    slice2.get_nodes_chosen()
    print(slice1.nodes[0].id)
    print(slice1.nodes[1].id)
    print(slice2.nodes[0].id)
    print(slice2.nodes[1].id)

def test_set_lightpath():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 2
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic,net)
    slice1.set_ILP(traffic[0],100,[50,200],ILP)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic,net)
    slice2.set_ILP(traffic[0], 200,[50,200],ILP)
    ##
    conf = ILP.solver()
    Interface.setting_connections(conf,[slice1,slice2])
    slice1.set_lightpaths()
    slice2.set_lightpaths()
    print(slice1.nodes[0].id)
    print(slice1.nodes[1].id)
    print("###")
    print(slice1.nodes[0].next_hopes[0][1].id)
    
def test_set_lightpath2():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 3
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    print(ILP.gama)
    print("\n")
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic1 = [60,10,10,10]
    traffic2 = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic1,net)
    slice1.set_ILP(traffic1[0],100,[50,200],ILP)
    print(ILP.gama)
    #
    slice2 = lightpath(env,1,[0,1],1,3,traffic2,net)
    slice2.set_ILP(traffic2[0], 200,[50,200],ILP)
    ##
    print("\n ")
    print(ILP.gama)
    conf = ILP.solver()
    print(conf)
    
'''

def test_set_lightpath2():
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 3
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    print(ILP.gama)
    print("\n")
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    traffic1 = [60,10,10,10]
    traffic2 = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic1,net)
    slice1.set_ILP(traffic1[0],100,ILP)
   
    slice2 = lightpath(env,1,[0,1],1,3,traffic2,net)
    slice2.set_ILP(traffic2[0], 200,ILP)
    ##
    conf = ILP.solver()
    print(conf)
    
def test_run():
    ## ILP ##
    qtd_demanda = 2
    qtd_links = 4
    qtd_path = 2
    qtd_channel = 1
    qtd_frequency_slot = 3
    qtd_modulacao = 2
    ILP = rmsa_ilp(qtd_demanda, qtd_links, qtd_path, qtd_channel, qtd_frequency_slot, qtd_modulacao)
    ###Setting NET #####
    env = simpy.Environment()
    topologia = [(1,2,5),(2,3,6),(1,4,7),(4,3,8)]
    switches = [2,4]
    actors = [1,3]
    frequency_slot = 0
    net = network(topologia,switches,actors,frequency_slot,env)
    ##### Setting lightpaths ######
    traffic1 = [60,10,10,10]
    traffic2 = [10,10,10,10]
    slice1 = lightpath(env,0,[0,1],1,3,traffic1,net)
    slice1.set_ILP(traffic1[0],100,ILP)
    ##
    slice2 = lightpath(env,1,[0,1],1,3,traffic2,net)
    slice2.set_ILP(traffic2[0], 200,ILP)
    #### Setting confs ####
    conf = ILP.solver()
    Interface.setting_connections(conf,[slice1,slice2])
   # env.run(until = 10)
    
    