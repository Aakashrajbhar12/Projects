#Importing the required libaries
import numpy as np
import pandas as pd
import streamlit as st 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge 
import pickle
import json
from pickle import dump
from pickle import load

data_columns = None
encode_list = None


#Title of the Site
st.title("Mumbai Houses Price Prediction")

st.sidebar.header('Enter your options')

with open("columns.json", "r") as f:
        data_columns = json.load(f)['data_columns']
        encode_list = data_columns[6:]

# load the model from disk
#loaded_model = load(open('house_price_model.sav', 'rb'))
loaded_model = load(open('house_prices_model.pickle', 'rb'))

area = st.sidebar.number_input("area")
Bedrooms = st.sidebar.selectbox('Bedrooms',('2','3','4','5','6','7','8'))
Bathrooms = st.sidebar.selectbox('Bathrooms',('2','3','4','5','6','7'))
Balcony = st.sidebar.selectbox('Balcony',('1','2','3','4','5','6','7','8'))
parking = st.sidebar.selectbox('parking',('1','2','3','4','5'))
Lift = st.sidebar.selectbox('Lift',('0','1','2','3','4','5','6'))
neworold = st.sidebar.selectbox('neworold',('New Property','Resale'))
Furnished_status = st.sidebar.selectbox('Furnished_status',('Furnished','Semi Furnished','Unfurnished'))
type_of_building = st.sidebar.selectbox('type_of_building',('Flat','Individual House'))
Location = st.sidebar.selectbox('Location',("andheri","bandra","bhandup","bhayandar","borivali","chandivali","charkop","chembur","dadar",
    "dahisar","dombivli","ghatkopar","gorai","goregaon","jogeshwari","juhu","kalyan","kandivali","kanjurmarg","khar","kurla", "lokhandwala",
    "mahim","malad","marol","matunga","mira","mulund","mumbai","nalasopara","parel","powai","prabhadevi","santacruz","sion","thakur",
    "thane","ulhasnagar","vasai","versova","vikhroli","vile","virar","wadala","worli"))
   
user_input = {'area':area,'Bedrooms':Bedrooms,'Bathrooms':Bathrooms,'Balcony':Balcony,'parking':parking,'Lift':Lift,'neworold':neworold,
'Furnished_status':Furnished_status,'type_of_building':type_of_building,'Location':Location}

user_input_df = pd.DataFrame(user_input, index = [0])

# Function to Gets New input/Datapoint
def predict_price(area,Bedrooms,Bathrooms,Balcony,parking,Lift,neworold,Furnished_status,type_of_building,Location):    
    try:
        nro_index = data_columns.index(neworold)
    except:
        nro_index = -1

    try:
        fus_index = data_columns.index(Furnished_status)
    except:
        fus_index = -1

    try:
        tob_index = data_columns.index(type_of_building)
    except:
        tob_index = -1

    try:
        loc_index = data_columns.index(location)
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = area
    x[1] = Bedrooms
    x[2] = Bathrooms
    x[3] = Balcony
    x[4] = parking
    x[5] = Lift
    if nro_index >= 0:
        x[nro_index] = 1
    if fus_index >= 0:
        x[fus_index] = 1
    if [np.logical_and(tob_index > 0 , tob_index == 0)] :
        x[tob_index] = 1
    if loc_index >= 0:
        x[loc_index] = 1

    return round(loaded_model.predict([x])[0],2)


st.subheader('User Input parameters')
st.write(user_input_df)

#Prediction
Predicted = None

st.subheader('Predicted Price')
if st.button("Click Here to Predict"):
    Predicted = predict_price(area,Bedrooms,Bathrooms,Balcony,parking,Lift,neworold,Furnished_status,type_of_building,Location)
st.success('The Price of the House Will be: {}'.format(Predicted))



