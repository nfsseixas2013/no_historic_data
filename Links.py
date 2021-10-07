#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:58:00 2021

@author: nilton
"""

class link:
    def __init__(self, node1, node2,frequency_slot_size_cod, cost):
        self.nodes = [node1, node2]
        self.size = frequency_slot_size_cod
        if frequency_slot_size_cod == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.control = [[0,0,0] for x in range (0, 800) ]
        elif frequency_slot_size_cod == 1:
            self.control = [[0,0,0] for x in range (0, 640) ]
        else:
            self.control = [[0,0,0] for x in range (0, 320) ] # [lightpath_id, modulation, control]
   #     self.env = env
        self.traffic = []
        self.cost = cost * 5 # 5 microsseconds per km 
        
    def add_traffic(self, time, load):
        self.traffic.append([time,load])
        
    
