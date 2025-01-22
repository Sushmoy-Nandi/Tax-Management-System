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
          CREATE TABLE Audit 
            (
                AuditID INT AUTO_INCREMENT PRIMARY KEY,
                EntityName VARCHAR(100) NOT NULL,
                EntityID INT NOT NULL,
                ChangeDescription TEXT NOT NULL,
                ChangedBy INT,  -- Assuming it references Users(UserID)
                ChangeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ChangedBy) REFERENCES Users(UserID) ON DELETE SET NULL
            )
             
            """

mycursor.execute(sqlquery)
print("Create audit table successful")