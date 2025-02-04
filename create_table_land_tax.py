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
        CREATE TABLE LandTax (
    LandTaxID INT PRIMARY KEY AUTO_INCREMENT,
    PropertyLocation VARCHAR(255), 
    PropertySize DECIMAL(10, 2), 
    PropertyValue DECIMAL(10, 2),
    TaxPayerNID INT,
    FOREIGN KEY (TaxPayerNID) REFERENCES UserSignup(NID)

    
);


            """

mycursor.execute(sqlquery)
print("Create land tax table successful")