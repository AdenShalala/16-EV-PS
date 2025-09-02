from dotenv import load_dotenv
import mysql.connector
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'classes'))
from Patient import Patient # pyright: ignore[reportMissingImports]
from Activity import Activity # pyright: ignore[reportMissingImports]
from Sensor import Sensor # pyright: ignore[reportMissingImports]
from Clinician import Clinician # pyright: ignore[reportMissingImports]
from PressureReading import PressureReading as PreRe # pyright: ignore[reportMissingImports]

load_dotenv()


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Database Init     #
#~~~~~~~~~~~~~~~~~~~~~~~#

def database_connect(): 
    load_dotenv(override=True)
    database = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )

    return database

#~~~~~~~~~~~~~~~~~~~~~~~#
#      Constructors     #
#~~~~~~~~~~~~~~~~~~~~~~~#

def create_sensor(result, readings):
    return Sensor(*result, readings)

def create_activity(result, sensors):
    return Activity(*result, sensors)

def create_patient(result, activities):
    return Patient(*result, activities)

def create_clinician(result):
    return Clinician(*result)

def create_reading(result):
    return PreRe(*result)

#~~~~~~~~~~~~~~~~~~~~~~~#
#  Read by clinician ID #
#~~~~~~~~~~~~~~~~~~~~~~~#

def read_patients_by_clinician_id(clinician_id: str):
    db = database_connect()
    cursor = db.cursor()

    cursor.execute("SELECT patient_id FROM Patient WHERE clinician_id = %s;", (clinician_id,))

    patient_id_list = cursor.fetchall()

    if patient_id_list is None:
        return None
    patients = list()
    #
    #LOOPING PATIENT IDS
    #
    for patient_id in patient_id_list:
        cursor.execute("SELECT activity_id FROM Activity WHERE patient_id = %s;", (patient_id[0],))
        patient_activity_list = cursor.fetchall()
        activities = list()
        #
        #LOOPING ACTIVITY IDS
        #
        for activity_id in patient_activity_list:
            cursor.execute("SELECT sensor_id FROM Sensor WHERE activity_id = %s;", (activity_id[0],))
            activity_sensor_list = cursor.fetchall()
            sensors = list()
            #
            #LOOPING SENSOR IDS
            #
            for sensor_id in activity_sensor_list:
                cursor.execute("SELECT pressure_value, time, sensor_type, pressure_reading_id, activity_id, sensor_id FROM PressureReading WHERE sensor_id = %s ORDER BY time;", (sensor_id[0], ))
                readings = list()
                results = cursor.fetchall()
                for result in results:
                    readings.append(create_reading(result))
                
                cursor.execute("SELECT sensor_id, location_name, sensor_location_id, sensor_type FROM Sensor where sensor_id = %s;", (sensor_id[0],))
                result = cursor.fetchone()
                sensor_list = (result[0], result[1], result[2], result[3])
                sensors.append(create_sensor(sensor_list, readings))
            cursor.execute("SELECT activity_type, start_time, end_time, activity_id FROM Activity WHERE activity_id = %s;", (activity_id[0],))
            result = cursor.fetchone()
            activity_list = (result[0], result[1], result[2], result[3])
            activities.append(create_activity(activity_list, sensors))
        cursor.execute("SELECT first_name, last_name, height, weight, amputation_type, prosthetic_type, email, patient_id, clinician_id FROM Patient where patient_id = %s;", (patient_id[0],))
        result = cursor.fetchone()
        patient_list = (result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8])
        patients.append(create_patient(patient_list, activities)) 
    db.close()
    return patients
