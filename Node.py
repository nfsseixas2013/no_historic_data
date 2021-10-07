#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:16:34 2021

@author: nilton
"""

# OBS - MSG format is (env.now, string message, lightpath ip, load (gigabits))
import simpy
# Verify if it is needed to import class link
class node:
    def __init__(self, cod, env):
        self.id = cod # id for the node
        self.connection = simpy.Store(env,capacity=simpy.core.Infinity) # Table for consumption of msgs
        self.links = [] # Ref. to links which the node connects to.
        self.env = env 
        self.next_hopes = [] # It's like a routing table. It holds the next hopes of lightpaths. Format:
        # i[0] = lightpath_id, i[1] = node
        
    def set_hopes(self, hope): # adding lightpaths next hopes
        self.next_hopes.append(hope)
    
    def get_next_hope(self,msg): # getting lightpaths next hopes
        for i in self.next_hopes: 
            if i[0] == msg[2]: # i[0] = lightpath_id, i[1] = node
                return i
            
    def get_link(self, hope):
        for i in self.links:
            if self in i.nodes and hope in i.nodes:
                return i
            
    def set_link(self, link):
        self.links.append(link)
        
    def receive_msg(self):
        msg = yield self.connection.get()
        print('the bits of lightpath %d have been received at %f by node %d' % (msg[2], self.env.now, self.id))
        self.forwarding_msg(msg)
        
    def forwarding_msg(self,msg):
        # Taking the next hope
        next_hope = self.get_next_hope(msg) 
        link = self.get_link(next_hope)  
        next_hope.connection.put(msg) # Put the message int the store of the next node.
        next_hope.env.process(next_hope.receive_msg(msg)) # This is an interface. Must be implemented by the class Links
        link.add_traffic(self.env.now,msg[3])
        yield self.env.timeout(link.cost)
        
        
        