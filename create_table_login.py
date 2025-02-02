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
        CREATE TABLE UserLogin 
(
    LoginID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,  -- Links to the Users table
    OTPCode VARCHAR(6),  -- OTP sent to phone for verification
    OTPExpiry TIMESTAMP, -- Expiry time for OTP validity
    LoginTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Login timestamp
    LogoutTime TIMESTAMP NULL,  -- Logout timestamp
    SessionToken VARCHAR(255),  -- Unique session token
    IsActive BOOLEAN DEFAULT TRUE,  -- Whether the session is active
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);


            """

mycursor.execute(sqlquery)
print("Create users login table successful")