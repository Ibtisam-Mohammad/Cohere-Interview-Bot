# Importing the modules
import streamlit as st
import re, pickle
import requests
import base64

API_KEY = 'KGJW6F2pb5VF9SdqaAfNyaGYQvpgYd0e' # Enter your API key

#################-------Accessing AMAZON API using RapidAPI :( -------###################

def amazon(keyword):
    url = "https://amazon-price1.p.rapidapi.com/search"
    querystring = {"keywords":keyword,"marketplace":"US"}    #Entering a search term
    headers = {
        "X-RapidAPI-Key": "bf01ff72c8msh1b3ca45edb53363p17a716jsn9c85a919b8ee",
        "X-RapidAPI-Host": "amazon-price1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()      # getting the response


#################------- Finding the Laptop using Jurassic-1 Grande Instruct -------###################

def find_laptop(pre_prompt):
    response=requests.post("https://api.ai21.com/studio/v1/experimental/j1-grande-instruct/complete",
    headers={"Authorization": f"Bearer {API_KEY}"},
            # Some prompt
    json={
        "prompt": f"If the laptop is not in the context, answer \"NONE\".\nContext: This laptop is from Asus, the ROG Strix GL502VM. It has Windows 10, a full HD 15.6 inch display for viewing streaming content in good quality and 8th Gen Intel Core I7 processor combined with 16 GB of RAM for fast browsing.\nQuestion: Get the name of laptop from above context.\nAnswer: Asus ROG Strix GL502VM\n--\nIf the laptop is not in the context, answer \"NONE\".\nContext: What about Lenovo, the Ideapad 330. It has Windows 10, a full HD 15.6 inch display for viewing streaming content in good quality and 8th Gen Intel Core I7 processor combined with 8 GB of RAM for fast browsing.\nQuestion: Get the name of laptop from above context.\nAnswer: Lenovo Ideapad 330\n--\nIf the laptop is not in the context, answer \"NONE\".\nContext: This laptop is just for office work, not for gaming or editing.\nQuestion: Get the name of laptop from above context.\nAnswer:\n--\nIf the laptop is not in the context, answer \"NONE\".\nContext: {pre_prompt}\nAnswer:",
        "numResults": 1,
        "maxTokens": 12,
        "temperature": 0,
        "topKReturn": 0,
        "topP":0.01,
        "countPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "frequencyPenalty": {
            "scale": 0,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
        },
        "presencePenalty": {
            "scale": 0.45,
            "applyToNumbers": False,
            "applyToPunctuations": False,
            "applyToStopwords": False,
            "applyToWhitespaces": False,
            "applyToEmojis": False
      },
      "stopSequences":["--"]
    }
)   
    print('-------'+response.json()['completions'][0]['data']['text'])
    if len(response.json()['completions'][0]['data']['text'])>6:   # The model sometimes outputs the laptops it knows or are in the previous answers so setting some limit
        return amazon(response.json()['completions'][0]['data']['text'])


#################------- Setting Background Image (Help from Streamlit forum + Stackoverflow) -------###################

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    opacity:1.0;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


#------|||||||||||||||||||||| END ||||||||||||||||||||||--------#
