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
            CREATE TABLE IncomeTax 
            (
                IncomeTaxID INT PRIMARY KEY AUTO_INCREMENT,
                AnnualIncome DECIMAL(10, 2),  -- Total annual income
                TaxableIncome DECIMAL(10, 2), -- Portion of the income that is taxable
                TaxPayerNID INT,
                FOREIGN KEY (TaxPayerNID) REFERENCES UserSignup(NID)
            );

            """

mycursor.execute(sqlquery)
print("Create Income tax table successful")