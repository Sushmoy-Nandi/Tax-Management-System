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
            CREATE TABLE BusinessTax 
            (
                BusinessTaxID INT PRIMARY KEY AUTO_INCREMENT,
                BusinessName VARCHAR(255),  -- Name of the business
                BusinessType VARCHAR(100),  -- Type of business (e.g., Retail, Manufacturing)
                AnnualRevenue DECIMAL(10, 2),  -- Total revenue for the year
                TaxPayerNID INT,
                FOREIGN KEY (TaxPayerNID) REFERENCES UserSignup(NID)
            );

            """

mycursor.execute(sqlquery)
print("Create Business Tax  table successful")