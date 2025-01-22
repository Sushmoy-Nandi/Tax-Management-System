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
            CREATE TABLE Citizen 
                (
                    NID INT PRIMARY KEY,
                    Name VARCHAR(255),
                    DateOfBirth DATE,
                    Gender VARCHAR(10),
                    AddressID INT,
                    PhoneNumber VARCHAR(20),
                    Email VARCHAR(100),
                    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE SET NULL
                )
            """

mycursor.execute(sqlquery)
print("Create citizen table successful")