#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 19:31:00 2021

@author: nilton
"""

import networkx as nx
import itertools as it

class interface:
    
    def __init__(self, net):
        self.net = net
        
    def get_nodes_candidates(self, source, destination): # we will work with 2 paths for now...
        # source and destinations are nodes... Let's work with references (pointer style)
        # 
        return list(it.islice(nx.all_shortest_paths(self.net.graph, source, destination), 2))
        # it most return the list of ids of nodes
        
    def nodes2links(self,path): # PRIVATE 
        # The goal of this method is return list of links of the same path. Ex. [x,y,z]->[(x,y), (y,z)]
        result = []
        for i in range(0, len(path)-1):
            result.append((path[i],path[i+1]))
        return result
    
    def get_links_candidates(self, source, destination):
        # The goal of this method is call recursively the method nodes2links to transform all candidate nodes
        # in tuples of links. Ex. [[x,y,z], [a,b,c]]->[[(x,y), (y,z)], [(a,b), (b,c)]]
        nodes_ref = self.get_nodes_candidates(source, destination)
        paths = []
        for i in nodes_ref:
            paths.append(self.nodes2links(i))
        return paths
    
    def get_nodes_object(self, link):# link is a tuple Ex. (1,2)
        # This method gets the nodes objects referenced by a link 
        nodes = []
        for i in self.net.nodes:
            if i.id == link[0] or i.id == link[1]:
                nodes.append(i)      
        return nodes
    
    def get_link_object(self, node1, node2):
        # With the 2 nodes of a link, we can get the link object
        for i in self.net.links:
            if node1 in i.nodes and node2 in i.nodes:
                return i
    
    def get_all_links_objects(self,source, destination):
        # This is a recursive method that gets [(1,2),(2,3)],[(5,6),(6,7)] -> [[link1, link2],[link3, link4]]
        # We get every link of path candidates
        paths =  self.get_links_candidates(source, destination)
        result = []
        for i in paths:
            aux = []
            for j in range(0, len(i)):
                nodes = self.get_nodes_object(i[j]) # We get the nodes
                link = self.get_link_object(nodes[0], nodes[1]) # We get the link
                aux.append(link) # We add the links of the ṕath
            result.append(aux) # here we add the entire path of links
        return result
            
    ## So far, we got all objects of links candidates to test if there is spectrum space to allocate the demand.
    # Now, we run tests 
            
    def test_path(self, links): # It receives a list of links and return a template of use of the spectrum
        resposta = []
        for i in range(0, len(links[0].control)):# Every link.control has the same size.
            flag = 0
            for j in links:
                if j.control[i][2] == 1:
                    resposta.append(1)
                    flag = 1
                    break
            if flag == 0:
                resposta.append(0)
        return resposta  # This answer will hold a template of the state of the network. 
    
    def test_allocation(self, template, slot_numbers):
        # This method verifies if the the template has the necessary number of frequency slots to hold the requisition
        counter = 0
        for i in range(0, len(template)):
            if template[i] == 0:
                counter += 1
                if counter == slot_numbers:
                    break
            else:
                counter = 0
        if counter == slot_numbers:
            return i # if there's space, then this method should deliver the end **
        else:
            return -1
        
    def get_number_slots(self, need, mode): # need in Gbps
        # This method returns the number of slots needed to establish the lightpath.
        slot_type = self.net.links[0].size # In this case, I know the modulation for DL is 256 qam and for UL is 64 Qam 
        if slot_type == 0: # 5GHz
            if mode == "DL":
                slot_size = 40
            else:
                slot_size = 30
        elif slot_type == 1: # 6GHz
            if mode == "DL":
                slot_size = 48
            else:
                slot_size = 36
        else:
            if mode == "DL":
                slot_size = 100
            else:
                slot_size = 75
        # Once set the slot  size, we proceed with the calculation
        if slot_size >= need:
            return 1
        else:
            count = 1
            while slot_size < need:
                slot_size += slot_size
                count += 1
        return count
    
    def set_links_spectrum(self, links, end, slot_numbers, mode, lightpath_id):### TO FIX
        ranges = [x for x in range(end-slot_numbers+1, end+1)]
        modulation = 0 if mode == "DL" else 1 # 0 = 256 QAM, 1 = 64 QAM
        for i in ranges:
            for j in links:
                j.control[i][2] = 1
                j.control[i][1] = modulation
                j.control[i][0] = lightpath_id
                
  ##### These are interfaces with the lightpath class   ######         
    def establish_lightpath (self, source, destination, need, mode, lightpath_id):
        link_lists = self.get_all_links_objects(source, destination)
        number_slots = self.get_number_slots(need, mode)
        modulation = 0 if mode == "DL" else 1 # 0 = 256 QAM, 1 = 64 QAM
        channel_size = 40 * number_slots if modulation == 0 else 30 * number_slots
        for i in link_lists:
            template = self.test_path(i)
            cod = self.test_allocation(template, number_slots)
            if cod != -1: # That means there's a space to put the request.
                self.set_links_spectrum(i, cod, number_slots, mode, lightpath_id) # Setting configuration
                return [i, channel_size]
        return None
                
    def clean_lightpath(self, lightpath_id, links):
        for i in links:
            for j in range(0, len(i.control)):
                if i.control[j][0] == lightpath_id:
                    i.control[j][0] = 0
        
           
    
                
                
        
    
        
        
    
    
    
   