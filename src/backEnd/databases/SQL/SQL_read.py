from dotenv import load_dotenv
import mysql.connector
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'classes'))
from Patient import Patient
from Activity import Activity
from Sensor import Sensor

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

    cursor.execute("SELECT patient_id FROM Patient WHERE clinician_id = %s;", (clinician_id,))

    patient_id_list = cursor.fetchall()

    if patient_id_list is None:
        return None
    patients = list()
    for patient_id in patient_id_list:
        cursor.execute("SELECT activity_id FROM Activity WHERE patient_id = %s;", (patient_id[0],))
        patient_activity_list = cursor.fetchall()
        activities = list()
        for activity_id in patient_activity_list:
            cursor.execute("SELECT sensor_id FROM Sensor WHERE activity_id = %s;", (activity_id[0],))
            activity_sensor_list = cursor.fetchall()
            sensors = list()
            for sensor_id in activity_sensor_list:
                cursor.execute("SELECT time_stamp FROM Timestamp WHERE sensor_id = %s ORDER BY sequence_number;", (sensor_id[0],))
                activity_timestamps = cursor.fetchall()
                cursor.execute("SELECT signal_output FROM Sensor_signal WHERE sensor_id = %s ORDER BY sequence_number;", (sensor_id[0],))
                activity_signals = cursor.fetchall()
                cursor.execute("SELECT point_of_interest_time_stamp FROM Point_of_interest WHERE sensor_id = %s;", (sensor_id[0],))
                activity_pois = cursor.fetchall()
                for i in range(len(activity_timestamps)):
                    activity_timestamps[i] = round(float(activity_timestamps[i][0]), 1)
                    activity_signals[i] = float(activity_signals[i][0])
                for i in range(len(activity_pois)):
                    activity_pois[i] = float(activity_pois[i][0])
                cursor.execute("SELECT * FROM Sensor where sensor_id = %s;", (sensor_id[0],))
                result = cursor.fetchone()
                sensor_list = (result[0], result[2], result[3], result[4], activity_signals, activity_timestamps, activity_pois)
                sensors.append(create_sensor(sensor_list))
            cursor.execute("SELECT * FROM Activity WHERE activity_id = %s;", (activity_id[0],))
            result = cursor.fetchone()
            activity_list = (result[0], result[2], result[3], result[4])
            activities.append(create_activity(activity_list, sensors))
        cursor.execute("SELECT patient_id, clinician_id, month_year_birth, gender, height, weight, amputation_type, socket_type, first_fitting, hours_per_week, distance_per_week FROM Patient where patient_id = %s;", (patient_id[0],))
        result = cursor.fetchone()
        patient_list = (result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10])
        patients.append(create_patient(patient_list, activities)) 
    db.close()
    return patients