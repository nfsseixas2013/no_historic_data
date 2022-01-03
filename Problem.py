#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Network import network
from Interface import interface
from Lightpath import lightpath
import simpy


# In[2]:


#from IPython.display import Image
#Image(filename='04.png') 


# In[3]:


env = simpy.Environment()
topologia = [(1,2,10),(2,3,10), (3,4,10), (4,5,10), (5,6,10), (1,7,15), (7,8,10), (8,9,10),(9,6,25)]
switches = [2,3,4,5,7,8,9]
actors = [1,6]
frequency_slot = 0 # 5GHz

net = network(topologia,switches,actors,frequency_slot,env)
rsa = interface(net)

traffic = [31000,31000,31000,31000]
traffic2 = [1000,1000,2000,2000]

eMBB = lightpath(env,1,rsa,'DL',1,5,traffic)
URLLC = lightpath(env,2,rsa,'DL',1,5,traffic2)


# In[4]:


env.run(until = 4)


# In[ ]:




