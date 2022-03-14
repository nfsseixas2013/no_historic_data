#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:58:00 2021

@author: nilton
"""

import pandas as pd
import simpy

class link:
    global ultra_eon
    global eon
    global reduced_eon
    global testing
    ultra_eon = 800
    reduced_eon = 640
    eon = 320
    testing = 2
    def __init__(self, node1, node2,frequency_slot_size_cod, cost, id_cod, env):
        self.nodes = [node1, node2]
        self.size = frequency_slot_size_cod
        self.id = id_cod
        self.control = [[],[]]
        self.shadow = [[],[]]

        self.fragmentation = []
        self.frag_x_time = []
        self.env = env
        #self.connection = simpy.Store(env,capacity=simpy.core.Infinity)

        
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

            
    def get_template_link(self):
        template = []
        for i in range(0,len(self.control[0])):
            if self.control[0][i][2] == 1 or self.control[1][i][2] == 1:
                template.append(1)
            else:
                template.append(0)
        return template
                
            
    def get_fragmentation(self, time):
        template = self.get_template_link()
        counter = 0
        flag = False
        for i in range(len(template)-1,-1,-1):
           if flag == False: 
               if template[i] == 1:
                flag = True
           else:
                if template[i] == 0:
                    counter += 1
        self.fragmentation.append(counter/len(template))
        self.frag_x_time.append([time,(counter/len(template)), self.id])
        
    def get_report(self):
        time = [x[0] for x in self.frag_x_time]
        fragmentation = [x[1] for x in self.frag_x_time]
        id_link = [x[2] for x in self.frag_x_time]
        dict_data = {'time': time, 'fragmentation': fragmentation, 'id': id_link}
        return pd.DataFrame(dict_data)
   

