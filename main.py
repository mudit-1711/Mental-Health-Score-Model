import joblib
from fastapi import FastAPI
model = joblib.load('mental_health_model.pkl')
app = FastAPI() 

@app.post('/predict')
def predict(data):
    input_row = {
        'Age',
        'Gender',
        'Country',
        'Academic_Level',
        'Most_Used_Platform',
        'Purpose_Of_Use',
        'Avg_Daily_Usage_Hours',
        'Daily_Unlocks',
        'Study_Hours',
        'Physical_Activity_Hours',
        'Sleep_Hours_Per_Night',
        'Stress_Level',
        'Mental_Health_Score',
        'grouped_country'
    }
