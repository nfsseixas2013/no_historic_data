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