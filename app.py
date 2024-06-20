# app.py
import streamlit as st
import mlflow.pyfunc
import yaml
import warnings
from openai import OpenAI
import openai
import os

client = OpenAI()
warnings.filterwarnings('ignore')
deployment_name = "gpt-3.5-turbo"

# Load model URI from config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
model_name = config['model_name']
model_version = str(config['latest_version'])
mlflow.set_tracking_uri(config["tracking_uri"])

@st.cache(allow_output_mutation=True)
def load_model():
    return mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")

model = load_model()

st.title('Model Prediction')

# User input
content = st.text_input('Enter review')
#st.write('you entered: ',content)
if content:
    data = [{'role': 'user', 'content': content}]
    #st.write('Data:', data)
    prediction = model.predict(data)
    st.write('Prediction: ', prediction)