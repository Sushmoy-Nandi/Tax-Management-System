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
    TaxPayerID INT,
    NID INT NULL,
    TaxType TEXT,
    TaxAmount DECIMAL(10, 2),
    PaidAmount DECIMAL(10, 2) DEFAULT 0,
    DueAmount DECIMAL(10, 2) AS (TaxAmount - PaidAmount) STORED,
    DueDate DATE,
    FOREIGN KEY (NID) REFERENCES UserSignup(NID) ON DELETE CASCADE,
    FOREIGN KEY (TaxPayerID) REFERENCES TaxPayers(TaxPayerID) 
);
            """

mycursor.execute(sqlquery)
print("Create TaxPayment table successful")