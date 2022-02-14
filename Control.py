#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 10:34:48 2022

@author: nilton
"""
import Interface
import simpy

class control:
    def __init__(self, env, net, ilp):
        self.lightpaths = []
        self.env = env
        self.net = net
        self.ilp = ilp
        self.flag = []
        self.connection = simpy.Store(env,capacity=simpy.core.Infinity)
        self.demands_size = 14 * 3
        self.conf = []
        
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
            i.reset_control()
        for i in self.flag:
            i[2].set_ILP_update(i[1],i[2].latencia_required,self.ilp)
        self.conf = self.ilp.solver()
        for i in self.lightpaths:
            i.action.interrupt()
        self.flag.clear()
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
        yield self.env.timeout(0.000001)
        
                
                
                
        