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
            CREATE TABLE TaxRates 
                (
                    TaxRateID INT PRIMARY KEY,
                    TaxType VARCHAR(50),
                    RateDescription VARCHAR(255),
                    RatePercentage DECIMAL(5, 2),
                    EffectiveDate DATE,
                    ExpiryDate DATE
                )
              
            """

mycursor.execute(sqlquery)
print("Create taxrates table successful")