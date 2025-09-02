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

    # # Create test data
    # with open(os.path.join(os.path.dirname(__file__), "bulk_dataset_named.sql"),  'r') as f:
    #     cursor.execute(f.read())

    # database.commit() 

    database.close()