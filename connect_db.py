import mysql.connector
from mysql.connector import Error
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="#sqsks@1091l",
            database="tax_management_system"
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None