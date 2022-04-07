#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:08:50 2022

@author: nilton
"""
from keras.models import model_from_json
import joblib
import numpy as np

class IA:
    def __init__(self):
        ## Loading model and weights of eMBB
        file = open('../IA/eMBB_brain.json', 'r')
        self.eMBB_model = model_from_json(file.read())
        file.close()
        self.eMBB_model.load_weights('../IA/eMBB_brain_pesos.h5')
        # Loading scaler of eMBB
        self.eMBB_scaler = joblib.load('../IA/eMBB_normalizer.save')
        # Compiling the model
        self.eMBB_model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['mean_absolute_error'])
        
         ## Loading model and weights of mMTC
        file = open('../IA/mMTC_brain.json', 'r')
        self.mMTC_model = model_from_json(file.read())
        file.close()
        self.mMTC_model.load_weights('../IA/mMTC_brain_pesos.h5')
        # Loading scaler of mMTC
        self.mMTC_scaler = joblib.load('../IA/mMTC_normalizer.save')
        # compiling the model
        self.mMTC_model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['mean_absolute_error'])

        ## Loading model and weights of URLLC
        file = open('../IA/URLLC_brain.json', 'r')
        self.URLLC_model = model_from_json(file.read())
        file.close()
        self.URLLC_model.load_weights('../IA/URLLC_brain_pesos.h5')
        # Loading scaler of mMTC
        self.URLLC_scaler = joblib.load('../IA/URLLC_normalizer.save')
        # compiling the model
        self.URLLC_model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['mean_absolute_error'])

        
    def predict_eMBB(self, predictors):
        new_values = np.array(predictors)
        new_values = new_values.reshape(-1,1)
        new_values_norm = self.eMBB_scaler.transform(new_values)
        new_values_norm = new_values_norm.reshape(1,-1)
        input_values = np.reshape(new_values_norm, (new_values_norm.shape[0], new_values_norm.shape[1], 1))
        predicted = self.eMBB_model.predict(input_values)
        return self.eMBB_scaler.inverse_transform(predicted)[0][0]
    
    def predict_mMTC(self, predictors):
        new_values = np.array(predictors)
        new_values = new_values.reshape(-1,1)
        new_values_norm = self.mMTC_scaler.transform(new_values)
        new_values_norm = new_values_norm.reshape(1,-1)
        input_values = np.reshape(new_values_norm, (new_values_norm.shape[0], new_values_norm.shape[1], 1))
        predicted = self.mMTC_model.predict(input_values)
        return self.mMTC_scaler.inverse_transform(predicted)[0][0]


    def predict_URLLC(self, predictors):
        new_values = np.array(predictors)
        new_values = new_values.reshape(-1,1)
        new_values_norm = self.URLLC_scaler.transform(new_values)
        new_values_norm = new_values_norm.reshape(1,-1)
        input_values = np.reshape(new_values_norm, (new_values_norm.shape[0], new_values_norm.shape[1], 1))
        predicted = self.URLLC_model.predict(input_values)
        return self.URLLC_scaler.inverse_transform(predicted)[0][0]


    

    
   
