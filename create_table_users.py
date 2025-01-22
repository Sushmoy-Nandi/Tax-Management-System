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
          CREATE TABLE Users 
            (
                UserID INT PRIMARY KEY,
                NID INT,
                RoleID INT,
                Username VARCHAR(50) UNIQUE,
                Password VARCHAR(255),
                Email VARCHAR(100),
                FOREIGN KEY (NID) REFERENCES Citizen(NID) ON DELETE CASCADE,
                FOREIGN KEY (RoleID) REFERENCES UserRoles(RoleID) ON DELETE SET NULL
            )
            """

mycursor.execute(sqlquery)
print("Create users table successful")