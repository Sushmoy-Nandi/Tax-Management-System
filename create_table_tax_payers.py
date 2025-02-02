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
CREATE TABLE TaxPayers (
    TaxPayerID INT PRIMARY KEY AUTO_INCREMENT,
    NID INT UNIQUE,  -- Added UNIQUE constraint for NID
    Name VARCHAR(255),
    DOB DATE,
    Gender VARCHAR(10),
    Address VARCHAR(50),
    Status VARCHAR(20) DEFAULT 'Active', 
    FOREIGN KEY (NID) REFERENCES UserSignup(NID)

);

            """

mycursor.execute(sqlquery)
print("Create citizen who pay tax table successful")