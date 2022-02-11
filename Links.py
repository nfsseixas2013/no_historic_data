#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:58:00 2021

@author: nilton
"""

class link:
    global ultra_eon
    global eon
    global reduced_eon
    global testing
    ultra_eon = 800
    reduced_eon = 640
    eon = 320
    testing = 2
    def __init__(self, node1, node2,frequency_slot_size_cod, cost, id_cod):
        self.nodes = [node1, node2]
        self.size = frequency_slot_size_cod
        self.id = id_cod
        self.control = [[],[]]
        self.shadow = [[],[]]
        
        if frequency_slot_size_cod == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.control[0] = [[-1,0,0] for x in range (0, ultra_eon) ]
            self.control[1] = [[-1,1,0] for x in range (0, ultra_eon) ]
        elif frequency_slot_size_cod == 1:
            self.control[0] = [[-1,0,0] for x in range (0, reduced_eon) ]
            self.control[1] = [[-1,1,0] for x in range (0, reduced_eon) ]
        elif frequency_slot_size_cod == 2:
            self.control[0] = [[-1,0,0] for x in range (0, eon) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, eon) ]
        else:
            self.control[0] = [[-1,0,0] for x in range (0, testing) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, testing) ]
            
        if frequency_slot_size_cod == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.shadow[0] = [[-1,0,0] for x in range (0, ultra_eon) ]
            self.shadow[1] = [[-1,1,0] for x in range (0, ultra_eon) ]
        elif frequency_slot_size_cod == 1:
            self.shadow[0] = [[-1,0,0] for x in range (0, reduced_eon) ]
            self.shadow[1] = [[-1,1,0] for x in range (0, reduced_eon) ]
        elif frequency_slot_size_cod == 2:
            self.shadow[0] = [[-1,0,0] for x in range (0, eon) ] # [lightpath_id, modulation, control]
            self.shadow[1] = [[-1,1,0] for x in range (0, eon) ]
        else:
            self.shadow[0] = [[-1,0,0] for x in range (0, testing) ] # [lightpath_id, modulation, control]
            self.shadow[1] = [[-1,1,0] for x in range (0, testing) ]
        
        
   #     self.env = env
        self.traffic = []
        self.cost = cost * 0.000005 # 5 microsseconds per km 
        
    def add_traffic(self, time, load):
        self.traffic.append([time,load])
    
    def reset_control(self):
        if self.size == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.control[0] = [[-1,0,0] for x in range (0, ultra_eon) ]
            self.control[1] = [[-1,1,0] for x in range (0, ultra_eon) ]
        elif self.size == 1:
            self.control[0] = [[-1,0,0] for x in range (0, reduced_eon) ]
            self.control[1] = [[-1,1,0] for x in range (0, reduced_eon) ]
        elif self.size == 2:
            self.control[0] = [[-1,0,0] for x in range (0, eon) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, eon) ]
        else:
            self.control[0] = [[-1,0,0] for x in range (0, testing) ] # [lightpath_id, modulation, control]
            self.control[1] = [[-1,1,0] for x in range (0, testing) ]
            
        if self.size == 0: # 0 for 5GHz, 1 for 6.25 GHz and 2 for 12.5GHz
            self.shadow[0] = [[-1,0,0] for x in range (0, ultra_eon) ]
            self.shadow[1] = [[-1,1,0] for x in range (0, ultra_eon) ]
        elif self.size == 1:
            self.shadow[0] = [[-1,0,0] for x in range (0, reduced_eon) ]
            self.shadow[1] = [[-1,1,0] for x in range (0, reduced_eon) ]
        elif self.size == 2:
            self.shadow[0] = [[-1,0,0] for x in range (0, eon) ] # [lightpath_id, modulation, control]
            self.shadow[1] = [[-1,1,0] for x in range (0, eon) ]
        else:
            self.shadow[0] = [[-1,0,0] for x in range (0, testing) ] # [lightpath_id, modulation, control]
            self.shadow[1] = [[-1,1,0] for x in range (0, testing) ]
    
