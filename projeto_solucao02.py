# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""
import simpy
class Car(object):
     def __init__(self, env):
         self.env = env
         self.connection = simpy.Store(env,capacity=simpy.core.Infinity)
         self.flag_msg = []
         # Start the run process everytime an instance is created.

     def receivemsg(self):
         msg = yield self.connection.get()
         self.flag_msg.append(msg[0])
         if len(self.flag_msg) == 40:
             print("Bingo")
             print(self.env.now)
             self.flag_msg.clear()
             print("tamanho de flag: {}".format(len(self.flag_msg)))
         yield self.env.timeout(0.0000001)
         
         
         
class Car2(object):
     def __init__(self, env,car):
         self.env = env
         self.connection = simpy.Store(env,capacity=simpy.core.Infinity)
         self.flag_msg = False
         self.car = car
         self.action = env.process(self.run())

     def run(self):
         while True:
             
             yield self.env.process(self.sendmsg(self.car))

     def charge(self, duration):
         yield self.env.timeout(duration)
         
     def sendmsg(self,car):
         yield self.env.timeout(5)
         msg = [True]
         print("Enviado no {}".format(self.env.now))
         car.connection.put(msg)
         yield car.env.process(car.receivemsg())
         
         
         
         
     def receivemsg(self):
         msg = yield self.connection.get()
         print(msg[0])
         self.flag_msg = True
         
         

env = simpy.Environment()
car = Car(env)
for i in range(0,40):
    car2 = Car2(env,car)
env.run(until=15)