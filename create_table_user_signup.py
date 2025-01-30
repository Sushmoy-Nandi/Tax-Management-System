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
            CREATE TABLE UserSignup
                (
                    SignupID INT PRIMARY KEY AUTO_INCREMENT,
                    NID INT,
                    PhoneNumber VARCHAR(20),
                    Email VARCHAR(50),
                    Password VARCHAR(255),  -- Encrypted password
                    SignupStatus VARCHAR(20) DEFAULT 'Pending', -- Pending, Verified, Expired
                    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    
                );

            """

mycursor.execute(sqlquery)
print("Create user signup table successful")