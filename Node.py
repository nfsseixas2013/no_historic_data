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
        #self.next_hopes = [] # It's like a routing table. It holds the next hopes of lightpaths. Format:
        # i[0] = lightpath_id, i[1] = node
    '''    
    def set_hopes(self, hope): # adding lightpaths next hopes
        self.next_hopes.append(hope)
    
    def get_next_hope(self,msg): # getting lightpaths next hopes
        for i in self.next_hopes: 
            if i[0] == msg[3]:
                return i[1]
            
    def get_link(self, hope):
        for i in self.links:
            if self in i.nodes and hope in i.nodes:
                return i
            
    def set_link(self, link): # Adding list of links to insert the traffic and get the cost of the link
        self.links.append(link)
    '''
    '''    
    def receive_msg(self): # That's a switch, therefore it must forward the bits through the circuits
        msg = yield self.connection.get()
        if msg[0] == 0:
            print('the bits of lightpath %d have been received at %f by node %d' % (msg[3], self.env.now, self.id))
            self.env.process(self.forwarding_msg(msg))
        elif msg[0] == 1: ## to add
            self.set_hopes(msg[1])
            msg[2].connection_nodes.put("reply_node")
            yield self.env.timeout(0.0000001)
        else: # to remove
            self.remove_item_next_hope(msg[1])
            msg[2].connection_nodes.put("reply_node")
            yield self.env.timeout(0.0000001)
    '''
    def receive_msg(self,cost): # That's a switch, therefore it must forward the bits through the circuits
        msg = yield self.connection.get()
        yield self.env.timeout(cost)
        print('the bits of lightpath %d have been received at %f by node %d' % (msg[2], self.env.now, self.id))
    
    
    '''        
    def forwarding_msg(self,msg):
        # Taking the next hope
        next_hope = self.get_next_hope(msg) # Getting the referenceof the next node
        link = self.get_link(next_hope)  # Getting the link
        yield self.env.timeout(link.cost) # 
        next_hope.connection.put(msg) # Put the message int the store of the next node.
        next_hope.env.process(next_hope.receive_msg()) # This is an interface. Must be implemented by the class Links
        link.add_traffic(self.env.now,msg[3]) # Adding traffic to the link
        
    def get_index_next_hope(self, id_cod):
        for i in range(0, len(self.next_hopes)):
            if self.next_hopes[i][0] == id_cod:
                return i
            
    def remove_item_next_hope(self, id_cod):
        del self.next_hopes[self.get_index_next_hope(id_cod)]
   '''     
        
        
        
