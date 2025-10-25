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
    """
    Gets a Session from a session_id
    """    
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
    
def get_sessions():
    """
    Gets all Sessions
    """         
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Session;")
    result = cursor.fetchall()

    sessions = []

    for i in result:
        sessions.append(create_session(i))

    database.close()

    return sessions

def update_session_verified_at(session: Session):
    """
    Updates a Session's session_verified_at field
    """        
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Session SET last_verified_at = %s WHERE session_id = %s", (session.last_verified_at, session.session_id))
    
    database.commit()
    database.close()

def write_session(session: Session):
    """
    Writes a Session to the database
    """    

    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Session (session_id, id, account_type, secret_hash, created_at, last_verified_at) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (session.session_id, session.id, session.account_type, session.secret_hash, session.created_at, session.last_verified_at,))
    
    database.commit()
    database.close()
    
def delete_session(session_id: str):
    """
    Deletes a Session from the database from a session_id
    """        
    database = get_database()
    cursor = database.cursor()

    cursor.execute("DELETE FROM Session WHERE session_id = %s", (session_id,))
    database.commit()
    database.close()



##########
# ADMINS #
##########
def get_admin(admin_id: str):
    """
    Gets an Admin from an admin_id
    """        
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
    
def get_admins():
    """
    Gets all Admins
    """         
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Admin;")
    result = cursor.fetchall()

    admins = []

    for i in result:
        admins.append(create_admin(i))

    database.close()

    return admins
    
def get_admin_from_email(email: str):
    """
    Gets an Admin from an email
    """         
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
    
def update_admin(admin: Admin):
    """
    Updates an Admin from an Admin dataclass
    """         
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Admin SET first_name = %s, last_name = %s, email = %s WHERE admin_id = %s;", 
                           (admin.first_name, admin.last_name, admin.email, admin.admin_id))
    
    database.commit()
    database.close()    

def write_admin(admin: Admin):
    """
    Writes an Admin from an Admin dataclass
    """         
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Admin (admin_id, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)", 
                           (admin.admin_id, admin.first_name, admin.last_name, admin.email, admin.password))
    
    database.commit()
    database.close()        


##############
# CLINICIANS #
##############
def get_clinician(clinician_id: str):
    """
    Gets a Clinician from a clinician_id
    """         
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
    """
    Gets a Clinician from an email
    """         
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
    """
    Gets all Clinicians
    """         
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
    """
    Updates a Clinician from a Clinician dataclass
    """         
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Clinician SET first_name = %s, last_name = %s, email = %s WHERE clinician_id = %s;", 
                           (clinician.first_name, clinician.last_name, clinician.email, clinician.clinician_id))
    
    database.commit()
    database.close()    

def write_clinician(clinician: Clinician):
    """
    Writes a Clinician from a Clinician dataclass
    """         
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Clinician (clinician_id, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)", 
                           (clinician.clinician_id, clinician.first_name, clinician.last_name, clinician.email, clinician.password,))
    
    database.commit()
    database.close()

############
# PATIENTS #
############
def get_patient(patient_id: str):
    """
    Gets a Patient from a patient_id
    """         
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
    
def get_patient_from_email(email: str):
    """
    Gets a Patient from an email
    """         
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Patient WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_patient(result)
    else:
        database.close()
        return None    

def get_patients_from_clinician(clinician: Clinician):
    """
    Gets all Patients linked to a Clinician
    """      
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
    """
    Gets a Patient from a patient_id and a Clinician
    Ensures that the Clinician has access to the patient.
    """      
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
    """
    Gets all Patients.
    """      
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
    """
    Gets a Patient from a patient_id
    """      
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password, user_id, clinician_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (patient.patient_id, patient.first_name, patient.last_name, patient.height, patient.weight, patient.amputation_type, patient.prosthetic_type, patient.email, patient.password, patient.user_id, patient.clinician_id,))
    
    database.commit()
    database.close()    

def update_patient(patient: Patient):
    """
    Gets a Patient from a patient_id
    """      
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Patient SET first_name = %s, last_name = %s, height = %s, weight = %s, amputation_type = %s, prosthetic_type = %s, email = %s WHERE patient_id = %s;", 
                           (patient.first_name, patient.last_name, int(patient.height), int(patient.weight), patient.amputation_type, patient.prosthetic_type, patient.email, patient.patient_id))
    
    database.commit()
    database.close()        

##############
# ACTIVITIES #
##############
def get_activity(activity_id: str): 
    """
    Gets an Activity from an activity_id
    """          
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
    
def get_activities_from_patient_id(patient_id: str):
    """
    Gets all Activities connected to a patient
    """       
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Activity WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchall()

    activities = []

    for i in result:
        activities.append(create_activity(i))

    return activities


def get_activity_from_clinician(activity_id: str, clinician: Clinician):
    """
    Gets an activity from an activity_id and a Clinician
    Ensures clinician has access to activity
    """       
    patients = get_patients_from_clinician(clinician)
    database = get_database()
    cursor = database.cursor()
    for patient in patients:
        cursor.execute(
            "SELECT * FROM Activity WHERE activity_id = %s AND patient_id = %s",
            (activity_id, patient.patient_id,)
        )
        result = cursor.fetchone()
        if result:
            database.close()  
            return create_activity(result)
    database.close()          
    return None               


def get_activities():
    """
    Gets all Activities
    """       
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
    """
    Gets all Activities connected to a Clinician
    """       
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



def write_activity(activity: Activity):
    """
    Writes an Activity to the database from an Activity dataclass
    """           
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (activity.activity_id, activity.activity_type, activity.start_time, activity.end_time, activity.is_uploaded, activity.patient_id,))
    
    database.commit()
    database.close()       

##########
# SENSOR #
##########

def get_sensor(sensor_id: str):
    """
    Gets a Sensor from a sensor_id
    """           
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Sensor WHERE sensor_id = %s", (sensor_id,))
    result = cursor.fetchone()

    if result:
        database.close()
        return create_sensor(result)
    else:
        database.close()
        return None        
    
def get_sensors():
    """
    Gets all Sensors
    """         
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Sensor;")
    result = cursor.fetchall()

    sensors = []

    for i in result:
        sensors.append(create_sensor(i))

    database.close()

    return sensors

def get_sensors_from_patient_id(patient_id: str):
    """
    Gets all Sensors from a patient_id
    """       
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Sensor WHERE patient_id = %s", (patient_id,))
    result = cursor.fetchall()

    sensors = [create_sensor(i) for i in result]

    database.close()          
    return sensors
  

def write_sensor(sensor: Sensor):
    """
    Writes a Sensor to the database from a Sensor dataclass
    """           
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Sensor (sensor_id, patient_id, sensor_type, location_name, location_id, sensor_location_id, is_connected) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (sensor.sensor_id, sensor.patient_id, sensor.sensor_type, sensor.location_name, sensor.location_id, sensor.sensor_location_id, sensor.is_connected,))
    
    database.commit()
    database.close()         

#####################
# ACTIVITY READINGS #
#####################
def get_activity_readings():
    """
    Gets all ActivityReadings
    """         
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM ActivityReading;")
    result = cursor.fetchall()

    activity_readings = []

    for i in result:
        activity_readings.append(create_activity_reading(i))

    database.close()

    return activity_readings

def get_activity_readings_from_activity_id(activity_id: str):
    """
    Gets all ActivityReadings from an activity_id
    """           
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM ActivityReading WHERE activity_id = %s", (activity_id,))
    result = cursor.fetchall()

    activity_readings = [create_activity_reading(i) for i in result]

    database.close()          
    return activity_readings


def write_activity_reading(activity_reading: ActivityReading):
    """
    Writes an ActivityReading to the database from an ActivityReading dataclass
    """           
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO ActivityReading (activity_id, reading_series_id, sensor_id) VALUES (%s, %s, %s)", 
                           (activity_reading.activity_id, activity_reading.reading_series_id, activity_reading.sensor_id,))
    
    database.commit()
    database.close()         

#####################
# PRESSURE READINGS #
#####################
def get_pressure_readings():
    """
    Gets all PressureReadings
    """         
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM PressureReading;")
    result = cursor.fetchall()

    pressure_readings = []

    for i in result:
        pressure_readings.append(create_pressure_reading(i))

    database.close()

    return pressure_readings

def get_pressure_readings_for_activities(activity_id, patient_id):
    database = get_database()
    cursor = database.cursor()
    cursor.execute("""
        SELECT
            ar.reading_series_id,
            ar.sensor_id,
            s.location_name,
            s.sensor_type,
            pr.time,
            pr.pressure_value
        FROM Activity a
        INNER JOIN ActivityReading ar ON a.activity_id = ar.activity_id
        INNER JOIN Sensor s ON ar.sensor_id = s.sensor_id
        INNER JOIN PressureReading pr ON ar.reading_series_id = pr.reading_series_id
        WHERE a.activity_id = %s AND a.patient_id = %s
        ORDER BY ar.reading_series_id, pr.time ASC
    """, (activity_id, patient_id))

    result = cursor.fetchall()
    return result


def get_pressure_readings_from_reading_series_id(reading_series_id: str):
    """
    Gets all PressureReadings from a reading_series_id
    """               
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM PressureReading WHERE reading_series_id = %s ORDER BY time ASC;", (reading_series_id,))
    result = cursor.fetchall()

    pressure_readings = [create_pressure_reading(i) for i in result]

    database.close()        
    return pressure_readings


def write_pressure_reading(pressure_reading: PressureReading):
    """
    Writes a PressureReading to the database from a PressureReading dataclass
    """           
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, is_uploaded, reading_series_id) VALUES (%s, %s, %s, %s, %s)", 
                           (pressure_reading.pressure_reading_id, pressure_reading.pressure_value, pressure_reading.time, pressure_reading.is_uploaded, pressure_reading.reading_series_id,))
    
    database.commit()
    database.close()


#################
# XML Functions #
#################
def get_session_xml(session: Session):
    xml = ""

    xml += '\t<Session>\n\t\t<session_id>' + session.session_id + '</session_id>'
    xml += '\n\t\t<id>' + session.id + '</id>'
    xml += '\n\t\t<account_type>' + session.account_type + '</account_type>'
    xml += '\n\t\t<secret_hash>' + str(session.secret_hash) + '</secret_hash>'
    xml += '\n\t\t<created_at>' + str(session.created_at) + '</created_at>'
    xml += '\n\t\t<last_verified_at>' + str(session.last_verified_at) + '</last_verified_at>'
    xml += '\n\t</Session>'

    return xml    

def get_admin_xml(admin: Admin):
    xml = ""

    xml += '\t<Admin>\n\t\t<admin_id>' + admin.admin_id + '</admin_id>'
    xml += '\n\t\t<first_name>' + admin.first_name + '</first_name>'
    xml += '\n\t\t<last_name>' + admin.last_name + '</last_name>'
    xml += '\n\t\t<email>' + admin.email + '</email>'
    xml += '\n\t\t<password>' + admin.email + '</password>'
    xml += '\n\t</Admin>'

    return xml

def get_clinician_xml(clinician: Clinician):
    xml = ""

    xml += '\n\t<Clinician>\n\t\t<clinician_id>' + clinician.clinician_id + '</clinician_id>'
    xml += '\n\t\t<first_name>' + clinician.first_name + '</first_name>'
    xml += '\n\t\t<last_name>' + clinician.last_name + '</last_name>'
    xml += '\n\t\t<email>' + clinician.email + '</email>'
    xml += '\n\t\t<password>' + clinician.password + '</password>'
    xml += '\n\t</Clinician>'

    return xml

def get_patient_xml(patient: Patient):
    xml = ""

    xml += '\n\t<Patient>\n\t\t<patient_id>' + patient.patient_id + '</patient_id>'
    xml += '\n\t\t<first_name>' + patient.first_name + '</first_name>'
    xml += '\n\t\t<last_name>' + patient.last_name + '</last_name>'
    xml += '\n\t\t<height>' + patient.height + '</height>'
    xml += '\n\t\t<weight>' + patient.weight + '</weight>'
    xml += '\n\t\t<amputation_type>' + patient.amputation_type + '</amputation_type>'
    xml += '\n\t\t<prosthetic_type>' + patient.prosthetic_type + '</prosthetic_type>'
    xml += '\n\t\t<email>' + patient.email + '</email>'
    xml += '\n\t\t<password>' + patient.password + '</password>'
    xml += '\n\t\t<user_id>USER' + patient.user_id + '</user_id>'
    xml += '\n\t\t<clinician_id>' + patient.clinician_id + '</clinician_id>'
    xml += '\n\t</Patient>'

    return xml

def get_sensor_xml(sensor: Sensor):
    xml = ""

    xml += '\n\t<Sensor>\n\t\t<sensor_id>' + sensor.sensor_id + '</sensor_id>'
    xml += '\n\t\t<patient_id>' + sensor.patient_id + '</patient_id>'
    xml += '\n\t\t<sensor_type>' + str(sensor.sensor_type) + '</sensor_type>'
    xml += '\n\t\t<location_name>' + sensor.location_name + '</location_name>'
    xml += '\n\t\t<location_id>' + str(sensor.location_id) + '</location_id>'
    xml += '\n\t\t<sensor_location_id>' + sensor.sensor_location_id + '</sensor_location_id>'
    xml += '\n\t\t<is_connected>' + str(sensor.is_connected).upper() + '</is_connected>'
    xml += '\n\t</Sensor>'

    return xml

def get_activity_xml(activity: Activity):
    xml = ""

    xml += '\n\t<Activity>\n\t\t<activity_id>' + activity.activity_id + '</activity_id>'
    xml += '\n\t\t<activity_type>' + activity.activity_type + '</activity_type>'
    xml += '\n\t\t<start_time>' + str(activity.start_time) + '</start_time>'
    xml += '\n\t\t<end_time>' + str(activity.end_time) + '</end_time>'
    xml += '\n\t\t<is_uploaded>' + str(activity.is_uploaded).upper() + '</is_uploaded>'
    xml += '\n\t\t<patient_id>' + activity.patient_id + '</patient_id>'
    xml += '\n\t</Activity>'

    return xml

def get_activity_reading_xml(activity_reading: ActivityReading):
    xml = ""

    xml += '\n\t<ActivityReading>\n\t\t<activity_id>' + activity_reading.activity_id + '</activity_id>'
    xml += '\n\t\t<reading_series_id>' + activity_reading.reading_series_id + '</reading_series_id>'
    xml += '\n\t\t<sensor_id>' + activity_reading.sensor_id + '</sensor_id>'
    xml += '\n\t</ActivityReading>'  

    return xml

def get_pressure_reading_xml(pressure_reading: PressureReading):
    xml = ""

    xml += '\n\t<PressureReading>\n\t\t<pressure_reading_id>' + pressure_reading.pressure_reading_id + '</pressure_reading_id>'
    xml += '\n\t\t<pressure_value>' + str(pressure_reading.pressure_value) + '</pressure_value>'
    xml += '\n\t\t<time>' + str(pressure_reading.time) + '</time>'
    xml += '\n\t\t<is_uploaded>' + str(pressure_reading.is_uploaded).upper() + '</is_uploaded>'
    xml += '\n\t\t<reading_series_id>' + pressure_reading.reading_series_id + '</reading_series_id>'
    xml += '\n\t</PressureReading>'        

    return xml