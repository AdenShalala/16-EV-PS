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
    database = get_database()
    cursor = database.cursor()

    with open(os.path.join(os.path.dirname(__file__), "sql/populate.sql"),  'r') as f:
        cursor.execute(f.read())

    database.commit() 
    database.close()

# constructor candy
def create_clinician(result):
    return Clinician(*result)

def create_patient(result):
    return Patient(*result)

def create_session(result):
    #print(result)
    return Session(*result)

# accessors
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

def write_session(session: Session):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("INSERT INTO Session (session_id, id, account_type, secret_hash, created_at, last_verified_at) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (session.session_id, session.id, session.account_type, session.secret_hash, session.created_at, session.last_verified_at,))
    
    database.commit()
    database.close()

def update_session_verified_at(session: Session):
    database = get_database()

    cursor = database.cursor()
    cursor.execute("UPDATE Session SET last_verified_at %s WHERE session_id = %s", (session.last_verified_at, session.session_id))
    
    database.commit()
    database.close()

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
    
def delete_session(session_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("DELETE FROM Session WHERE session_id = %s", (session_id,))
    database.commit()
    database.close()

def get_patients_from_clinician(clinician: Clinician):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Patient WHERE clinician_id = %s", (Clinician.clinician_id,))
    result = cursor.fetchall()

    patients = []

    for i in result:
        patients.append(create_patient(i))

    database.close()

    return patients