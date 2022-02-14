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
         self.action = env.process(self.run())

     def run(self):
         while True:
             '''
             print('Start parking and charging at %d' % self.env.now)
             charge_duration = 5
             # We yield the process that process() returns
             # to wait for it to finish
             yield self.env.process(self.charge(charge_duration))

             # The charge process has finished and
             # we can start driving again.
             print('Start driving at %d' % self.env.now)
             trip_duration = 2
             yield self.env.timeout(trip_duration)
             '''
             try:
                 print('Driving at %d' % self.env.now)
                 yield self.env.timeout(1)
                 if len(self.flag_msg) == 40:
                     print("Minha pica hahahaha")
             except simpy.Interrupt:
                 yield self.env.process(self.receivemsg())

     def charge(self, duration):
         yield self.env.timeout(duration)
         
         
     def receivemsg(self):
         msg = yield self.connection.get()
         print(msg[0])
         self.flag_msg.append(True)
         yield self.env.timeout(0.000001)
         
         
         
class Car2(object):
     def __init__(self, env,car):
         self.env = env
         self.connection = simpy.Store(env,capacity=simpy.core.Infinity)
         self.flag_msg = False
         self.env.process(self.sendmsg(car))
         self.action = env.process(self.run())

     def run(self):
         while True:
             '''
             print('Start parking and charging at %d' % self.env.now)
             charge_duration = 5
             # We yield the process that process() returns
             # to wait for it to finish
             yield self.env.process(self.charge(charge_duration))

             # The charge process has finished and
             # we can start driving again.
             print('Start driving at %d' % self.env.now)
             trip_duration = 2
             yield self.env.timeout(trip_duration)
             '''
             yield self.env.timeout(1)

     def charge(self, duration):
         yield self.env.timeout(duration)
         
     def sendmsg(self,car):
         yield self.env.timeout(5)
         msg = ['haha']
         car.connection.put(msg)
         car.action.interrupt()
         yield self.env.timeout(0.0000001)
         
     def receivemsg(self):
         msg = yield self.connection.get()
         print(msg[0])
         self.flag_msg = True
         
         

env = simpy.Environment()
car = Car(env)
car2 = Car2(env,car)
env.run(until=15)