#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:08:21 2021

@author: nilton
"""

import numpy as np

class lightpath:
    
    def __init__(self, env, cod, interface, mode, source, destination, traffic):
        self.id = cod
        self.nodes = []
        self.interface = interface
        self.mode = mode
        self.channel_size = 0
        self.source = source
        self.destination = destination
        self.conf = []
        self.env = env
        self.report = []
        self.traffic = traffic
        self.connection = False
        self.env.process(self.run())
       
        
    def set_lightpaths(self):
        for i in range(0, len(self.nodes)-1):
            self.nodes[i].set_hopes([self.id, self.nodes[i+1]])
    
    def get_nodes(self): # It receives (1,2), (2,3) -> [1,2,2,3] -> [1,2,3] * Nodes references
        for i in self.conf[2]: # This conf delivers the exact order of nodes.
            self.nodes.append(i)
       
            
              
    def establish_link(self, need): # It uses the interface to set the lightpath spectrum
        self.conf = self.interface.establish_lightpath(self.source, self.destination, need, self.mode, self.id)
        if self.conf == None:
            return False
        else:
            self.get_nodes()
            self.set_lightpaths()
            self.channel_size = self.conf[1]
            return True
        
    def update_lightpath(self, need): # It clears the list of nodes and clears the spectrum
        self.nodes.clear()
        self.interface.clean_lightpath(self.id, self.conf[0])
        return self.establish_link(need)
    
    def sending(self,load): # Modularization of sending of one msg
        msg = [self.env.now,"bytes", self.id, load]
        self.nodes[0].connection.put(msg)
        self.nodes[0].env.process(self.nodes[0].forwarding_msg(msg)) ## Formarding not receive # Lightpath just send.
        self.report.append([self.env.now, load])
        yield self.env.timeout(self.conf[0][0].cost) 
        
    def sending_traffic(self, load): 
        if not self.connection:
            self.connection = self.establish_link(load)
            if self.connection:
                 self.env.process(self.sending(load))
            else:
                self.report.append([self.env.now, 0])
        else:
            slot_available = self.interface.get_number_slots(self.channel_size, self.mode)
            slot_needed = self.interface.get_number_slots(load, self.mode)
            if slot_available - slot_needed > 0:
                self.connection = self.update_lightpath(load)
                self.env.process(self.sending(load))
                  
            elif slot_available - slot_needed < 0:
                 self.connection = self.update_lightpath(load)
                 if self.connection:
                     self.env.process(self.sending(load))
                 else:
                     self.report.append([self.env.now, 0])
            else:
                self.env.process(self.sending(load))
          
    def run(self):
        if type(self.traffic) == list: 
            for i in self.traffic:
                self.sending_traffic(i)
                yield self.env.timeout(1)
        else:
            while True:
               self.sending_traffic(np.random.poisson(self.traffic,1)[0]) 
                
                