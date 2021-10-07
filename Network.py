#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 17:38:09 2021

@author: nilton
"""
from Node import node
from Actors import Actor
from Links import link
import networkx as nx

class network:
    def __init__(self, conf_graph, set_nodes, set_actors, frequency_slot_size, env):
       self.nodes = []
       self.actors = []
       self.switch = []
       self.links = []
       self.graph = nx.Graph()
       self.set_nodes = set_nodes
       self.set_actors = set_actors
       self.frequency_slot_size = frequency_slot_size
       self.conf_graph = conf_graph
       self.create_graph()
       self.env = env
       self.create_nodes()
       self.create_actors()
       self.create_links()
       
    def create_graph(self):
        self.graph.add_weighted_edges_from(self.conf_graph)
        
    def create_nodes(self):
        for i in self.set_nodes:
            aux = node(i,self.env)
            self.nodes.append(aux)
            self.switch.append(aux)
    
    def create_actors(self):
        for i in self.set_actors:
            aux = Actor(i, self.env)
            self.nodes.append(aux)
            self.actors.append(aux)
            
    def get_nodes(self, id1, id2):
        result = []
        for i in self.nodes:
            if i.id == id1 or i.id == id2:
                result.append(i)
        return result
    
    def create_links(self):
        for i in self.conf_graph:
            nodes = self.get_nodes(i[0], i[1])
            aux = link(nodes[0], nodes[1], self.frequency_slot_size, i[2])
            self.links.append(aux)
            nodes[0].links.append(aux)
            nodes[1].links.append(aux)
            
   
    