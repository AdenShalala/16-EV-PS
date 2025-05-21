import mysql.connector as sql
from readXML import XMLInsert
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

def database_connect(): 
    database = sql.connect(
        host = os.getenv('MYSQL_HOST'), 
        user = os.getenv('MYSQL_USER'), 
        password = os.getenv('MYSQL_PASSWORD'),
        port = os.getenv('MYSQL_PORT'),
        database = os.getenv('MYSQL_DATABASE')
    )

    return database


