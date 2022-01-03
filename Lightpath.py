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
        for i in range(0, len(self.nodes)-1): # Setting the circuit in the nodes.
            self.nodes[i].set_hopes([self.id, self.nodes[i+1]])
   ''' 
    def get_nodes(self): # It receives (1,2), (2,3) -> [1,2,2,3] -> [1,2,3] * Nodes references
        for i in self.conf[2]: # This conf delivers the exact order of nodes.
            self.nodes.append(i)
       
            
              
    def establish_link(self, need): # It uses the interface to set the lightpath spectrum, the nodes and teh channel size
        self.conf = self.interface.establish_lightpath(self.source, self.destination, need, self.mode, self.id)
        if self.conf == None:
            return False
        else:
            self.get_nodes()
            self.set_lightpaths()
            self.channel_size = self.conf[1]
            return True
        
    def update_lightpath(self, need): # It clears the list of nodes and the spectrum ocuppied by the lightpath
        for i in range(0, len(self.nodes) - 1): # The destination does not forward!
            self.nodes[i].remove_item_next_hope(self.id)
        self.nodes.clear()
        self.interface.clean_lightpath(self.id, self.conf[0])
        return self.establish_link(need)
    
    def sending(self,load): # Modularization of sending of one msg
        msg = [self.env.now,"bytes", self.id, load] # Setting msg
        self.nodes[0].connection.put(msg) # Putting the msg in the store of the nodes
        self.nodes[0].env.process(self.nodes[0].forwarding_msg(msg)) ## Formarding not receive # Lightpath just send.
        self.report.append([self.env.now, load]) # Reporting
        yield self.env.timeout(self.conf[0][0].cost) # getting the cost of the transmission
        
    def sending_traffic(self, load): 
        if not self.connection: # Getting connection when there isn't one
            self.connection = self.establish_link(load)
            if self.connection: # It must be tested if it succeeded.
                 self.env.process(self.sending(load)) # I have to create other process. Investigate why...
            else:
                self.report.append([self.env.now, 0])
        else: # There's connection
            slot_available = self.interface.get_number_slots(self.channel_size, self.mode) 
            slot_needed = self.interface.get_number_slots(load, self.mode)
            if slot_available - slot_needed > 0: # It has slot lefting over
                self.connection = self.update_lightpath(load)
                self.env.process(self.sending(load))
                  
            elif slot_available - slot_needed < 0: # There's a lack of slots
                 self.connection = self.update_lightpath(load)
                 if self.connection:
                     self.env.process(self.sending(load))
                 else:
                     self.report.append([self.env.now, 0])
            else: # The needed and the available are the same
                self.env.process(self.sending(load))
          
    def run(self):
        if type(self.traffic) == list: # Modelling of traffic
            for i in self.traffic:
                self.sending_traffic(i)
                yield self.env.timeout(1)
        else:
            while True: # # Using poisson to model the traffic
               self.sending_traffic(np.random.poisson(self.traffic,1)[0]) 
                
   '''             
