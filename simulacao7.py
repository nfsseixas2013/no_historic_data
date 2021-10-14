#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 16:11:16 2021

@author: nilton
"""
from Network import network
from Interface import interface
from Lightpath import lightpath
import simpy
# topologia:
# 1-2, 2-3, 3-4. Todos os pesos iguais
env = simpy.Environment()
topologia = [(1,2,5),(2,3,10), (3,5,10), (2,4,15),(4,5,10),(1,4,10)]
switches = [2,3,4]
actors = [1,5]
frequency_slot = 0 # 5GHz

net = network(topologia,switches,actors,0,env)
rsa = interface(net)

traffic = [31000,31000,31000,31000]
traffic2 = [1000,1000,2000,2000]

slice1 = lightpath(env,1,rsa,'DL',1,5,traffic)
slice2 = lightpath(env,2,rsa,'DL',1,5,traffic2)

env.run(until = 4)

#print(slice1.report)
#print(net.links[0].traffic)
