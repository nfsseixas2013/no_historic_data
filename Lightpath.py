#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 20:08:21 2021

@author: nilton
"""

import numpy as np
import Interface
from Template import template
import simpy
from IA.IA import IA
import pandas as pd
class lightpath:
    
    def __init__(self, env, cod, mode, source, destination, traffic, net, service_type, metric, IA, controller, error_type):
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
        self.traffic_predicted = 0 ## depois mudar isso
        self.path = 0 # defined by ILP solution
        self.modulation = 0 # defined by ILP solution
        self.slots = []
        self.latencia_required = 0
        self.IA = IA
        self.metric = metric
        self.service_type = service_type
        self.ia_data_input = []
        self.controller = controller
        self.controller.set_lightpaths(self)
        self.flag_update = False
        self.granted = 0
        self.connection_control = simpy.Store(env,capacity=simpy.core.Infinity)
        self.connection_nodes = simpy.Store(env,capacity=simpy.core.Infinity)
        self.connection_lightpath = simpy.Store(env,capacity=simpy.core.Infinity)
        self.eMBB_factor = 300.5
        self.mMTC_factor = 2.50
        self.URLLC_factor = 1.40
        self.split = None
        self.error_type = error_type
        self.time_slot = 600*6
        #self.ia_factor = 0

	# Interruption
        self.action = self.env.process(self.run())
       
        
######## Preparations to get ILP parameters  ########################
    def get_links_candidates(self): ## REF1
        # It returns format [(1,2),(2,3)]
        self.links_candidates = Interface.get_nodes_candidates(self.net,self.source, self.destination)
        
    def get_links_ids(self): # REF2
        # The purpose is get the ids of the links to fill edp constant in the ILP
        links_ids = []
        for i in self.links_candidates:
            aux = []
            for j in i:# list of list
               aux.append(Interface.get_link_id(j,self.net))
            links_ids.append(aux)
        self.links_ids = links_ids # We get the links separeted by path candidate
    
    def get_links_costs(self): # REF3
        # This function returns the cost per path. The function in the interface must change 
        for i in self.links_candidates:
            self.links_costs.append(Interface.get_cost(i,[0,1],self.net))
            
    def get_links_refs(self):# REF4
        ## getting the links objects to calculate teh template
        self.links_ref = Interface.get_links_ref_list(self.links_candidates,self.net)
        
        
    def get_slots_number(self,traffic): # REF5
        number_slots = []
        for i in self.mode:# It gets the number of slots per modulation
            number_slots.append(Interface.get_number_slots(traffic,i,self.net))
        return number_slots
        
    def get_templates(self): # REF6
        resultado = []
        for i in self.links_ref:
            aux = []
            aux2 = []
            for j in self.mode:
                aux.append([Interface.get_template(i,j),i])# Creating a reference for links and templates
                aux2.append([Interface.get_template_shadow(i,j),i])
            resultado.append(template(aux,aux2))  
        return resultado # Templates per modulation and per path
    
    def set_slices_candidates(self, modulation,slice_range,links,flag): # REF7
        #The purpose is control what range will be picked as slices candidates to different modulations
       ## In this case, modulation will be the index of templates at get_slices_indices
       if flag == False:
           Interface.set_links_spectrum(links,slice_range,modulation,self.id)
       else:
           Interface.set_links_spectrum_shadow(links,slice_range,modulation,self.id)
    
    def get_slices_indices(self,traffic): #
        ## This function returns the interval of slices candidates
        estrutura = self.get_templates() # REF6
        number_slots = self.get_slots_number(traffic) # REF5
        self.slots = number_slots.copy()
        slices = []
        for i in estrutura:
            indice = 0
            aux = []
            for a in range(0, len(self.mode)):
                flag = False
                end = Interface.test_allocation(i.template[a][0],number_slots[indice])
                if end == -1:
                    end = Interface.test_allocation(i.shadow[a][0],number_slots[indice])
                    flag = True
                start = end-number_slots[indice]+1
                aux.append([start,end+1])
                ## Call here the set_slices_candidates
                if flag == False:
                    self.set_slices_candidates(a,aux[a],i.template[a][1],flag)
                else:
                    self.set_slices_candidates(a,aux[a],i.shadow[a][1],flag)
                indice += 1
            slices.append(aux)
        self.slices = slices
        return slices
        
    def set_ILP(self,traffic,latencia,ILP): # REF9 -> REF1,REF2,REF3,REF4,REF8
        self.get_links_candidates() # REF1
        self.get_links_refs() # REF4
        self.get_links_ids() # REF2
        self.get_links_costs()# REF3
        self.get_slices_indices(traffic) # REF8
        latencia_values = self.calculate_latencies()
        ILP.latencia[self.id] = latencia
        self.latencia_required = latencia
        for p in range(0,len(self.links_candidates)):
            Interface.fill_links(self.links_ids[p],[self.id],[p],ILP)
            Interface.fill_dpm([self.id],[p],self.mode,self.links_costs[p],ILP)
            Interface.fill_gama([self.id],[p],[0],self.mode,[self.slices[p]],ILP)
            Interface.fill_latencies(self.id,p,latencia_values[p],ILP)
            
    def set_ILP_update(self,traffic,latencia,ILP):
        latencia_values = self.calculate_latencies()
        self.get_slices_indices(traffic)
        for p in range(0,len(self.links_candidates)):
            Interface.fill_links(self.links_ids[p],[self.id],[p],ILP)
            Interface.fill_dpm([self.id],[p],self.mode,self.links_costs[p],ILP)
            Interface.fill_gama([self.id],[p],[0],self.mode,[self.slices[p]],ILP)
            Interface.fill_latencies(self.id,p,latencia_values[p],ILP)
  
    def set_conf(self,indice):
        self.path = indice[1]
        self.modulation = indice[3]
        self.set_connection()
        self.granted = Interface.get_bandwidth(self.slots[self.modulation], self.modulation, self.net)
       
         
    def calculate_latencies(self):
        latencias = []
        for i in self.links_ref:
            soma = 0
            for j in i:
                soma += j.cost
            latencias.append(soma)
        return latencias
        
################################################ Spectrum Management ###################################################################
    
    def verify(self):
        intervalo = [x for x in range(0,len(self.links_ref[self.path][0].shadow[0]))]
        for i in intervalo:
            for j in self.links_ref[self.path]:
                if j.shadow[self.modulation][i][0] == self.id:
                    j.control[self.modulation][i][0] = self.id
            
    
    def set_connection(self): # REF10
        # It must be called after ILP decision
        self.verify()
        for i in range(0,len(self.links_candidates)):
            for j in self.mode:
                if j!= self.modulation:
                    Interface.clean_lightpath(self.id,self.links_ref[i],j)
    
    def update_connection(self,traffic):# REF11
        Interface.clean_lightpath(self.id,self.links_ref[self.path],self.modulation)
        number_slots = [Interface.get_number_slots(traffic,m,self.net) for m in self.mode]
        template = Interface.get_template(self.links_ref[self.path], self.modulation)
        end = Interface.test_allocation(template,number_slots[self.modulation])
        aux = []
        if end != -1:
            self.slots = number_slots.copy()
            start = end-number_slots[self.modulation]+1
            aux.append([start,end+1])
            self.set_slices_candidates(self.modulation,aux[0],self.links_ref[self.path],False)# This false is to link.control always.
            return True
        else:
            self.slots = [0,0]
            return False
############################################ Setting UP ##########################################################################
            
    def get_nodes_chosen(self):
        self.nodes = Interface.links2nodes(self.links_ref[self.path],self.links_candidates[self.path])
        
################################################ TRAFFIC #########################################################################
    
    def setup_predictions(self):
        flag = False
        if len(self.ia_data_input) == 4:
            if self.service_type == 'eMBB':
                self.traffic_predicted = self.IA.predict_eMBB(self.ia_data_input)+self.eMBB_factor
            elif self.service_type == 'mMTC':
                self.traffic_predicted = self.IA.predict_mMTC(self.ia_data_input)+self.mMTC_factor
            elif self.service_type == 'URLLC':
                self.traffic_predicted = self.IA.predict_URLLC(self.ia_data_input)+self.URLLC_factor
            #flag = self.update_connection(self.traffic_predicted)
            self.ia_data_input.pop(0) 
            
        elif len(self.ia_data_input) < 4 and self.service_type == 'eMBB':
            self.traffic_predicted = self.ia_data_input[len(self.ia_data_input)-1]+self.eMBB_factor
        elif len(self.ia_data_input) < 4 and self.service_type == 'mMTC':
            self.traffic_predicted = self.ia_data_input[len(self.ia_data_input)-1]+self.mMTC_factor
        elif len(self.ia_data_input) < 4 and self.service_type == 'URLLC':
            self.traffic_predicted = self.ia_data_input[len(self.ia_data_input)-1]+self.URLLC_factor

        flag = self.update_connection(self.traffic_predicted)
        print("\n lightpath: {} - Prediction: {} \n".format(self.id,self.traffic_predicted))
        return flag
        

    def sending(self,load): # Modularization of sending of one msg
        cost = 0
        self.get_nodes_chosen()
        for i in range(0, len(self.nodes)-1):
            link = self.get_link(self.nodes[i], self.nodes[i+1])
            cost += link.cost
            #yield self.env.timeout(link.cost)
            msg = [self.env.now,"bytes", self.id, load]
            self.nodes[i+1].connection.put(msg)
            self.nodes[i+1].env.process(self.nodes[i+1].receive_msg(cost))
        return cost


    def sending_traffic(self, traffic):
        slots_needed = Interface.get_number_slots(traffic,self.modulation,self.net)
        request = traffic
        if self.slots[self.modulation] - slots_needed < 0:
            self.report.append([self.id, self.env.now, 0, self.path, 0, self.traffic_predicted, request, self.granted, self.error_type])
            #if self.split != None:
            #    self.split.report.append([self.id, self.env.now, 0, self.path, 0, self.traffic_predicted, request, self.granted,self.error_type])
        else:
            #self.env.process(self.sending(traffic))
            wasting = Interface.get_bandwidth(self.slots[self.modulation],self.modulation,self.net) - traffic
            self.report.append([self.id, self.env.now, traffic, self.path, wasting, self.traffic_predicted, request, self.granted, self.error_type]) # Reporting
            cost = self.sending(traffic)
            yield self.env.timeout(cost)
            if type(self).__name__ == 'lightpath':
                if self.split != None:
                    msg = [traffic]
                    self.split.connection_lightpath.put(msg)
        
   
             
    def get_conf_indices(self):
        for i in self.controller.conf:
            if i[0] == self.id:
                return i
          
    def get_link(self, node1, node2):
        for i in self.net.links:
            if node1 in i.nodes and node2 in i.nodes:
                return i
    

    def run(self):
        time_counter = 0
        interval_data = []
        for i in self.traffic:
            contador = 0
            while contador <  600: # time_slot dataset.
                traffic = np.random.poisson(i,1)[0]
                while traffic == 0:
                    traffic = np.random.poisson(i,1)[0]
                try:
                    if self.flag_update == True:
                        indices = self.get_conf_indices()
                        self.set_conf(indices)
                    self.env.process(self.sending_traffic(traffic))
                    interval_data.append(traffic)
                    yield self.env.timeout(1)
                except simpy.Interrupt:
                    contador -=1
                    time_counter -= 1 
                    self.flag_update = True
                contador += 1
                time_counter += 1

            if time_counter == self.time_slot:
                if self.metric == 'median':
                    self.ia_data_input.append(np.median(interval_data))
                elif self.metric == 'quantile3':
                    self.ia_data_input.append(np.quantile(interval_data,0.75))
                else:
                    self.ia_data_input.append(np.amax(interval_data))
                flag = self.setup_predictions()
                if flag:
                    self.granted = Interface.get_bandwidth(self.slots[self.modulation], self.modulation, self.net)
                self.env.process(self.send_msg_control(flag))
                time_counter = 0
                interval_data = []
              
               
    
                     
  
    
################################# CONTROL ###########################################################
    def send_msg_control(self,flag):
        msg = [flag, self.traffic_predicted, self]
        self.controller.connection.put(msg)
        yield self.controller.env.process(self.controller.receive_msg(msg))
        yield self.env.timeout(0.000001)
 
    def set_splits(self, split):
        self.split = split
            
#######################################################################################################################     
        
    def get_reports(self):
        id_lightpath = [x[0] for x in self.report]
        time = [x[1] for x in self.report]
        traffic = [x[2] for x in self.report]
        path = [x[3] for x in self.report]
        wasting = [x[4] for x in self.report]
        predicted_traffic = [x[5] for x in self.report]
        request = [x[6] for x in self.report]
        granted = [x[7] for x in self.report]
        error_type = [x[8] for x in self.report]
        data_dict = {'id':id_lightpath, 'time': time, 'traffic': traffic, 'path': path, 
        'wasting': wasting, 'predicted_traffic': predicted_traffic, 'request': request, 'granted': granted,
        'error_type': error_type}
        return pd.DataFrame(data_dict)

    
    
     
