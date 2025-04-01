from mysql.connector import Error
from user_login import login_user
from connect_db import connect_db
import mysql.connector
import re  # For email validation
from bcrypt import hashpw, gensalt, checkpw  # Import gensalt
from prettytable import PrettyTable


def user_dashboard(user_nid):

    while True:
        print("\n1. View Tax Status")
        print("2. View Payment History")
        print("3. Edit User Information") 
        print("4. Add New Tax Record") 
        print("5. Log Out")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                view_user_tax_records(user_nid)  
            elif choice == 2:
                view_payment_history(user_nid) 
            elif choice == 3:
                edit_user_records(user_nid) 
            elif choice == 4:
                add_new_tax_entity(user_nid) 
            elif choice == 5:
                print("Logging Out...")
                break 
            else:
                print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
        except ValueError:
            print("Invalid input. Please enter a number.") 

def view_user_tax_records(user_nid):

    db = connect_db()
    if not db:
        return

    try:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT 
                tp.TaxID,
                tp.NID,
                tp.TaxType,
                tp.TaxAmount,
                tp.PaidAmount,
                tp.DueAmount,
                tp.DueDate,
                CASE
                    WHEN tp.PaidAmount >= tp.TaxAmount THEN 'Paid'
                    WHEN tp.DueDate < CURDATE() THEN 'Overdue'
                    ELSE 'Unpaid'
                END AS PaymentStatus
            FROM TaxPayment tp
            WHERE tp.NID = %s
        """
        cursor.execute(query, (user_nid,))
        results = cursor.fetchall()

        if results:
            table = PrettyTable(["TaxID", "NID", "TaxType", "TaxAmount", "PaidAmount", "DueAmount", "DueDate", "PaymentStatus"])
            for record in results:
                table.add_row([
                    record['TaxID'],
                    record['NID'],
                    record['TaxType'],
                    record['TaxAmount'],
                    record['PaidAmount'],
                    record['DueAmount'],
                    record['DueDate'],
                    record['PaymentStatus']
                ])

            print("\nTax Records:")
            print(table) 
        else:
            print("No tax records found for this user.")

    except Error as e:
        print(f"Error retrieving tax records: {e}")
    finally:
        if db and db.is_connected():
            db.close()

def view_payment_history(user_nid):
    
    db = connect_db()
    if not db:
        return

    try:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT 
                tp.TaxID,
                tp.NID,
                tp.TaxType,
                tp.TaxAmount,
                tp.PaidAmount,
                tp.DueAmount,
                tp.DueDate
            FROM TaxPayment tp
            WHERE tp.NID = %s
        """
        cursor.execute(query, (user_nid,))
        results = cursor.fetchall()

        if results:
            table = PrettyTable(["TaxID", "NID", "TaxType", "TaxAmount", "PaidAmount", "DueAmount", "DueDate"])
            for payment in results:
                table.add_row([
                    payment['TaxID'],
                    payment['NID'],
                    payment['TaxType'],
                    payment['TaxAmount'],
                    payment['PaidAmount'],
                    payment['DueAmount'],
                    payment['DueDate']
                ])
            print("\nPayment History:")
            print(table)
        else:
            print("No payment history found for this user.")

    except Error as e:
        print(f"Error retrieving payment history: {e}")
    finally:
        if db and db.is_connected():
            db.close()

def update_phone_number(user_nid, new_phone_number):
   
    db = connect_db()
    if db:
        try:
            cursor = db.cursor()
            query = "UPDATE UserSignup SET PhoneNumber = %s WHERE NID = %s"  
            cursor.execute(query, (new_phone_number, user_nid))
            db.commit()
            return True
        except Error as e:
            print(f"Error updating phone number: {e}")
            db.rollback()  # Rollback in case of error
            return False
        finally:
            db.close()
    else:
        print("Could not connect to the database.")
        return False
    
def update_email_address(user_nid, new_email_address):

    if not is_valid_email(new_email_address):  # Email validation
        print("Invalid email address format.")
        return False

    db = connect_db()
    if db:
        try:
            cursor = db.cursor()
            query = "UPDATE UserSignup SET Email = %s WHERE NID = %s"  
            cursor.execute(query, (new_email_address, user_nid))
            db.commit()
            print("Email address updated successfully!")
            return True
        except Error as e:
            print(f"Error updating email address: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    else:
        print("Could not connect to the database.")
        return False

def is_valid_email(email):

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

def update_password(user_nid, new_password):

    if not is_strong_password(new_password):  # Password strength check
        print("Password is not strong enough. It must be at least 8 characters long and include a mix of uppercase, lowercase, digits, and symbols.")
        return False

    hashed_password = hashpw(new_password.encode('utf-8'), gensalt())  # Hash the new password

    db = connect_db()
    if db:
        try:
            cursor = db.cursor()
            query = "UPDATE UserSignup SET Password = %s WHERE NID = %s"  
            cursor.execute(query, (hashed_password, user_nid))
            db.commit()
            print("Password updated successfully!")
            return True
        except Error as e:
            print(f"Error updating password: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    else:
        print("Could not connect to the database.")
        return False


def is_strong_password(password):
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 symbol
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(password_regex, password) is not None

def edit_user_records(user_nid):

    print("\nEdit User Information")
    print("1. Update Phone Number")
    print("2. Update Email Address")
    print("3. Update Password")
    print("4. Cancel")

    try:
        edit_choice = int(input("Enter your choice: "))
        if edit_choice == 1:
            new_phone_number = input("Enter new phone number: ")
            if not new_phone_number.isdigit():
                print("Invalid phone number. Please enter digits only.")
                return

            if update_phone_number(user_nid, new_phone_number):
                print("Phone number updated successfully!")
            else:
                print("Failed to update phone number.")

        elif edit_choice == 2:
            new_email_address = input("Enter new email address: ")
            if update_email_address(user_nid, new_email_address):
                print("Email address updated successfully!")
            else:
                print("Failed to update email address.")

        elif edit_choice == 3:  # Handle password update
            new_password = input("Enter new password: ")
            if update_password(user_nid, new_password):
                print("Password updated successfully!")
            else:
                print("Failed to update password.")

        elif edit_choice == 4:
            print("Edit canceled.")
            return
        else:
            print("Invalid choice. Please select a valid option.")
    except ValueError:
        print("Invalid input. Please enter a number.")
import uuid

def add_new_tax_entity(user_nid):
    print("\nAdd New Tax Entity")
    print("1. Land Tax")
    print("2. Income Tax")
    print("3. Business Tax")

    try:
        entity_type = int(input("Select tax type: "))
        db = connect_db()
        cursor = db.cursor()

        if entity_type == 1:
            # Handle land tax addition logic
            print("Adding Land Tax")
            property_location = input("Enter property location: ")
            land_area = float(input("Enter land area (in sq.m): "))
            land_value = float(input("Enter land value: "))

            add_land_tax_query = """
                INSERT INTO LandTax (PropertyLocation, PropertySize, PropertyValue, TaxPayerNID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(add_land_tax_query, (property_location, land_area, land_value, user_nid))
            db.commit()

            # Insert corresponding tax payment
            tax_amount = land_value * 0.1  # Example: 10% of property value
            print("Your Payable Tax Amount: "+ str(land_value * 0.1))
            paid_amount=input("Enter your paid Aamount: ")
            due_date = input("Enter the due date (YYYY-MM-DD): ")

            tax_payment_query = """
                                INSERT INTO TaxPayment (NID, TaxType, TaxAmount, PaidAmount, DueDate)
                                VALUES (%s, %s, %s, %s, %s)
                                """
            
            cursor.execute(tax_payment_query, (user_nid, 'Land Tax', tax_amount, paid_amount, due_date))
            db.commit()

            print("Land Tax record and tax payment added successfully!")

        elif entity_type == 2:
            # Handle income tax addition logic
            print("Adding Income Tax")
            annual_income = float(input("Enter annual income: "))
            taxable_income = float(input("Enter taxable income: "))

            add_income_tax_query = """
                INSERT INTO IncomeTax (AnnualIncome, TaxableIncome, TaxPayerNID)
                VALUES (%s, %s, %s)
            """
            cursor.execute(add_income_tax_query, (annual_income, taxable_income, user_nid))
            db.commit()

            # Insert corresponding tax payment
            tax_amount = taxable_income * 0.2  # Example: 20% of taxable income
            print("Your Payable Tax Amount: "+ str(taxable_income * 0.1))
            paid_amount=input("Enter your paid Aamount: ")
            due_date = input("Enter the due date (YYYY-MM-DD): ")

            tax_payment_query = """
                INSERT INTO TaxPayment (NID, TaxType, TaxAmount, PaidAmount, DueDate)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(tax_payment_query, (user_nid, 'Income Tax', tax_amount, paid_amount, due_date))
            db.commit()

            print("Income Tax record and tax payment added successfully!")

        elif entity_type == 3:
            # Handle business tax addition logic
            print("Adding Business Tax")
            business_name = input("Enter business name: ")
            business_type = input("Enter your business type: ")
            annual_revenue = float(input("Enter annual revenue: "))

            add_business_tax_query = """
                INSERT INTO BusinessTax (BusinessName, BusinessType, AnnualRevenue, TaxPayerID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(add_business_tax_query, (business_name, business_type, annual_revenue, user_nid))
            db.commit()

            # Insert corresponding tax payment
            tax_amount = annual_revenue * 0.1  # Example: 10% of annual revenue
            print("Your Payable Tax Amount: "+ str(annual_revenue * 0.1))
            paid_amount=input("Enter your paid Aamount: ")

            due_date = input("Enter the due date (YYYY-MM-DD): ")
            tax_payment_query = """
                                INSERT INTO TaxPayment (NID, TaxType, TaxAmount, PaidAmount, DueDate)
                                VALUES (%s, %s, %s, %s, %s)
                                """

            cursor.execute(tax_payment_query, (user_nid, 'Business Tax', tax_amount, paid_amount, due_date))
            db.commit()

            print("Business Tax record and tax payment added successfully!")

        else:
            print("Invalid entity type. Please select a valid option.")

    except ValueError as ve:
        print("Invalid input. Please enter valid numbers where required.")
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        db.rollback()  # Rollback transaction in case of error
    finally:
        # Close the connection
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


if __name__ == "__main__":
    while True:
        user_nid = login_user()  # Call login_user to get user ID
        if user_nid:
            user_dashboard(user_nid)  # Pass the user_nid to user_dashboard()
        else:
            print("Login failed. Exiting.")
            break