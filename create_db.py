import mysql.connector

mydbconnection=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="#sqsks@1091l"
)

print(mydbconnection)

db_name="tax_management_system"
mycursor = mydbconnection.cursor()

sqlquery = "CREATE DATABASE " + db_name

mycursor.execute(sqlquery)