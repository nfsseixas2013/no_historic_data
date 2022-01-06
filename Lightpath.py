#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:08:21 2021

@author: nilton
"""

import numpy as np
import Interface

class lightpath:
    
    def __init__(self, env, cod, mode, source, destination, traffic, net):
        self.id = cod
        self.nodes = []
        self.mode = mode
        self.channel_size = 0
        self.source = source
        self.destination = destination
        self.conf = []
        self.env = env
        self.report = []
        self.traffic = traffic
        self.connection = False
        ## parameters of ilp
        self.links_candidates = []
        self.links_ids = []
        self.links_costs = []
        self.links_ref = []
        self.slices = []
        self.net = net
        self.traffic_predicted = traffic[0] ## depois mudar isso
       # self.env.process(self.run())
       
        
    #### Preparations to get ILP parameters
    def get_links_candidates(self): # It returns format [(1,2),(2,3)]
        self.links_candidates = Interface.get_nodes_candidates(self.net,self.source, self.destination)
        
    def get_links_ids(self): # The purpose is get the ids of the links to fill edp constant in the ILP
        links_ids = []
        for i in self.links_candidates:
            aux = []
            for j in i:# list of list
               aux.append(Interface.get_link_id(j,self.net))
            links_ids.append(aux)
        self.links_ids = links_ids # We get the links separeted by path candidate
    
    def get_links_costs(self): # This function returns the cost per path. The function in the interface must change 
        for i in self.links_candidates:
            self.links_costs.append(Interface.get_cost(i,[0,1],self.net))
            
    def get_links_refs(self):## getting the links objects to calculate teh template
        self.links_ref = Interface.get_links_ref_list(self.links_candidates,self.net)
    
    def get_slices_indices(self):## This function returns the interval of slices candidates
        self.get_links_refs()
        number_slots = []
        templates = []
        for i in self.mode:
            number_slots.append(Interface.get_number_slots(self.traffic_predicted,i,self.net)) # number of slots per modulation
        for i in self.links_ref:
            aux = []
            for j in self.mode:
                aux.append(Interface.get_template(i,j))
            templates.append(aux)
        slices = []
        for i in templates:
            indice = 0
            aux = []
            for j in i:
               end = Interface.test_allocation(j,number_slots[indice])
               start = end-number_slots[indice]+1
               aux.append([start,end+1])
               indice += 1
            slices.append(aux)
        self.slices = slices
        return slices
                
       
    def set_ILP(self,ILP): # Incomplete. Need to set the spectrum.
        self.get_links_candidates()
        self.get_links_ids()
        self.get_links_costs()
        self.get_slices_indices()
        for p in range(0,len(self.links_candidates)):
            Interface.fill_links(self.links_ids[p],[self.id],[p],ILP)
            Interface.fill_dpm([self.id],[p],self.mode,self.links_costs[p],ILP)
            Interface.fill_gama([self.id],[p],[0],self.mode,[self.slices[p]],ILP)
            
#########################################################################################################################
            
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
