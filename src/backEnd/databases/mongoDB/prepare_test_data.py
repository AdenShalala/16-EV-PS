# for testing only
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from datetime import datetime

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('MONGO_DB', 'test_db')]

# clear old test data
db.Patient.delete_many({})
db.Activity.delete_many({})
db.Sensor.delete_many({})


db.Patient.insert_one({
    "patientID": "p001",
    "clinicianID": "c123",
    "birthDate": datetime(1980, 5, 1),
    "gender": "M",
    "height": 175.0,
    "weight": 70.0,
    "amputationType": "transfemoral",
    "socketType": "typeA",
    "prosthesisStartDate": datetime(2020, 1, 1),
    "hoursPerWeek": 10,
    "distancePerWeek": 20.3
})

db.Activity.insert_many([
    {
        "activityID": "a100",
        "patientID": "p001",
        "startTime": datetime(2025,7,1,9,0),
        "endTime": datetime(2025,7,1,10,0),
        "type": "walking"
    },
    {
        "activityID": "a101",
        "patientID": "p001",
        "startTime": datetime(2025,7,2,14,0),
        "endTime": datetime(2025,7,2,15,0),
        "type": "running"
    }
])

db.Sensor.insert_many([
    {
        "sensorID": "s1",
        "activityID": "a100",
        "location": "foot",
        "type": "pressure",
        "pressureTolerance": 5.0,
        "timestamps": [0.0, 0.5, 1.0],
        "signals": [12.1, 13.5, 11.8],
        "pointsOfInterest": [1]
    },
    {
        "sensorID": "s2",
        "activityID": "a101",
        "location": "knee",
        "type": "angle",
        "pressureTolerance": 0.0,
        "timestamps": [0.0, 0.2, 0.4],
        "signals": [30, 35, 33],
        "pointsOfInterest": [2]
    }
])

print("test data inserted")