from dotenv import load_dotenv
import mysql.connector
import os
from src.Patient import Patient
from src.Activity import Activity
from src.Sensor import Sensor

load_dotenv()

#~~~~~~~~~~~~~~~~~~~~~~~#
#      Database Init    #
#~~~~~~~~~~~~~~~~~~~~~~~#

def database_connect(): 
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

def create_sensor(result):
    return Sensor(*result)

def create_activity(result, sensors):
    return Activity(*result, sensors)

def create_patient(result, activities):
    return Patient(*result, activities)

#~~~~~~~~~~~~~~~~~~~~~~~#
#  Read by clinician ID #
#~~~~~~~~~~~~~~~~~~~~~~~#

def read_patients_by_clinician_id(clinician_id: str):
    db = database_connect()
    cursor = db.cursor()

    cursor.execute("SELECT user_id FROM User WHERE clinician_id = %s;", (clinician_id,))

    patient_id_list = cursor.fetchall()

    if patient_id_list is None:
        return None
    
    for patient_id in patient_id_list:
        cursor.execute("SELECT activity_id FROM Actiity WHERE user_id = %s;", (patient_id,))
        patient_activity_list = cursor.fetchall()

        for activity_id in patient_activity_list:
            cursor.execute("SELECT sensor_id FROM Sensor WHERE activity_id = %s;", (activity_id,))
            activity_sensor_list = cursor.fetchall()

            for sensor_id in activity_sensor_list:
                cursor.execute("SELECT time_stamp FROM Timestamp WHERE sensor_id = %s")
