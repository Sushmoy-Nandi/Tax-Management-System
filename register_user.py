from bcrypt import hashpw, gensalt
from mysql.connector import connect, Error
import re
from connect_db import connect_db


def is_strong_password(password):
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 symbol
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(password_regex, password) is not None

def register_user():
    db = connect_db()
    if not db:
        return

    while True:
        try:
            nid = int(input("Enter NID: "))
            if nid <= 0:
                raise ValueError("NID must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid NID: {e}. Please enter a valid NID.")

    phone_number = input("Enter Phone Number: ")
    email = input("Enter Email: ")

    while True:
        password = input("Enter Password: ")
        confirm_password = input("Confirm Password: ")

        if not is_strong_password(password):
            print("Password is not strong enough. It must be at least 8 characters long and include a mix of uppercase, lowercase, digits, and symbols.")
            return False  # Early return on weak password

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        else:
            hashed_password = hashpw(password.encode('utf-8'), gensalt())
            break

    # Now we handle the user's registration and the corresponding taxpayer and tax payment registration.
    try:
        cursor = db.cursor()
        
        # 1. Insert into UserSignup table
        user_signup_query = "INSERT INTO UserSignup (NID, PhoneNumber, Email, Password) VALUES (%s, %s, %s, %s)"
        user_signup_values = (nid, phone_number, email, hashed_password)

        cursor.execute(user_signup_query, user_signup_values)
        db.commit()  # Commit to ensure the NID is inserted before proceeding
        
        # 2. Insert into TaxPayers table
        name = input("Enter your Name: ")
        dob = input("Enter your Date of Birth (YYYY-MM-DD): ")
        gender = input("Enter your Gender: ")
        address = input("Enter your Address: ")

        taxpayer_query = "INSERT INTO TaxPayers (NID, Name, DOB, Gender, Address) VALUES (%s, %s, %s, %s, %s)"
        taxpayer_values = (nid, name, dob, gender, address)
        
        cursor.execute(taxpayer_query, taxpayer_values)
        taxpayer_id = cursor.lastrowid  # Get the auto-generated TaxPayerID

        db.commit()  # Commit all changes at once
        
        print("User registration and taxpayer details successfully recorded!")

    except Error as e:
        db.rollback()  # Rollback on error
        if "Duplicate entry" in str(e):  # Check for duplicate NID
            print(f"NID already exists. Please try a different NID.")
        else:
            print(f"Error during registration: {e}")
    finally:
        cursor.close()
        db.close()




