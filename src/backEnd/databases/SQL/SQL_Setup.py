from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Database Init     #
#~~~~~~~~~~~~~~~~~~~~~~~#

def database_connect(): 
    load_dotenv(override=True)
    connection = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT')
    )

    cursor = connection.cursor()

    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + str(os.getenv('MYSQL_DATABASE')) + ';')

    connection.close()

    database = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )

    cursor = database.cursor()
    # Use Database
    cursor.execute("USE " + str(os.getenv('MYSQL_DATABASE')) + ';')

    # Create tables
    with open(os.path.join(os.path.dirname(__file__), "Create.sql"),  'r') as f:
        cursor.execute(f.read())

    database.commit() 

    database.close()
    
    database = mysql.connector.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )

    cursor = database.cursor()
    # Use Database
    cursor.execute("USE " + str(os.getenv('MYSQL_DATABASE')) + ';')

    
    # Insert Clinicians 

    clinicians = [
    ['CLIN402', 'Dr. Zhang', 'zhang@email.com', 'hashed_password_123'],
    ['CLIN180', 'Dr. Smith', 'smith@email.com', 'hashed_password_456'],
    ['CLIN495', 'Dr. Johnson', 'johnson@email.com', 'hashed_password_789'],
    ['CLIN612', 'Dr. Lee', 'lee@email.com', 'hashed_password_101'],
    ['CLIN953', 'Dr. Patel', 'patel@email.com', 'hashed_password_102'],
    ['CLIN133', 'Dr. Brown', 'brown@email.com', 'hashed_password_103'],
    ['CLIN888', 'Dr. Davis', 'davis@email.com', 'hashed_password_104'],
    ['CLIN956', 'Dr. Wilson', 'wilson@email.com', 'hashed_password_105'],
    ['CLIN844', 'Dr. House', 'house@email.com', 'hashed_password_102'],
    ['CLIN978', 'Dr. Taylor', 'taylor@email.com', 'hashed_password_106']
    ]

    # Insert into the table
    for c in clinicians:
        cursor.execute("""
        INSERT INTO Clinician (clinician_id, name, email, password_hash)
        VALUES (%s, %s, %s, %s)
        """, (c[0], c[1], c[2], c[3]))

    database.commit()


    database.close()