import mysql.connector
from prettytable import PrettyTable
import getpass
from mysql.connector import Error
from connect_db import connect_db  # For secure password input

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "#sqsks@1091l"
DB_NAME = "tax_management_system"

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None
    
def admin_login():
    """Handles admin login authentication."""
    attempts = 3
    while attempts > 0:
        username = input("Enter admin username: ").strip()
        password = getpass.getpass("Enter admin password: ") # Secure password input

        if username == "admin" and password == "password": 
            print("Admin login successful!")
            return True  # Login successful
        else:
            attempts -= 1
            print(f"Incorrect username or password. {attempts} attempts remaining.")

    print("Too many incorrect login attempts. Access denied.")
    return False  # Login failed

def display_tax_records_table_with_status(records):
    # Displays tax records in a nicely formatted table.
    table = PrettyTable()
    table.field_names = ["TaxID", "NID", "TaxType", "TaxAmount", "PaidAmount", "DueAmount", "DueDate", "PaymentStatus"]

    for record in records:
        row = []
        for field in table.field_names:  # Iterate through field names for consistent order
            value = record.get(field)  # Use .get() to safely handle missing keys/None values
            row.append(value if value is not None else "N/A")  # Replace None with "N/A"

        table.add_row(row)

    print(table)

def display_tax_records_table(records):

    table = PrettyTable()
    table.field_names = ["TaxID", "NID", "TaxType", "TaxAmount", "PaidAmount", "DueAmount", "DueDate"]

    for record in records:
        row = []
        for field in table.field_names:  # Iterate through field names for consistent order
            value = record.get(field)  # Use .get() to safely handle missing keys/None values
            row.append(value if value is not None else "N/A")  # Replace None with "N/A"

        table.add_row(row)

    print(table)

def display_tax_payers_table(records):
   
    table = PrettyTable()
    table.field_names = ["TaxPayerID", "NID", "Name", "DOB", "Address", "Status"]

    for record in records:
        row = []
        for field in table.field_names:  # Iterate through field names for consistent order
            value = record.get(field)  # Use .get() to safely handle missing keys/None values
            row.append(value if value is not None else "N/A")  # Replace None with "N/A"

        table.add_row(row)

    print(table)
    
def view_all_tax_records():
    mydb = get_db_connection()
    if mydb is None:
        return

    mycursor = None
    try:
        mycursor = mydb.cursor(dictionary=True)
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
        """
        mycursor.execute(query)
        results = mycursor.fetchall()

        if results:
            display_tax_records_table(results)  # Use the table display function
        else:
            print("No tax records found.")

    except mysql.connector.Error as err:
        print(f"Error in view_all_tax_records: {err}")

    except mysql.connector.Error as err:
        print(f"Error in view_all_tax_records: {err}")

    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()

def view_tax_payments_with_status():

    mydb = get_db_connection()
    if mydb is None:
        return

    mycursor = None
    try:
        mycursor = mydb.cursor(dictionary=True)
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
                    WHEN tp.DueDate < CURDATE() THEN 'Overdue'  -- Check if DueDate is in the past
                    ELSE 'Unpaid'
                END AS PaymentStatus
            FROM TaxPayment tp
        """
        mycursor.execute(query)
        results = mycursor.fetchall()

        if results:
            display_tax_records_table_with_status(results)  # Display in table format
        else:
            print("No tax records found.")
    except mysql.connector.Error as err:
        print(f"Error in view_tax_payments_with_status: {err}")

    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()

def add_new_tax_record():
   
    mydb = get_db_connection()
    if mydb is None:
        return

    mycursor = None
    try:
        mycursor = mydb.cursor()
        mydb.start_transaction()

        print("\nEnter details for the new tax record:")

        nid = input("NID (or press Enter to skip): ").strip()
        if nid:
            try:
                nid = int(nid)
            except ValueError:
                raise ValueError("Invalid NID. Must be an integer.")
        print("Allowed tax types = Land Tax, Income Tax, Business Tax")
        tax_type = input("Tax Type: ").strip()
        allowed_tax_types = {'Land Tax', 'Income Tax', 'Business Tax'}
        if tax_type not in allowed_tax_types:
            raise ValueError(f"Invalid Tax Type. Allowed types: {', '.join(allowed_tax_types)}")

        # Insert into specific tax table based on TaxType
        if tax_type == "Land Tax":
            property_location = input("Property Location: ")
            property_size = float(input("Property Size: "))
            property_value = float(input("Property Value: "))

            insert_specific_tax_query = """
                INSERT INTO LandTax (PropertyLocation, PropertySize, PropertyValue, TaxPayerNID) 
                VALUES (%s, %s, %s, %s)
            """
            values = (property_location, property_size, property_value, nid)

        elif tax_type == "Income Tax":
            annual_income = float(input("Annual Income: "))
            taxable_income = float(input("Taxable Income: "))

            insert_specific_tax_query = """
                INSERT INTO IncomeTax (AnnualIncome, TaxableIncome, TaxPayerNID) 
                VALUES (%s, %s, %s)
            """
            values = (annual_income, taxable_income, nid)
            
        elif tax_type == "Business Tax":
            business_name = input("Business Name: ")
            business_type = input("Business Type: ")
            annual_revenue = float(input("Annual Revenue: "))

            insert_specific_tax_query = """
                INSERT INTO BusinessTax (BusinessName, BusinessType, AnnualRevenue, TaxPayerNID) 
                VALUES (%s, %s, %s, %s)
            """
            values = (business_name, business_type, annual_revenue, nid)

        try:
            mycursor.execute(insert_specific_tax_query, values)
        except mysql.connector.Error as specific_table_err:
            mydb.rollback()
            print(f"Error inserting into {tax_type} table: {specific_table_err}")
            return

        # Calculate Tax Amount based on Tax Type
        if tax_type == "Land Tax": 
            tax_amount = property_value * 0.1  # Example: 10% of property value
        elif tax_type == "Income Tax":
            tax_amount = taxable_income * 0.2  # Example: 20% of taxable income
        elif tax_type == "Business Tax":
            tax_amount = annual_revenue * 0.1  # Example: 10% of annual revenue

        # Insert into TaxPayment
        print(f"Your Payable Tax Amount: {tax_amount}")
        paid_amount=input("Enter your paid Aamount: ")
        due_date = input("Enter the due date (YYYY-MM-DD): ")

        query = """
            INSERT INTO TaxPayment (NID, TaxType, TaxAmount, PaidAmount, DueDate) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (nid, tax_type, tax_amount,paid_amount, due_date)
        mycursor.execute(query, values)

        mydb.commit()
        print("\nNew tax record added successfully.")

    except mysql.connector.Error as err:
        mydb.rollback()
        print(f"Error adding tax record: {err}")
    except ValueError as err:
        mydb.rollback()
        print(f"Invalid input: {err}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()

def edit_tax_record():
    mydb = get_db_connection()
    if mydb is None:
        return

    mycursor = None
    try:
        mycursor = mydb.cursor()
        mydb.start_transaction()

        tax_id = input("Enter the TaxID of the record you want to edit: ").strip()
        try:
            tax_id = int(tax_id)
        except ValueError:
            raise ValueError("Invalid TaxID. Must be an integer.")

        mycursor.execute("SELECT * FROM TaxPayment WHERE TaxID = %s", (tax_id,))
        record = mycursor.fetchone()

        if not record:
            print("Tax record not found.")
            return

        print("\nCurrent record details:")
        print(record)

        print("\nEnter new values (or press Enter to keep current value):")

        taxpayer_id = input(f"TaxPayerID ({record[1] or 'N/A'}): ").strip() or record[1]
        nid = input(f"NID ({record[2] or 'N/A'}): ").strip() or record[2]
        tax_type = input(f"Tax Type ({record[3]}): ").strip() or record[3]

        while True:  # Loop until a valid float is entered
            tax_amount_input = input(f"Tax Amount ({record[4]}): ").strip() or record[4]
            try:
                tax_amount = float(tax_amount_input)
                break  # Exit the loop if conversion is successful
            except ValueError:
                print("Invalid Tax Amount. Please enter a number.")

        due_date = input(f"Due Date ({record[7]}): ").strip() or record[7]

        query = """
            UPDATE TaxPayment 
            SET TaxPayerID = %s, NID = %s, TaxType = %s, TaxAmount = %s, DueDate = %s
            WHERE TaxID = %s
        """
        values = (taxpayer_id, nid, tax_type, tax_amount, due_date, tax_id)

        mycursor.execute(query, values)
        mydb.commit()
        print("\nTax record updated successfully.")

    except mysql.connector.Error as err:
        mydb.rollback()
        print(f"Error in edit_tax_record: {err}")
    except ValueError as err:
        mydb.rollback()
        print(f"Invalid input: {err}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()


def delete_tax_record():
    mydb = get_db_connection()
    if mydb is None:
        return

    mycursor = None
    try:
        mycursor = mydb.cursor()
        mydb.start_transaction()

        tax_id = input("Enter the TaxID of the record you want to delete: ").strip()
        try:
            tax_id = int(tax_id)
        except ValueError:
            raise ValueError("Invalid TaxID. Must be an integer.")

        query = "DELETE FROM TaxPayment WHERE TaxID = %s"
        mycursor.execute(query, (tax_id,))

        if mycursor.rowcount == 0:
            print("Tax record not found.")
        else:
            mydb.commit()
            print("\nTax record deleted successfully.")

    except mysql.connector.Error as err:
        mydb.rollback()
        print(f"Error in delete_tax_record: {err}")
    except ValueError as err:
        mydb.rollback()
        print(f"Invalid input: {err}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()

def view_all_tax_payers():  # New function to view tax payers
    mydb = get_db_connection()
    if mydb is None:
        return

    mycursor = None
    try:
        mycursor = mydb.cursor(dictionary=True)
        query = """
                SELECT
                    txp.TaxPayerID,
                    txp.NID,
                    txp.Name,
                    txp.DOB,
                    txp.Gender,
                    txp.Address,
                    txp.Status
                FROM TaxPayers txp
                """
        mycursor.execute(query)
        results = mycursor.fetchall()

        if results:
            display_tax_payers_table(results) # Reuse the display function
        else:
            print("No tax payers found.")

    except mysql.connector.Error as err:
        print(f"Error in view_all_tax_payers: {err}")

    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()
def search_records(table_name: str, search_column: str, search_value: str):

    db = connect_db()
    if not db:
        return

    try:
        cursor = db.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name} WHERE {search_column} LIKE %s"
        cursor.execute(query, (f"%{search_value}%",))
        rows = cursor.fetchall()

        if rows:
            table = PrettyTable(list(rows[0].keys()))  
            for row in rows:
                table.add_row(list(row.values()))
            print(f"\nSearch Results for '{search_value}' in '{search_column}':")
            print(table)
        else:
            print(f"No records found for '{search_value}' in '{search_column}'.")

    except Error as e:
        print(f"Error searching records: {e}")
    finally:
        db.close()
        
def admin_dashboard():
    if not admin_login():  # Check if login was successful
        return
    while True:
        print("\nWelcome to the Admin Panel")
        print("1. View All Tax Records")
        print("2. Add New Tax Record")
        print("3. Update Tax Record")
        print("4. Delete Tax Record")
        print("5. View Tax Payments with Status")
        print("6. View All Tax Payers")  
        print("7. Search Tax Records")
        print("8. Log Out")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_tax_records()
        elif choice == "2":
            add_new_tax_record()
        elif choice == "3":
            edit_tax_record()
        elif choice == "4":
            delete_tax_record()
        elif choice == "5":
            view_tax_payments_with_status()
        elif choice == "6":
            view_all_tax_payers()
        elif choice == "7":
            table_name = input("Enter table name: ").strip()
            search_column = input("Enter column to search: ").strip()
            search_value = input("Enter value to search: ").strip()
            search_records(table_name, search_column, search_value)
        elif choice == "8":
            print("Logging out...")
            return
        else:
            print("Invalid choice. Please try again.")