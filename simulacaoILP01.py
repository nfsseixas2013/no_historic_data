#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:11:13 2022

@author: nilton
"""
#import numpy as np
from Network import network
import Interface
import simpy
from Lightpath import lightpath
from RMSA_ILP import rmsa_ilp





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
    env.run(until = 1000)
    print(slice1.report)

test_run()