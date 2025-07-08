from dotenv import load_dotenv
import mysql.connector
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Patient import Patient
from Activity import Activity
from Sensor import Sensor

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

    cursor.execute("SELECT patient_id FROM Patient WHERE clinician_id = %s;", (clinician_id,))

    patient_id_list = cursor.fetchall()

    if patient_id_list is None:
        return None
    
    for patient_id in patient_id_list:
        cursor.execute("SELECT activity_id FROM Activity WHERE patient_id = %s;", (patient_id[0],))
        patient_activity_list = cursor.fetchall()

        for activity_id in patient_activity_list:
            cursor.execute("SELECT sensor_id FROM Sensor WHERE activity_id = %s;", (activity_id[0],))
            activity_sensor_list = cursor.fetchall()

            for sensor_id in activity_sensor_list:
                cursor.execute("SELECT time_stamp FROM Timestamp WHERE sensor_id = %s ORDER BY sequence_number;", (sensor_id[0],))
                activity_timestamps = cursor.fetchall()
                cursor.execute("SELECT signal_output FROM Sensor_signal WHERE sensor_id = %s ORDER BY sequence_number;", (sensor_id[0],))
                activity_signals = cursor.fetchall()
                cursor.execute("SELECT point_of_interest_time_stamp FROM Point_of_interest WHERE sensor_id = %s;", (sensor_id[0],))
                activity_pois = cursor.fetchall()
                print("_"*20 + f"\nActivity: {activity_id} | Sensor: {sensor_id}\n")
                for stamp in activity_timestamps:
                    print(f"{float(stamp[0]):.2f}", end=" ")
                for sig in activity_signals:
                    print(f"{float(sig[0]):.2f}", end=" ")
                for poi in activity_pois:
                    print(float(poi[0]), end=" ")
                print()

read_patients_by_clinician_id("CLIN402")