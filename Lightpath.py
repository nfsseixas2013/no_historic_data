#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:08:21 2021

@author: nilton
"""
import simpy
import numpy as np

class lightpath:
    
    def __init__(self, env, cod, interface, mode, source, destination, traffic):
        self.id = cod
        self.nodes = None
        self.interface = interface
        self.mode = mode
        self.channel_size = 0
        self.source = source
        self.destination = destination
        self.conf = None
        self.env = env
        self.report = []
        self.traffic = traffic
        self.connection = False
        self.env.process(self.run())
       
         
    def set_lightpaths(self, nodes):# It receives a set of nodes and set the next hopes.
        # ex. node1, node2, node3 -> node1.set_nodes(node2), node2.set_hope(node3)
        for i in range(0, len(nodes) -1):
            nodes[i].set_hopes(nodes[i+1])
    
    def get_nodes(self, links): # It receives (1,2), (2,3) -> [1,2,2,3] -> [1,2,3] * Nodes references
        result = []
        for i in links:
            result.append(i.nodes[0])
            result.append(i.nodes[1])
        return set(result)
            
              
    def establish_link(self, need): # It uses the interface to set the lightpath spectrum
        self.conf = self.interface.establish_lightpath(self.source, self.destination, need, self.mode, self.id)
        if self.conf == None:
            return False
        else:
            self.nodes = self.get_nodes(self.conf[0])
            self.set_lightpaths(self.nodes)
            self.channel_size = self.conf[1]
            return True
        
    def update_lightpath(self, need): # It clears the list of nodes and clears the spectrum
        self.nodes.clear()
        self.interface.clean_lightpath(self.id, self.conf[0])
        return self.establish_link(need)
    
    def sending_msg(self,i): # Modularization of sending of one msg
        msg = [self.env,"bytes", self.id, i]
        self.nodes[0].connection.put(msg)
        self.nodes[0].env.process(self.nodes[0].forwarding(msg)) ## Formarding not receive # Lightpath just send.
        self.report.append([self.env, i])
        yield self.env.timeout(self.conf[0][0].cost) 
        
    def sending_traffic(self, i): # Trick one, trying a connection doesn't mean you succeeded having it.
        if not self.connection:
            self.connection = self.establish_link(i)
     
        elif self.connection:
            if i <= self.channel_size:
                self.sending_msg(i)
            else:
                self.connection = self.update_lightpath(i)
                if self.connection:
                   self.sending_msg(i)
                else:
                   self.report.append([self.env, 0])
                  
        else:
            self.report.append([self.env, 0])
          
    def run(self):
        if type(self.traffic) == list: 
            for i in self.traffic:
                self.sending_traffic(i)
                yield self.env.timeout(1)
        else:
            while True:
               self.sending_traffic(np.random.poisson(self.traffic,1)[0]) 
                
                