import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.models import load_model
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load .env variables including GROQ_API_KEY
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Load model and data
model = load_model(r'TrainingModel/insurance_model.h5', compile=False)
data = pd.read_csv(r"TrainingModel/Medical_insurance.csv")
plans_df = pd.read_csv("Company data.csv", encoding="cp1252")

# Prepare encoders
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

def predict_insurance(age, sex, bmi, children, smoker, region):
    sex_encoded = encoders['sex'].transform([sex])[0]
    smoker_encoded = encoders['smoker'].transform([smoker])[0]
    region_encoded = encoders['region'].transform([region])[0]
    input_array = np.array([[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]])
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled, verbose=0)[0][0]
    return prediction

def filter_plans(plans_df, price):
    filtered = []
    for _, row in plans_df.iterrows():
        try:
            low, high = [int(x.replace("k", "000").replace("₹", "").strip()) for x in row["Premium Range"].split("–")]
            if low <= price <= high:
                filtered.append(row)
        except:
            pass
    return pd.DataFrame(filtered) if filtered else plans_df

def plans_to_text(df):
    return df[['Company', 'Plan Name', 'Sum Insured', 'Premium Range', 'Key Features/USP']].to_string(index=False)

# Initialize Groq LLM
if not groq_api_key:
    raise ValueError("Groq API Key not found. Please add it to your .env file.")

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.9,
    api_key=groq_api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", '''
You are a helpful insurance advisor. Given a list of insurance plans and a user's estimated budget:
- Compare ALL given plans against the user's budget.
- Rank by closeness to budget and feature relevance.
- Select TWO different plans that best fit the budget.
- Format your response like this:
1. [Plan Name] ([Price range])
   - Feature/USP 1
   - Feature/USP 2
2. [Plan Name] ([Price range])
   - Feature/USP 1
   - Feature/USP 2
Do NOT return JSON. Use only clear Markdown bullet points.'''),
    ("user", "Plans:\n{plans}\nUser Budget: ₹{price}")
])

chain = prompt | llm

def get_groq_recommendations(price):
    filtered_df = filter_plans(plans_df, price)
    plans_text = plans_to_text(filtered_df)
    result = chain.invoke({"plans": plans_text, "price": int(price)})
    return result.content
