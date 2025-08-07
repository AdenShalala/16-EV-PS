import mysql.connector as sql
from xml.dom.minidom import parseString
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

# Accepts xml content as a parameter to parse and insert into the database
def create_database(xml_content: str):
    # Connect to the database
    database = sql.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT')
    )
    cursor = database.cursor()

    cursor.execute("DROP DATABASE IF EXISTS " + str(os.getenv('MYSQL_DATABASE')) + ';')

    # Create database
    cursor.execute("CREATE DATABASE " + str(os.getenv('MYSQL_DATABASE')) + ';')

    # Use CSIT321
    cursor.execute("USE " + str(os.getenv('MYSQL_DATABASE')) + ';')

    # Create tables
    with open(os.path.join(os.path.dirname(__file__), "Create.sql"),  'r') as f:
        cursor.execute(f.read())

    database.close()

    print("Parsing XML from uploaded xml file")

    database = sql.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )

    # added parseString to parse the content of uploaded xml file content which is a string.
    dom = parseString(xml_content)
    users = dom.getElementsByTagName('Users')[0]
    for user in users.getElementsByTagName('User'):
        patient_id = str(uuid.uuid4())
        clinician_id = user.getAttribute('ClinicianID')
        month_year_birth = user.getElementsByTagName('MonthYearOfBirth')[0].firstChild.nodeValue
        gender = user.getElementsByTagName('Gender')[0].firstChild.nodeValue
        height = user.getElementsByTagName('Height_cm')[0].firstChild.nodeValue
        weight = user.getElementsByTagName('Weight_kg')[0].firstChild.nodeValue
        amputation_type = user.getElementsByTagName('AmputationType')[0].firstChild.nodeValue
        socket_type = user.getElementsByTagName('SocketType')[0].firstChild.nodeValue
        first_fitted = user.getElementsByTagName('FirstProsthesisFitted')[0].firstChild.nodeValue
        hours_per_week = user.getElementsByTagName('FirstProsthesisFitted')[0].firstChild.nodeValue
        distance_per_week = user.getElementsByTagName('DistancePerWeek_km')[0].firstChild.nodeValue
        cursor = database.cursor()
        cursor.execute("INSERT INTO Patient (patient_id, clinician_id, month_year_birth, gender, height, weight,\
                      amputation_type, socket_type, first_fitting, hours_per_week, distance_per_week )\
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                      (patient_id, clinician_id, month_year_birth, gender, height, weight, 
                      amputation_type, socket_type, first_fitted, hours_per_week, distance_per_week))
        database.commit()
        for activity in user.getElementsByTagName('Activity'):
            activity_id = str(uuid.uuid4())
            end_time = activity.getAttribute('EndTime')
            start_time = activity.getAttribute('StartTime')
            activity_type = activity.getAttribute('Type')
            cursor.execute("INSERT INTO Activity VALUES (%s, %s, %s, %s, %s)", 
                      (activity_id, patient_id, end_time, start_time, activity_type))
            for sensor in activity.getElementsByTagName('Sensor'):
                sensor_id = str(uuid.uuid4())
                location = sensor.getAttribute('Location')
                sensor_type = sensor.getAttribute('Type')
                pressure_tolerance = sensor.getElementsByTagName('PressureTolerance')[0].firstChild.nodeValue
                cursor.execute("INSERT INTO Sensor VALUES (%s, %s, %s, %s, %s)",
                      (sensor_id, activity_id, location, sensor_type, pressure_tolerance))
                signal_output = sensor.getElementsByTagName('Signal')[0].firstChild.nodeValue
                signalnums = signal_output.replace("[", "")
                signalnums = signalnums.replace("]", "")
                signalList = signalnums.split(';')
                time_stamp = sensor.getElementsByTagName('Timestamp')[0].firstChild.nodeValue
                timenums = time_stamp.replace("[", "")
                timenums = timenums.replace("]", "")
                timeList = timenums.split(" ")
                point_of_interest = sensor.getElementsByTagName('PointsOfInterest')[0].firstChild.nodeValue
                poinums = point_of_interest.replace("[", "")
                poinums = poinums.replace("]", "")
                poiList = poinums.split(" ")
                for i in range(len(signalList)):
                    cursor.execute("INSERT INTO Timestamp VALUES (%s, %s, %s)",
                                  (sensor_id, i, timeList[i]))
                    database.commit()
                    cursor.execute("INSERT INTO Sensor_signal VALUES (%s, %s, %s)",
                                   (sensor_id, i, signalList[i]))
                    database.commit()
                for poi in poiList:
                    cursor.execute("INSERT INTO Point_of_interest VALUES (%s, %s)",
                                   (sensor_id, poi))
                    database.commit()
            print("XML data inserted successfully.")

def amWorking():
    print("Am working")

if __name__ == "__main__":
    create_database()