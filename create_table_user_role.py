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
          CREATE TABLE UserRoles 
            (
                RoleID INT PRIMARY KEY,
                RoleName VARCHAR(50)    
            )
            """

mycursor.execute(sqlquery)
print("Create user roles table successful")