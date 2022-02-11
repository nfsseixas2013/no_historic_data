#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 10:34:48 2022

@author: nilton
"""
import Interface

class control:
    def __init__(self, env, net, ilp):
        self.lightpaths = []
        self.env = env
        self.net = net
        self.ilp = ilp
        self.env.process(self.run())
        
    def set_lightpaths(self,lightpath):
        self.lightpaths.append(lightpath)
        
    def run(self):
        while True:
            for i in range(0,601):
                yield self.env.timeout(1)
            for j in self.lightpaths:
                j.action.interrupt()
            flag = []
            for j in self.lightpaths:
                flag.append(self.smart_resize(j))
            yield self.env.timeout(0.000001)
            if False in flag:
                self.ilp.reset_ILP()
                self.smart_routing()
                yield self.env.timeout(0.000001)
                
                       
    def smart_resize(self, lightpath):
        return lightpath.setup_predictions()
    
    def smart_routing(self):
        for i in self.net.links:
            i.reset_control()
        for i in self.lightpaths:
            i.set_ILP_update(i.traffic_predicted,i.latencia_required,self.ilp)
        conf = self.ilp.solver()
        Interface.setting_connections_update(conf,self.lightpaths)