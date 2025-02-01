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
CREATE TABLE TaxPayment (
    TaxID INT PRIMARY KEY AUTO_INCREMENT,
    NID INT NULL,
    TaxType ENUM('Land Tax', 'Income Tax', 'Business Tax') NOT NULL,  -- Use ENUM for better control over types
    TaxAmount DECIMAL(10, 2),
    PaidAmount DECIMAL(10, 2) DEFAULT 0,
    DueAmount DECIMAL(10, 2) AS (TaxAmount - PaidAmount) STORED,
    DueDate DATE,
    FOREIGN KEY (NID) REFERENCES UserSignup(NID) ON DELETE CASCADE
);

            """

mycursor.execute(sqlquery)
print("Create TaxPayment table successful")