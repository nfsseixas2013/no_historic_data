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

############################################# Sorted links candidates ########
def get_nodes_candidates(net, source, destination):
   paths =  list(it.islice(nx.shortest_simple_paths(net.graph, source, destination), 2))
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
                
def fill_latencies(d,p,value, ILP):
    ILP.set_ldp((d,p),value)
    
    
############################## Parameters of ILP ##################################
    
def get_link_id(link,net):
    for i in net.links:
        if (i.nodes[0].id == link[0] or i.nodes[0].id == link[1]) and (i.nodes[1].id == link[0] or i.nodes[1].id == link[1]):
            return i.id
        
def get_cost(links,modulation,net):# Only for test. Shall be changed
   # 1 kwh per kilometer modulation 1
   # 2 Kwh per kilometer modulation 2
   costs = []
   for m in modulation:
       soma = 0
       for l in links:
           if m == 0:
               soma += net.graph.edges[l]["weight"]
           else:
               soma += 2 * net.graph.edges[l]["weight"]
       costs.append(soma)
   return costs
   
   
def get_number_slots(need, modulacao, net): # need in Gbps
        # This method returns the number of slots needed to establish the lightpath.
        slot_type = net.links[0].size # The size is equal to everyone
        if modulacao == 1:
            if slot_type == 0 or slot_type == 3: # 5GHZ
                slot_size = 40
            elif slot_type == 1: # 6.25GHZ
                slot_size = 48
            else:
                slot_size = 100 # 12.5 GHZ
        else:
            if slot_type == 0 or slot_type == 3:
                slot_size = 30
            elif slot_type == 1:
                slot_size = 36
            else:
                slot_size = 75
           
        
        # Once set the slot  size, we proceed with the calculation
        if slot_size >= need:
            return 1
        else:
            count = 1
            bandwidth = slot_size
            while bandwidth < need:
                bandwidth += slot_size
                count += 1
        return count
    
def get_bandwidth(slots,modulation,net):
    slot_type = net.links[0].size # The size is equal to everyone
    if modulation == 1:
        if slot_type == 0 or slot_type == 3: # 5GHZ
            slot_size = 40
        elif slot_type == 1: # 6.25GHZ
            slot_size = 48
        else:
            slot_size = 100 # 12.5 GHZ
    else:
        if slot_type == 0 or slot_type == 3:
            slot_size = 30
        elif slot_type == 1:
            slot_size = 36
        else:
            slot_size = 75
    bandwidth = 0
    for i in range(0,slots):
        bandwidth += slot_size
    return bandwidth


def get_link_ref(link,net):## Link is a tuple
    for i in net.links:
        if (i.nodes[0].id == link[0] or i.nodes[0].id == link[1]) and (i.nodes[1].id == link[0] or i.nodes[1].id == link[1]):
            return i
        
def get_links_ref_list(links,net): # return the references of the links
    lista = []
    for i in links:
        aux = []
        for j in i: # to break into tuples
            aux.append(get_link_ref(j,net)) # I did that to separate links candidates of different paths
        lista.append(aux)
    return lista

def get_template(links, modulation): # It receives a list of links(references) and return a template of use of the spectrum
        resposta = []
        for i in range(0, len(links[0].control[modulation])):# Every link.control has the same size.
            flag = 0
            for j in links:
                if j.control[modulation][i][2] == 1: ## OR logic
                    resposta.append(1)
                    flag = 1
                    break
            if flag == 0:
                resposta.append(0)
        return resposta  # This answer will hold a template of the state of the network.
    
    
def get_template_shadow(links, modulation): # It receives a list of links(references) and return a template of use of the spectrum
        resposta = []
        for i in range(0, len(links[0].shadow[modulation])):# Every link.control has the same size.
            flag = 0
            for j in links:
                if j.shadow[modulation][i][2] == 1: ## OR logic
                    resposta.append(1)
                    flag = 1
                    break
            if flag == 0:
                resposta.append(0)
        return resposta  # This answer will hold a template of the state of the network.

def test_allocation(template, slot_numbers):
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

    
############################## Spectrum Management #####################################################
def set_links_spectrum(links, slice_range, modulation, lightpath_id):
        ranges = [x for x in range(slice_range[0], slice_range[1])]
        for i in ranges:
            for j in links:
                j.control[modulation][i][2] = 1
                j.control[modulation][i][0] = lightpath_id
        

                
def set_links_spectrum_shadow(links, slice_range, modulation, lightpath_id):
        ranges = [x for x in range(slice_range[0], slice_range[1])]
        for i in ranges:
            for j in links:
                j.shadow[modulation][i][2] = 1
                j.shadow[modulation][i][0] = lightpath_id

                


def clean_lightpath(lightpath_id, links, modulation):
    for i in links:
        for j in range(0, len(i.control[0])):
            if i.control[modulation][j][0] == lightpath_id:
                i.control[modulation][j][0] = -1
                i.control[modulation][j][2] = 0

                
                
################################ Setting UP ############################################################

def setting_connections(conf,lightpaths):
    for i in lightpaths:
        for j in conf:
            if j[0] == i.id:
                i.set_conf(j)

def setting_connections_update(conf,lightpaths):
    for i in lightpaths:
        for j in conf:
            if j[0] == i.id:
                i.set_conf_update(j)
                
def fetch_node(id_, links):
    for i in links:
        if i.nodes[0].id == id_ :
            return i.nodes[0]
        elif i.nodes[1].id == id_:
            return i.nodes[1]

def links2nodes(links,nodes_candidates):
    nodes = []
    for i in nodes_candidates:
        candidate = fetch_node(i[0], links)
        if candidate not in nodes:
            nodes.append(candidate)
        candidate = fetch_node(i[1], links)
        if candidate not in nodes:
            nodes.append(candidate)
    return nodes
            

    
               
        
    
        
        
    
    
    
   
