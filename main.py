import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

model = joblib.load('mental_health_model.pkl')
top_countries = ['Other','India','USA','Canada','Australia','UK','Germany','Mexico','Turkey','France']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#A first Pydantic Model
class StudentData(BaseModel):
    age                     : int = Field(..., ge=10, le=100)
    gender                  : Literal['Male', 'Female']
    country                 : str
    academic_level          : Literal['Undergraduate', 'Graduate', 'High School']
    most_used_platform      : Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat','Twitter','YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp','WeChat']
    purpose_of_use          : Literal['Networking', 'Education', 'Entertainment', 'News']
    avg_daily_usage_hours   : float = Field(..., ge=0, le=24)
    daily_unlocks           : int   = Field(..., ge=0)
    study_hours             : float = Field(..., ge=0, le=24)
    physical_activity_hours : float = Field(..., ge=0, le=24)
    sleep_hours_per_night   : float = Field(..., ge=0, le=24)
    stress_level            : Literal['Medium', 'Low', 'Very High', 'High']




# Describe what we send back
class PredictionResponse(BaseModel):
    predicted_mental_health_score:float
    #6.777777 -> float


@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.get("/script.js")
def read_script():
    return FileResponse("script.js")

@app.get("/style.css")
def read_style():
    return FileResponse("style.css")


@app.post('/predict', response_model=PredictionResponse) #6.77777
def predict(data: StudentData):
   
   # Case-insensitive mapping and normalization
   country_clean = data.country.strip()
   country_map = {
       "united states": "USA",
       "united states of america": "USA",
       "us": "USA",
       "usa": "USA",
       "united kingdom": "UK",
       "uk": "UK",
       "gb": "UK",
       "great britain": "UK",
   }
   clean_lower = country_clean.lower()
   if clean_lower in country_map:
       country_group = country_map[clean_lower]
   else:
       matched = [c for c in top_countries if c.lower() == clean_lower]
       if matched:
           country_group = matched[0]
       else:
           country_group = "Other"

   input_row = pd.DataFrame([{
        'Study_Hours'               :data.study_hours,
        'Age'                       :data.age,
        'Avg_Daily_Usage_Hours'     :data.avg_daily_usage_hours,
        'Daily_Unlocks'             :data.daily_unlocks,
        'Physical_Activity_Hours'   :data.physical_activity_hours,
        'Sleep_Hours_Per_Night'     :data.sleep_hours_per_night,
        'Stress_Level'              :data.stress_level,
        'Gender'                    :data.gender,
        'Academic_Level'            :data.academic_level,
        'Most_Used_Platform'        :data.most_used_platform,
        'Purpose_Of_Use'            :data.purpose_of_use,
        'grouped_country'           :country_group
   }])

   prediction = model.predict(input_row)[0] #6.77
   return PredictionResponse(predicted_mental_health_score=round(float(prediction),2))