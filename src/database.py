from dotenv import load_dotenv
import mysql.connector
import os
import sys

from schema import *;

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

    database.commit() 
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
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + str(os.getenv('MYSQL_DATABASE')) + ';')
    database.close();

    # re open database
    database = get_database()
    cursor = database.cursor()

    with open(os.path.join(os.path.dirname(__file__), "sql/create.sql"),  'r') as f:
        cursor.execute(f.read())

    database.commit() 
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


# accessors
def get_clinician(clinician_id: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Clinician WHERE clinician_id = %s", (clinician_id,));
    result = cursor.fetchone();

    if result:
        database.close()
        return create_clinician(result)
    else:
        database.close()
        return None

def get_clinician_from_email(email: str):
    database = get_database()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM Clinician WHERE email = %s", (email,));
    result = cursor.fetchone();

    if result:
        database.close()
        return create_clinician(result)
    else:
        database.close()
        return None
