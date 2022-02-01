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
        file = open('eMBB_brain.json', 'r')
        self.eMBB_model = model_from_json(file.read())
        file.close()
        self.eMBB_model.load_weights('eMBB_brain_pesos.h5')
        # Loading scaler of eMBB
        self.eMBB_scaler = joblib.load('eMBB_normalizer.save')
        # Compiling the model
        self.eMBB_model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['mean_absolute_error'])
        
        ## Loading model and weights of eMBB
        file = open('mMTC_URLLC_brain.json', 'r')
        self.URLLC_mMTC_model = model_from_json(file.read())
        file.close()
        self.URLLC_mMTC_model.load_weights('mMTC_URLLC_brain_pesos.h5')
        # Loading scaler of URLLC_mMTC
        self.URLLC_mMTC_scaler = joblib.load('mMTC_URLLC_normalizer.save')
        # compiling the model
        self.URLLC_mMTC_model.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['mean_absolute_error'])
    
        
    def predict_eMBB(self, predictors):
        new_values = np.array(predictors)
        new_values = new_values.reshape(-1,1)
        new_values_norm = self.eMBB_scaler.transform(new_values)
        new_values_norm = new_values_norm.reshape(1,-1)
        input_values = np.reshape(new_values_norm, (new_values_norm.shape[0], new_values_norm.shape[1], 1))
        predicted = self.eMBB_model.predict(input_values)
        return self.eMBB_scaler.inverse_transform(predicted)[0][0]
    
    def predict_UR_mM(self, predictors):
        new_values = np.array(predictors)
        new_values = new_values.reshape(-1,1)
        new_values_norm = self.URLLC_mMTC_scaler.transform(new_values)
        new_values_norm = new_values_norm.reshape(1,-1)
        input_values = np.reshape(new_values_norm, (new_values_norm.shape[0], new_values_norm.shape[1], 1))
        predicted = self.URLLC_mMTC_model.predict(input_values)
        return self.URLLC_mMTC_scaler.inverse_transform(predicted)[0][0]
    

    
   