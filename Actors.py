#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 19:41:49 2021

@author: nilton
"""

from Node import node

class Actor(node):
    
    def __init__(self, cod, env):
        super().__init__(cod, env)
        
    def receive_msg(self):
        msg = yield self.connection.get()
        print('the bits of lightpath %d has been received at %f by node %d' % (msg[2], self.env.now, self.id))
    
        
       
        
    
    