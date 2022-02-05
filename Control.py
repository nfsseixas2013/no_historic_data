#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 10:34:48 2022

@author: nilton
"""

class control:
    def __init__(self, env):
        self.lightpaths = []
        self.env = env
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
                # To activate the routing
                
                
    def smart_resize(self, lightpath):
        return lightpath.setup_predictions()
        