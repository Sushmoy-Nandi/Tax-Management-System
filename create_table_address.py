import mysql.connector

db_name = "tax_management_system"

mydbconnection=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="#sqsks@1091l",
    database=db_name
)

mycursor = mydbconnection.cursor()

sqlquery = """
            CREATE TABLE Address 
            (
                AddressID INT PRIMARY KEY,
                Street VARCHAR(255),
                City VARCHAR(100),
                State VARCHAR(100),
                PostalCode VARCHAR(20),
                Country VARCHAR(100)
            )
            """

mycursor.execute(sqlquery)
print("Create address table successful")