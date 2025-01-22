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
           CREATE TABLE TaxPayment 
                (
                    PaymentID INT PRIMARY KEY,
                    TaxID INT,
                    PaymentDate DATE,
                    PaymentAmount DECIMAL(10, 2),
                    PaymentMethod VARCHAR(50),
                    FOREIGN KEY (TaxID) REFERENCES Tax(TaxID) ON DELETE CASCADE
                )
            """

mycursor.execute(sqlquery)
print("Create tax payment table successful")