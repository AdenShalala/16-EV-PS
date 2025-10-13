from dotenv import load_dotenv
import mysql.connector
import os
import sys

from schema import *

load_dotenv()

# top level functions
def get_database():
    load_dotenv(override=True)
    database = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )

    return database

def drop():
    database = get_database()
    cursor = database.cursor()

    with open(os.path.join(os.path.dirname(__file__), "sql/drop.sql"),  'r') as f:
        cursor.execute(f.read())

   # database.commit() 
    database.close()

def create():
    # create the initial database
    load_dotenv(override=True)
    database = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT')
    )

    cursor = database.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + str(os.getenv('MYSQL_DATABASE')) + '')
    cursor.execute("USE " + str(os.getenv('MYSQL_DATABASE')) + '')
    # database.close()

    # # re open database
    # database = get_database()
    # cursor = database.cursor()

    with open(os.path.join(os.path.dirname(__file__), "sql/create.sql"),  'r') as f:
        cursor.execute(f.read())

    #database.commit() 
    database.close()

def populate():
    database = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )
    
    with open(os.path.join(os.path.dirname(__file__), "sql/populate.sql"),  'r') as f:
        sql_script = f.read()
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                cursor = database.cursor()
                cursor.execute(statement + ';')
                cursor.close()
        
    path = os.path.join(os.path.dirname(__file__), "sql/patients/")    
    for sql in os.listdir(path):
        full_path = os.path.join(path, sql)
        with open(full_path) as f:
            for statement in f.read().split(';'):
                statement = statement.strip()
                if statement:
                    cursor = database.cursor()
                    cursor.execute(statement + ';')
                    cursor.close()

    database.commit()
    database.close()
    

# constructor candy
# realistically these could be one liners in code but id like them to be functions
# in case we need to add other stuff later :P
def create_session(result):
    return Session(*result)

def create_admin(result):
    return Admin(*result)

def create_clinician(result):
    return Clinician(*result)

def create_patient(result):
    return Patient(*result)

def create_activity(result):
    return Activity(*result)

def create_sensor(result):
    return Sensor(*result)

def create_pressure_reading(result):
    return PressureReading(*result)

def create_activity_reading(result):
    return ActivityReading(*result)

############
# SESSIONS #
############
def get_session(session_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Session WHERE session_id = %s", (session_id,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_session(result)
    else:
        database.close()
        return None

def update_session_verified_at(session: Session):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Session SET last_verified_at = %s WHERE session_id = %s", (session.last_verified_at, session.session_id))
    
    database.commit()
    database.close()

def write_session(session: Session):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Session (session_id, id, account_type, secret_hash, created_at, last_verified_at) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (session.session_id, session.id, session.account_type, session.secret_hash, session.created_at, session.last_verified_at,))
    
    database.commit()
    database.close()
    
def delete_session(session_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("DELETE FROM Session WHERE session_id = %s", (session_id,))
    database.commit()
    database.close()



##########
# ADMINS #
##########
def get_admin(admin_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Admin WHERE admin_id = %s", (admin_id,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_admin(result)
    else:
        database.close()
        return None
    
def get_admin_from_email(email: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Admin WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_admin(result)
    else:
        database.close()
        return None

##############
# CLINICIANS #
##############
def get_clinician(clinician_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Clinician WHERE clinician_id = %s", (clinician_id,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_clinician(result)
    else:
        database.close()
        return None
    
def get_clinician_from_email(email: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Clinician WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_clinician(result)
    else:
        database.close()
        return None

def get_clinicians():
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Clinician;")
    result = cursor.fetchall()

    clinicians = []

    for i in result:
        clinicians.append(create_clinician(i))

    database.close()

    return clinicians

def update_clinician(clinician: Clinician):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Clinician (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                           (clinician.first_name, clinician.last_name, clinician.email, clinician.password))
    
    database.commit()
    database.close()    

def write_clinician(clinician: Clinician):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Clinician (clinician_id, first_name, last_name, email, password, created_at) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (clinician.clinician_id, clinician.first_name, clinician.last_name, clinician.email, clinician.password, datetime.now(),))
    
    database.commit()
    database.close()

############
# PATIENTS #
############
def get_patient(patient_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Patient WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_patient(result)
    else:
        database.close()
        return None

def get_patients_from_clinician(clinician: Clinician):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Patient WHERE clinician_id = %s", (clinician.clinician_id,))
    result = cursor.fetchall()

    patients = []

    for i in result:
        patients.append(create_patient(i))

    database.close()

    return patients

# ensures the patient is from a clinician
def get_patient_from_clinician(patient_id: str, clinician: Clinician):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Patient WHERE patient_id = %s AND clinician_id = %s", (patient_id, clinician.clinician_id))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_patient(result)
    else:
        database.close()
        return None

def get_patients():
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Patient;")
    result = cursor.fetchall()

    patients = []

    for i in result:
        patients.append(create_patient(i))

    database.close()

    return patients

def write_patient(patient: Patient):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password, user_id, clinician_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (patient.patient_id, patient.first_name, patient.last_name, patient.height, patient.weight, patient.amputation_type, patient.prosthetic_type, patient.email, patient.password, patient.user_id, patient.clinician_id,))
    
    database.commit()
    database.close()    

##############
# ACTIVITIES #
##############
def get_activity(activity_id: str): 
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Activity WHERE activity_id = %s", (activity_id,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_activity(result)
    else:
        database.close()
        return None    
    
def get_activity_from_patient(patient_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Activity WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchall()

    activities = []

    for i in result:
        activities.append(create_activity(i))

    database.close()

    return activities

def get_activity_from_clinician(activity_id: str, clinician: Clinician):
    patients = get_patients_from_clinician(clinician)

    database = get_database()
    cursor = database.cursor()

    for patient in patients:
        cursor.execute("SELECT * FROM Activity WHERE activity_id = %s AND patient_id = %s", (activity_id, patient.patient_id,))
        result = cursor.fetchone()

        if result:
            database.close()
            return create_activity(result)

def get_activities():
    database = get_database()
    cursor = database.cursor()

    activities = []

    cursor.execute("SELECT * FROM Activity;")
    result = cursor.fetchall()

    for i in result:
        activities.append(create_activity(i))

    database.close()

    return activities

def get_activities_from_clinician(clinician: Clinician):
    patients = get_patients_from_clinician(clinician)

    database = get_database()
    cursor = database.cursor()

    activities = []

    for patient in patients:
        cursor.execute("SELECT * FROM Activity WHERE patient_id = %s", (patient.patient_id,))
        result = cursor.fetchall()

        for i in result:
            activities.append(create_activity(i))

    database.close()

    return activities

def get_activities_from_patient_id(patient_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Activity WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchall()

    activities = []

    for i in result:
        activities.append(create_activity(i))

    return activities

def write_activity(activity: Activity):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (activity.activity_id, activity.activity_type, activity.start_time, activity.end_time, activity.is_uploaded, activity.patient_id,))
    
    database.commit()
    database.close()       

#####################
# ACTIVITY READINGS #
#####################
def get_readings_from_activity_id(activity_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM ActivityReading WHERE activity_id = %s", (activity_id,))
    result = cursor.fetchall()

    activities = []

    for i in result:
        activities.append(create_activity_reading(i))

    return activities

#####################
# PRESSURE READINGS #
#####################


###################
# SENSOR READINGS #
###################