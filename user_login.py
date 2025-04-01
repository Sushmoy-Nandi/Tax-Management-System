from bcrypt import hashpw, gensalt, checkpw
from connect_db import connect_db
from mysql.connector import Error

def login_user():
    db = connect_db()
    if not db:
        return None

    nid = input("Enter NID: ")

    try:
        cursor = db.cursor()
        # Retrieve user details (NID and Name from TaxPayers table)
        query = "SELECT NID, Name FROM TaxPayers WHERE NID = %s" 
        cursor.execute(query, (nid,))
        result = cursor.fetchone()

        if result:
            stored_nid, stored_name = result

            # Retrieve the stored hashed password from UserSignup
            query = "SELECT Password FROM UserSignup WHERE NID = %s"
            cursor.execute(query, (nid,))
            password_result = cursor.fetchone()

            if password_result:
                stored_hashed_password = password_result[0].encode('utf-8')
                password = input("Enter Password: ") 
                if checkpw(password.encode('utf-8'), stored_hashed_password):
                    return stored_nid, stored_name 
                else:
                    print("Incorrect Password.")
            else:
                print("NID not found in UserSignup table.")
        else:
            print("NID not found in TaxPayers table.")

    except Error as e:
        print(f"Error during login: {e}")
        return None 
    finally:
        db.close()

    return None  # Login failed (incorrect credentials or other error)

