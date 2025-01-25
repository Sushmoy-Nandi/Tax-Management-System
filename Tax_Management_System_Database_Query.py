import mysql.connector
from mysql.connector import Error
from typing import List, Dict
import csv

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="#sqsks@1091l",
            database="tax_management_system"
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_record(table_name: str, columns: List[str], values: List[str]):
    db = connect_db()
    if not db:
        return
    try:
        cursor = db.cursor()
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        cursor.execute(query, values)
        db.commit()
        print(f"Record added successfully to {table_name}.")
    except Error as e:
        print(f"Error adding record: {e}")
    finally:
        db.close()

def read_table(table_name: str, columns: List[str] = None, max_col_width: int = 30):
    db = connect_db()
    if not db:
        return

    try:
        cursor = db.cursor()
        columns_str = ", ".join(columns) if columns else "*"
        query = f"SELECT {columns_str} FROM {table_name}"
        cursor.execute(query)
        col_names = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        column_widths = [len(col_name) for col_name in col_names]
        for row in rows:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))
        column_widths = [min(width, max_col_width) for width in column_widths]
        row_format = " | ".join(f"{{:<{w}}}" for w in column_widths)
        print("\n")
        print(row_format.format(*col_names))
        print("-" * (sum(column_widths) + 3 * (len(col_names) - 1)))  
        for row in rows:
            truncated_row = [str(value)[:max_col_width] for value in row]
            print(row_format.format(*truncated_row))
    except Error as e:
        print(f"Error reading table: {e}")
    finally:
        db.close()

def execute_query(query, values):
    db = connect_db()  
    if not db:
        print("MySQL Connection not available.")
        return

    try:
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        
        print(f"Query Executed Successfully: {cursor.rowcount} row(s) affected")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def update_record(table_name, update_column, update_value, condition_column, condition_value):
    query = f"UPDATE {table_name} SET {update_column} = %s WHERE {condition_column} = %s"
    values = (update_value, condition_value)
    execute_query(query, values)

def delete_record(table_name, condition_column, condition_value):
    query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
    values = (condition_value,)
    execute_query(query, values)

def search_records(table_name: str, search_column: str, search_value: str):
    db = connect_db()
    if not db:
        return
    try:
        cursor = db.cursor()
        query = f"SELECT * FROM {table_name} WHERE {search_column} LIKE %s"
        cursor.execute(query, (f"%{search_value}%",))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print(f"No records found for '{search_value}' in '{search_column}'.")
    except Error as e:
        print(f"Error searching records: {e}")
    finally:
        db.close()

def get_columns_and_values(prompt: str) -> Dict[str, str]:
    data = {}
    print(f"Enter {prompt} (type 'done' to finish):")
    while True:
        column = input("Column name: ").strip()
        if column.lower() == "done":
            break
        value = input(f"Value for {column}: ").strip()
        data[column] = value
    return data

def create_table(table_name: str, columns_and_types: Dict[str, str]):
    db = connect_db()
    if not db:
        return
    
    try:
        cursor = db.cursor()
        
        columns_definitions = ", ".join([f"{column} {data_type}" for column, data_type in columns_and_types.items()])
        
        create_table_query = f"CREATE TABLE {table_name} ({columns_definitions})"
        
        cursor.execute(create_table_query)
        db.commit()
        
        print(f"Table '{table_name}' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        db.close()

def create_table_as_select(new_table_name: str, select_query: str):
    db = connect_db()
    if not db:
        return
    try:
        cursor = db.cursor()
        create_table_query = f"CREATE TABLE {new_table_name} AS {select_query}"
        cursor.execute(create_table_query)
        db.commit()
        print(f"New table '{new_table_name}' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        db.close()

def drop_table(table_name: str):
    db = connect_db()
    if not db:
        return
    try:
        cursor = db.cursor()
        drop_table_query = f"DROP TABLE {table_name}"
        cursor.execute(drop_table_query)
        db.commit()
        print(f"Table '{table_name}' dropped successfully.")
    except Error as e:
        print(f"Error dropping table: {e}")
    finally:
        db.close()

def export_to_csv(table_name: str, file_path: str):
    db = connect_db()
    if not db:
        return
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([column[0] for column in cursor.description])
            writer.writerows(rows)

        print(f"Data exported successfully to {file_path}")
    except Error as e:
        print(f"Error exporting to CSV: {e}")
    finally:
        db.close()

def main():
    while True:
        print("\nWelcome to Tax Management System\n")
        print("Efficiently manage your tax records online with our comprehensive Tax Management System.\nThis system is designed to securely store, update and retrieve tax-related information,\nproviding a user-friendly experience for managing tax data.\n")

        print("Key Features\n")
        print("Create and Store Tax Records Securely: Maintain your tax data in a safe and secure environment.\nView and Search Records Quickly: Access and search records for efficient management.\nUpdate and Delete Outdated Information: Keep your tax records up-to-date by modifying or\nremoving outdated entries.\nExport Data to CSV for Reporting: Export your tax records to CSV format for easy reporting and analysis.\n")

        print("The Tax Management System is built on a well-structured relational database.\nBelow are the key tables and their roles:\n")

        print("1.Address: Stores user addresses, ensuring accurate and reliable address information.\n2.Citizen: Contains taxpayer details, including personal and identification information.\n3.TaxRates: Manages different types of tax rates for calculation purposes.\n4.Tax: Stores all tax records, including filing history and applicable tax details.\n5.TaxPayment: Tracks payments related to taxes, providing a clear payment history.\n6.Audit: Logs changes made to the database, ensuring accountability and traceability.\n7.UserRoles: Defines roles and permissions for users within the system.\n8.Users: Manages user accounts, including authentication and profile information.\n\n")


        print("1. Create Table")
        print("2. Insert Data")
        print("3. Read Data")
        print("4. Update Data")
        print("5. Delete Data")
        print("6. Search Records")
        print("7. Create Table As Select")
        print("8. Export to CSV")
        print("9. Drop Table")
        print("10. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            table_name = input("Enter table name: ").strip()
            columns_and_types = get_columns_and_values("columns and types")
            create_table(table_name, columns_and_types)
        
        elif choice == "2":
            table_name = input("Enter table name: ").strip()
            columns_and_values = get_columns_and_values("columns and values")
            columns = list(columns_and_values.keys())
            values = list(columns_and_values.values())
            create_record(table_name, columns, values)

        elif choice == "3":
            table_name = input("Enter table name: ").strip()
            columns = input("Enter columns to display (comma-separated, or '*' for all): ").split(",")
            read_table(table_name, columns)

        elif choice == "4":
            table_name = input("Enter table name: ").strip()
            update_column = input("Enter column to update: ").strip()
            update_value = input("Enter new value: ").strip()
            condition_column = input("Enter condition column: ").strip()
            condition_value = input("Enter condition value: ").strip()
            update_record(table_name, update_column, update_value, condition_column, condition_value)

        elif choice == "5":
            table_name = input("Enter table name: ").strip()
            condition_column = input("Enter condition column: ").strip()
            condition_value = input("Enter condition value: ").strip()
            delete_record(table_name, condition_column, condition_value)

        elif choice == "6":
            table_name = input("Enter table name: ").strip()
            search_column = input("Enter column to search: ").strip()
            search_value = input("Enter value to search: ").strip()
            search_records(table_name, search_column, search_value)

        elif choice == "7":
            new_table_name = input("Enter new table name: ").strip()
            select_query = input("Enter the SELECT query: ").strip()
            create_table_as_select(new_table_name, select_query)

        elif choice == "8":
            table_name = input("Enter table name: ").strip()
            file_path = input("Enter CSV file path: ").strip()
            export_to_csv(table_name, file_path)

        elif choice == "9":
            table_name = input("Enter table name: ").strip()
            drop_table(table_name)

        elif choice == "10":
            print("Exiting...Pay your tax timely for the betterment of the country.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
