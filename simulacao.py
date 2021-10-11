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
topologia = [(1,2,10),(2,3,10), (3,4,10)]
switches = [2,3]
actors = [1,4]
frequency_slot = 0 # 5GHz

net = network(topologia,switches,actors,0,env)
rsa = interface(net)

traffic = [10,10,10,10]

slice1 = lightpath(env,1,rsa,'DL',1,4,traffic)

env.run(until = 4)

