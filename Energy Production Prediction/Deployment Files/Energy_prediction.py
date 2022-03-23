#Importing the required libaries
import numpy as np
import pandas as pd
import streamlit as st 
#import xgboost as xgb
from xgboost import XGBRegressor
import pickle
from pickle import dump
from pickle import load


#Title of the Site
st.title("Energy Production Prediction")

st.sidebar.header('Enter your Inputs')

# load the model from disk
loaded_model = load(open('Energy_Prediction.sav', 'rb'))
#loaded_model = load(open('Energy_Predictions.pickle', 'rb'))

def user_input_features():
    temperature = st.sidebar.number_input('Enter the Temperature Value')
    exhaust_vacuum = st.sidebar.number_input('Enter the Exhaust Vaccum Value')
    amb_pressure = st.sidebar.number_input('Enter the Amb Pressure Value')
    r_humidity = st.sidebar.number_input("Enter the Humidity Value")
    data = {'temperature':temperature,
            'exhaust_vacuum':exhaust_vacuum,
            'amb_pressure':amb_pressure,
            'r_humidity':r_humidity,
            }
    features = pd.DataFrame(data,index = [0])
    return features 
    
df = user_input_features()
st.subheader('User Input parameters')
st.write(df)

#Prediction
prediction = loaded_model.predict(df)

st.subheader('Predicted Energy Production')
st.write(prediction)