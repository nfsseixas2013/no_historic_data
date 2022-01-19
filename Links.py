#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:58:00 2021

@author: nilton
"""

class link:
    def __init__(self, node1, node2,frequency_slot_size_cod, cost, id_cod):
        self.nodes = [node1, node2]
        self.size = frequency_slot_size_cod
        self.id = id_cod
        self.control = [[],[]]
        self.shadow = [[],[]]
        
        if frequency_slot_size_cod == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.control[0] = [[-1,0,0] for x in range (0, 800) ]
            self.control[1] = [[-1,1,0] for x in range (0, 800) ]
        elif frequency_slot_size_cod == 1:
            self.control[0] = [[-1,0,0] for x in range (0, 640) ]
            self.control[1] = [[-1,1,0] for x in range (0, 640) ]
        elif frequency_slot_size_cod == 2:
            self.control[0] = [[-1,0,0] for x in range (0, 320) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, 320) ]
        else:
            self.control[0] = [[-1,0,0] for x in range (0, 2) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, 2) ]
            
        if frequency_slot_size_cod == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.shadow[0] = [[-1,0,0] for x in range (0, 800) ]
            self.shadow[1] = [[-1,1,0] for x in range (0, 800) ]
        elif frequency_slot_size_cod == 1:
            self.shadow[0] = [[-1,0,0] for x in range (0, 640) ]
            self.shadow[1] = [[-1,1,0] for x in range (0, 640) ]
        elif frequency_slot_size_cod == 2:
            self.shadow[0] = [[-1,0,0] for x in range (0, 320) ] # [lightpath_id, modulation, control]
            self.shadow[1] = [[-1,1,0] for x in range (0, 320) ]
        else:
            self.shadow[0] = [[-1,0,0] for x in range (0, 2) ] # [lightpath_id, modulation, control]
            self.shadow[1] = [[-1,1,0] for x in range (0, 2) ]
        
        
   #     self.env = env
        self.traffic = []
        self.cost = cost * 0.000005 # 5 microsseconds per km 
        
    def add_traffic(self, time, load):
        self.traffic.append([time,load])
    
    def reset_control(self):
        if self.size == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.control[0] = [[-1,0,0] for x in range (0, 800) ]
            self.control[1] = [[-1,1,0] for x in range (0, 800) ]
        elif self.size == 1:
            self.control[0] = [[-1,0,0] for x in range (0, 640) ]
            self.control[1] = [[-1,1,0] for x in range (0, 640) ]
        else:
            self.control[0] = [[-1,0,0] for x in range (0, 320) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, 320) ]
    
