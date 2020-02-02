# McHacks7 code for the BayMax virtual assistant
    # A mental health chatbot designed and implemented in the Voiceflow API
    # Helps guide those who phone a hotline through questions that volunteers
    # are required to ask by protocol, and records the responses to present
    # to the volunteer before they take the call from the virtual assistant

import pprint
pp = pprint.PrettyPrinter()

# Responses are exported from Voice Flow to Google Sheets
# Importing libraries required for reading the responses from Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Importing natural language processing libraries from IBM Watson
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

# Authenticating credentials to access Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('mchacks7-9018ad3b5276.json', scope)
client = gspread.authorize(creds)

# Accessing the data from the spreadsheet in a Python readable structure (list of dicts)
MHdataSheet = client.open('Mental_health_Database').sheet1
mentalHealthData = MHdataSheet.get_all_records()

# Receiving the input from the latest user to further analyze with IBM Watson's natural language processing service
mostRecentUser = mentalHealthData.pop()

# Authenticating access to IBM Watson
authenticator = IAMAuthenticator('1jplXA1AMzd3rlm3cRE-Nws1AwATXKe1cS7PUfY_dS8M')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8ac78265-c41b-45ea-8bc3-6942e96e3d63')

# Using Watson to process description of current mental state given by current user of virtual assistant
watsonAnalysis = natural_language_understanding.analyze(text=mostRecentUser['Description'], features=Features(emotion=EmotionOptions())).get_result()
emotionLevels = watsonAnalysis['emotion']['document']['emotion']
Row = mostRecentUser['Row']

# Printing output for volunteer who will be picking up the call
print('I am detecting these levels of emotions from the current caller')
pp.pprint(emotionLevels)

MHdataSheet.update_cell(Row, 9, emotionLevels['anger'])
MHdataSheet.update_cell(Row, 10, emotionLevels['disgust'])
MHdataSheet.update_cell(Row, 11, emotionLevels['fear'])
MHdataSheet.update_cell(Row, 12, emotionLevels['joy'])
MHdataSheet.update_cell(Row, 13, emotionLevels['sadness'])


# Using IBM Watson's emotion level outputs and the individual's own distress level rating
# we are going to generate a risk-factor that we can use as the response variable in our
# machine learning model that we will train to recognize individual's at greater risk
# of severe symptoms of mental illnesses based on the responses given to the demographic
# based question

import tensorflow as tf
from tensorflow import keras
import sklearn
from sklearn import linear_model
from sklearn import preprocessing
import numpy as np
import pandas as pd
from pandas import DataFrame
import csv

riskModelData = DataFrame(MHdataSheet.get_all_values())
riskModelData.columns = riskModelData.iloc[0]
riskModelData = riskModelData.drop(labels=['Row', 'Emergency', 'Description', 'Diagnosis'], axis=1).drop(labels=0)
pp.pprint(riskModelData)