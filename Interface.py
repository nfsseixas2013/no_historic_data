#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 19:31:00 2021

@author: nilton
"""

import networkx as nx
import itertools as it
import copy as c
#from RMSA_ILP import rmsa_ilp

##### Sorted links ########
def get_nodes_candidates(net, source, destination):
   paths =  list(it.islice(nx.shortest_simple_paths(net.graph, source, destination), 3))
   links = []
   for i in paths:
       link = nodes2links(i)
       links.append(link)
   links = sorting_paths(net,links)
   return links
   

def nodes2links(path): # PRIVATE 
        # The goal of this method is return list of links of the same path. Ex. [x,y,z]->[(x,y), (y,z)]
        result = []
        for i in range(0, len(path)-1):
            result.append((path[i],path[i+1]))
        return result

def get_weight_links(net, links): ## Get the sum of the weights ## PUBLIC
    pesos = []
    for i in links:
        soma = 0
        for j in i:
            soma += net.graph.edges[j]["weight"]
        pesos.append(soma)
    return pesos

def sorting_paths(net, links): # here I use bubble sort to put paths in ascending order. ## PRIVATE
    pesos = get_weight_links(net, links)
    enlace =  links.copy()
    for i in range(0,len(enlace)):
        for j in range(i+1, len(pesos)):
             if pesos[i] > pesos[j]:
                    aux = c.copy(enlace[i])
                    enlace[i] = enlace[j]
                    enlace[j] = c.copy(aux)
                    ##
                    aux = pesos[i]
                    pesos[i] = pesos[j]
                    pesos[j] = aux
    return enlace

############################FILLING the ILP #######################################

def fill_gama(d,p,c,m,canais_candidatos, ILP): 
    for d_ in d:
        for p_ in p:
            for c_ in c:
                for m_ in m:
                    for s in canais_candidatos:
                        for i in range(s[m_][0], s[m_][1]):
                            ILP.set_slices((d_,p_,c_,m_,i))

def fill_links(e,d,p, ILP):
    for e_ in e:
        for d_ in d:
            for p_ in p:
                ILP.set_links((e_,d_,p_))

def fill_dpm(d,p,m,custos, ILP):
    contador = 0
    for d_ in d:
        for p_ in p:
            for m_ in m:
                ILP.set_dpm((d_,p_,m_),custos[contador])
                contador += 1
                
def fill_latencies(latencias, ILP):
    ILP.set_latencias(latencias)
                                
###################################################################################
                
'''

class interface:
    
    def __init__(self, net):
        self.net = net
        self.path = []
        
    def get_nodes_candidates(self, source, destination): # we will work with 2 paths for now...(PRIVATE)
        # source and destinations are nodes id...
        # 
        return list(it.islice(nx.shortest_simple_paths(self.net.graph, source, destination), 3))
        #return list(nx.shortest_simple_paths(self.net.graph, source, destination))
        # it most return the list of ids of nodes
        
    
    
    def get_links_candidates(self, source, destination):#(PRIVATE)
        # The goal of this method is call recursively the method nodes2links to transform all candidate nodes
        # in tuples of links. Ex. [[x,y,z], [a,b,c]]->[[(x,y), (y,z)], [(a,b), (b,c)]]
        nodes_ref = self.get_nodes_candidates(source, destination)
        paths = []
        self.path = []
        for i in nodes_ref:
            paths.append(self.nodes2links(i))
            self.path.append(i) # This is the set of nodes id in the exact order in the paths. 
        return paths
    
    def get_nodes_object(self, link):# link is a tuple Ex. (1,2)
        # This method gets the nodes objects referenced by a link 
        nodes = []
        for i in self.net.nodes:
            if i.id == link[0] or i.id == link[1]:
                nodes.append(i)      
        return nodes # Return the references of nodes
    
    def get_link_object(self, node1, node2):
        # With the 2 nodes of a link, we can get the link object
        for i in self.net.links:
            if node1 in i.nodes and node2 in i.nodes:
                return i # Sending references of the link object
    
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
                slot_size += 40
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
                
    def get_node_indice(self, indice):
        for i in self.net.nodes:
            if i.id == indice:
                return i
            
    def get_node_list(self,lista):# get the path nodes in the correct order
        result = []
        for i in lista:
            result.append(self.get_node_indice(i))
        return result
                
  ##### These are interfaces with the lightpath class   ######         
    def establish_lightpath (self, source, destination, need, mode, lightpath_id):
        link_lists = self.get_all_links_objects(source, destination)
        self.putting_order()
        number_slots = self.get_number_slots(need, mode)
        modulation = 0 if mode == "DL" else 1 # 0 = 256 QAM, 1 = 64 QAM
        channel_size = 40 * number_slots if modulation == 0 else 30 * number_slots
        indice_path = 0 # To get the indice of path with nodes id
        for i in link_lists:
            template = self.test_path(i)
            cod = self.test_allocation(template, number_slots)
            if cod != -1: # That means there's a space to put the request.
                self.set_links_spectrum(i, cod, number_slots, mode, lightpath_id) # Setting configuration
                return [i, channel_size, self.get_node_list(self.path[indice_path])]
            indice_path += 1
        return None
                
    def clean_lightpath(self, lightpath_id, links):
        for i in links:
            for j in range(0, len(i.control)):
                if i.control[j][0] == lightpath_id:
                    i.control[j][0] = 0
                    i.control[j][1] = 0
                    i.control[j][2] = 0

# Sorting Candidates
                    
    def get_weight_list(self, link):# List of links
        result = []
        for i in link:
            soma = 0
            for j in range(0, len(i)):
                soma += self.net.graph.get_edge_data(i[j][0], i[j][1])["weight"]
            result.append(soma)
        return result
    
    def put_path_order(self, result):
        for i in range(0, len(result)):
            for j in range(i+1, len(result)):
                if result[i] > result[j]:
                    aux = c.copy(self.path[i])
                    self.path[i] = c.copy(self.path[j])
                    self.path[j] = c.copy(aux)
        
        
    def putting_order(self):
         links = []
         for i in self.path:
             links.append(self.nodes2links(i))
         result = self.get_weight_list(links)
         self.put_path_order(result)
         
           
''' 
                
                
        
    
        
        
    
    
    
   
