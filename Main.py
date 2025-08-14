import streamlit as st
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


model = load_model(r'TrainingModel\insurance_model.h5', compile=False)

# Load dataset for encoders/scaler
data = pd.read_csv(r"TrainingModel\Medical_insurance.csv")

# Prepare label encoders
encoders = {}
for col in ['sex', 'smoker', 'region']:
    le = LabelEncoder()
    le.fit(data[col])
    encoders[col] = le

# Prepare scaler
X = data.drop('charges', axis=1).copy()   
for col in ['sex', 'smoker', 'region']:
    X[col] = encoders[col].transform(X[col])

scaler = StandardScaler()
scaler.fit(X)


# Prediction function
def predict_insurance(age, sex, bmi, children, smoker, region):
    sex_encoded = encoders['sex'].transform([sex])[0]
    smoker_encoded = encoders['smoker'].transform([smoker])[0]
    region_encoded = encoders['region'].transform([region])[0]
    
    input_array = np.array([[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]])
    input_scaled = scaler.transform(input_array)
    
    prediction = model.predict(input_scaled, verbose=0)[0][0]
    return prediction

# Streamlit UI
st.title(" Health Insurance Price Prediction")

age = st.number_input("Age", min_value=0, max_value=100, value=29)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=26.5)
children = st.number_input("Children", min_value=0, max_value=10, value=1)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])

if st.button("Predict"):
    price = predict_insurance(age, sex, bmi, children, smoker, region)
    st.success(f"💰 Estimated Insurance Price: ₹{price:,.2f}")
