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
CREATE VIEW TaxPaymentWithStatus AS
SELECT 
    TaxID,
    NID,
    TaxType,
    TaxAmount,
    PaidAmount,
    DueAmount,
    DueDate,
    CASE
        WHEN DueAmount > 0 AND DueDate >= CURDATE() THEN 'Unpaid'
        WHEN DueAmount > 0 AND DueDate < CURDATE() THEN 'Overdue'
        ELSE 'Paid'
    END AS TaxStatus
FROM TaxPayment;


            """

mycursor.execute(sqlquery)
print("Create TaxPayment Status table successful")