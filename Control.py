#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 10:34:48 2022

@author: nilton
"""

class control:
    def __init__(self, env, net):
        self.lightpaths = []
        self.env = env
        self.net = net
        self.env.process(self.run())
        
    def set_lightpaths(self,lightpath):
        self.lightpaths.append(lightpath)
        
    def run(self):
        while True:
            for i in range(0,601):
                yield self.env.timeout(1)
            for j in self.lightpaths:
                j.action.interrupt()
                flag = self.smart_resize(j)
                yield self.env.timeout(0.000001)
                if flag == False:
                    self.smart_routing()
                    yield self.env.timeout(0.000001)
                    break
                       
    def smart_resize(self, lightpath):
        return lightpath.setup_predictions()
    
    def smart_routing(self):
        for i in self.net.links:
            i.reset_control()
        for i in self.lightpaths:
            i.set_ILP_update(i.self.traffic_predicted,i.latencia_required,self.ilp)
        