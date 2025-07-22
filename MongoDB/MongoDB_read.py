from dotenv import load_dotenv
import os
from pymongo import MongoClient
import sys
from datetime import datetime

# class files are under src folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from Patient import Patient
from Activity import Activity
from Sensor import Sensor

load_dotenv()

def database_connect():
    uri = os.getenv('MONGO_URI')
    db_name = os.getenv('MONGO_DB', 'clinical_db')
    client = MongoClient(uri)
    return client[db_name]

# create objects
def create_sensor(sensor_doc):
    return Sensor(
        location=sensor_doc.get("location", ""),
        type=sensor_doc.get("type", ""),
        pressure_tolerance=sensor_doc.get("pressureTolerance", 0.0),
        signal=sensor_doc.get("signals", []),
        timestamp=sensor_doc.get("timestamps", []),
        points_of_interest=sensor_doc.get("pointsOfInterest", [])
    )

def create_activity(activity_doc, sensors):
    return Activity(
        end_time=activity_doc.get("endTime"),
        start_time=activity_doc.get("startTime"),
        type=activity_doc.get("type", ""),
        sensors=sensors
    )

def create_patient(patient_doc, activities):
    return Patient(
        clinician_id=patient_doc.get("clinicianID", ""),
        month_year_birth=patient_doc.get("birthDate"),
        gender=patient_doc.get("gender", ""),
        height=patient_doc.get("height", 0.0),
        weight=patient_doc.get("weight", 0.0),
        amputation_type=patient_doc.get("amputationType", ""),
        socket_type=patient_doc.get("socketType", ""),
        first_fitting=patient_doc.get("prosthesisStartDate"),
        hours_per_week=patient_doc.get("hoursPerWeek", 0),
        distance_per_week=patient_doc.get("distancePerWeek", 0.0),
        activities=activities
    )


def read_patients_by_clinician_id(clinician_id: str):
    db = database_connect()
    patients = []

    #read patient documents
    for patient_doc in db.Patient.find({"clinicianID": clinician_id}):
        activities = []
        
        for activity_doc in db.Activity.find({"patientID": patient_doc["patientID"]}):
            sensors = []
            
            for sensor_doc in db.Sensor.find({"activityID": activity_doc["activityID"]}):
                sensors.append(create_sensor(sensor_doc))
            
            activities.append(create_activity(activity_doc, sensors))
        
        patients.append(create_patient(patient_doc, activities))
    
    return patients