#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 10:34:48 2022

@author: nilton
"""
import Interface
import simpy
import numpy as np
import pandas as pd
from statistics import mean
class control:
    def __init__(self, env, net, ilp):
        self.lightpaths = []
        self.env = env
        self.net = net
        self.ilp = ilp
        self.flag = []
        self.connection = simpy.Store(env,capacity=simpy.core.Infinity)
        self.demands_size = 16
        self.conf = []
        self.energy = []
        
    def set_lightpaths(self,lightpath):
        self.lightpaths.append(lightpath)
    '''        
    def run(self):
        while True:
            for i in range(0,601):
                yield self.env.timeout(1)
            for j in self.lightpaths:
                j.action.interrupt()
            flag = []
            for j in self.lightpaths:
                flag.append(j.setup_predictions())
            yield self.env.timeout(0.000001)
            if False in flag:
                self.ilp.reset_ILP()
                self.smart_routing()
                yield self.env.timeout(0.000001)
                    
    '''
    ## Msg will have 3 fields: [False|True, Traffic_predicted, reference of lightpath]                 
    def smart_routing(self):
        self.ilp.reset_ILP()
        for i in self.net.links:
            #msg = ["reset"]
            #i.connection.put(msg)
            #yield i.env.process(i.get_msg())
            i.reset_control()
        for i in self.flag:
            i[2].set_ILP_update(i[1],i[2].latencia_required,self.ilp)
           # print(f"Lightpath :{i[2].id} -- slices: {i[2].slices}")

        self.conf,energy = self.ilp.solver()
        self.energy.append(energy)

        for i in self.lightpaths:
            i.action.interrupt()
        yield self.env.timeout(0.000001)
        #Interface.setting_connections_update(conf,self.lightpaths)
    
    def receive_msg(self,msg):
        msg = yield self.connection.get()
        self.flag.append(msg)
        if len(self.flag) == self.demands_size:
            for i in self.flag:
                if i[0] == False:
                    yield self.env.process(self.smart_routing())
                    break

            for link in self.net.links:
                link.get_fragmentation(self.env.now)
            self.flag.clear()
        yield self.env.timeout(0.000001)
        
    def init_energy(self, cost):
        self.energy.append(cost)
        
    def get_energy_costs(self):
        data = []
        data.append(mean(self.energy))
        dict_data = {'energy_cost': data}
        return pd.DataFrame(dict_data)
                
                
                
        
