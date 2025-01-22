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
            CREATE TABLE Tax 
                (
                    TaxID INT PRIMARY KEY,
                    NID INT,
                    TaxType VARCHAR(50),
                    TaxDescription TEXT,
                    TaxBaseAmount DECIMAL(10, 2),
                    TaxRateID INT,
                    TaxAmount DECIMAL(10, 2),
                    DueDate DATE,
                    FOREIGN KEY (NID) REFERENCES Citizen(NID) ON DELETE CASCADE,
                    FOREIGN KEY (TaxRateID) REFERENCES TaxRates(TaxRateID) ON DELETE SET NULL
                )

              
            """

mycursor.execute(sqlquery)
print("Create tax table successful")