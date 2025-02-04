# Tax-Management-System

## Project Overview

**Project Title**: Tax Management System

This project demonstrates the implementation of a Tax Management System using SQL. It includes creating and managing tables, performing CRUD operations, and executing advanced SQL queries. The goal is to showcase skills in database design, manipulation, and querying.

![ERD](https://github.com/Sushmoy-Nandi/Tax-Management-System/blob/main/Tax_Manegement_System_ERD.png)

## Objectives

1. **Set up the Tax Management System Database**: Create and populate the database `tax_management_system` with tables for UserSignup, TaxPayers, TaxPayment, LandTax, BusinessTax, IncomeTax.
2. **CRUD Operations**: Perform Create, Read, Update, and Delete operations on the data.
4. **Search Records**: Search for specific records in the database.

**Database:**

*   The system utilizes a MySQL database to store user information, tax records, and payment details.
*   Key tables include:
    - `UserSignup`: Stores user information (NID, PhoneNumber, Email, HashedPassword)
    - `TaxPayers`: Stores taxpayer information (TaxPayerID, NID, Name, DOB, Gender, Address, Status)
    - `TaxPayment`: Stores general tax payment information (TaxID, TaxPayerID, NID, TaxType, TaxAmount, PaidAmount, DueAmount, DueDate)
    - `LandTax`: Stores specific details for Land Tax (LandTaxID, PropertyLocation, PropertySize, PropertyValue, TaxPayerNID)
    - `IncomeTax`: Stores specific details for Income Tax (IncomeTaxID, AnnualIncome, TaxableIncome, TaxPayerNID)
    - `BusinessTax`: Stores specific details for Business Tax (BusinessTaxID, BusinessName, BusinessType, AnnualRevenue, TaxPayerNID)

**Features:**

1. **User Registration:** 
    - Allows users to register with their NID (National Identification Number), phone number, and email address.
    - Implements strong password hashing for enhanced security.

2. **User Login:**
    - Enables users to log in to the system using their NID and password.
    - Verifies user credentials against the database.

3. **User Dashboard:** 
- Will allow users to:
    - **View Tax Status:** Displays the user's tax records with their current status (Paid, Unpaid, Overdue).
    - **View Payment History:** Shows a history of all tax payments made by the user.
    - **Edit User Information:** Allows users to update their phone number, email address, and password.
    - **Add New Tax Entity:** Enables users to add new tax entities (Land Tax, Income Tax, Business Tax) with relevant details and automatically calculates and records the tax amount.

4. **Admin Dashboard:** 
- Provides an administrative interface with the following functionalities:
    - **View All Tax Records:** Displays a list of all tax records.
    - **Add New Tax Record:** Allows administrators to add new tax records for different tax types (Land Tax, Income Tax, Business Tax).
    - **Edit Tax Record:** Enables administrators to modify existing tax record details. 
    - **Delete Tax Record:** Allows administrators to delete existing tax records.
    - **View Tax Payments with Status:** Displays tax payments with their status (Paid, Unpaid, Overdue).
    - **View All Tax Payers:** Displays a list of all registered taxpayers.
    - **Search Records:** Allows administrators to search for records across different tables based on specified criteria (table name, column, and search value). 
        
## Project Structure

### **Database Creation**
```sql
CREATE DATABASE tax_management_system;
USE tax_management_system;
```

### **Table Creation**

1. **UserSignup Table**
```sql
CREATE TABLE UserSignup (
    SignupID INT PRIMARY KEY AUTO_INCREMENT,
    NID INT,
    PhoneNumber VARCHAR(20),
    Email VARCHAR(50),
    Password VARCHAR(255),  -- Encrypted password
    SignupStatus VARCHAR(20) DEFAULT 'Pending', -- Pending, Verified, Expired
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    
);
```
2. **TaxPayers Table**
```sql
CREATE TABLE Citizen (
    NID INT PRIMARY KEY,
    Name VARCHAR(255),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    AddressID INT,
    PhoneNumber VARCHAR(20),
    Email VARCHAR(100),
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE SET NULL
);
```
3. **TaxPayment Table**
```sql
CREATE TABLE TaxPayment (
    TaxID INT PRIMARY KEY AUTO_INCREMENT,
    NID INT NULL,
    TaxType ENUM('Land Tax', 'Income Tax', 'Business Tax') NOT NULL,  -- Use ENUM for better control over types
    TaxAmount DECIMAL(10, 2),
    PaidAmount DECIMAL(10, 2) DEFAULT 0,
    DueAmount DECIMAL(10, 2) AS (TaxAmount - PaidAmount) STORED,
    DueDate DATE,
    FOREIGN KEY (NID) REFERENCES UserSignup(NID) ON DELETE CASCADE
);
```
4. **LandTax Table**
```sql
CREATE TABLE LandTax (
    LandTaxID INT PRIMARY KEY AUTO_INCREMENT,
    PropertyLocation VARCHAR(255), 
    PropertySize DECIMAL(10, 2), 
    PropertyValue DECIMAL(10, 2),
    TaxPayerNID INT,
    FOREIGN KEY (TaxPayerNID) REFERENCES UserSignup(NID)
);
```
5. **IncomeTax Table**
```sql
 CREATE TABLE IncomeTax (
    IncomeTaxID INT PRIMARY KEY AUTO_INCREMENT,
    AnnualIncome DECIMAL(10, 2),  -- Total annual income
    TaxableIncome DECIMAL(10, 2), -- Portion of the income that is taxable
    TaxPayerNID INT,
    FOREIGN KEY (TaxPayerNID) REFERENCES UserSignup(NID)
);
```
6. **BusinessTax Table**
```sql
CREATE TABLE BusinessTax (
    BusinessTaxID INT PRIMARY KEY AUTO_INCREMENT,
    BusinessName VARCHAR(255),  -- Name of the business
    BusinessType VARCHAR(100),  -- Type of business (e.g., Retail, Manufacturing)
    AnnualRevenue DECIMAL(10, 2),  -- Total revenue for the year
    TaxPayerNID INT,
    FOREIGN KEY (TaxPayerNID) REFERENCES UserSignup(NID)
);
```

## Requirements

* Python Version 3.13.1
* MySQL Database
* `mysql-connector-python` library: `pip install mysql-connector-python`
* `prettytable` library: `pip install prettytable`
* `bcrypt` library: `pip install bcrypt`

**Dependencies:**

*   `mysql-connector-python`: For interacting with the MySQL database.
*   `bcrypt`: For secure password hashing.
*   `prettytable`: For generating formatted table outputs.

**Installation:**

1.  **Install dependencies:**
    ```bash
    pip install mysql-connector-python bcrypt prettytable
    ```

2.  **Configure database connection:** Update the `connect_db()` function in `connect_db.py` with your actual database credentials (host, user, password, database name).

3.  **Run the application:** Execute the `main.py` script to start the system.

## Project Details
This project was developed during the 4th semester while pursing B.Sc. in CSE of 2024 as part of the CSE-2211: Database Management Systems-I Lab Course conducted by the National Institute of Textile Engineering and Research-NITER, Constituent Institute of the University of Dhaka, Savar, Dhaka-1350

## Future Enhancements:

*   Develop a user-friendly web interface for better user experience.
*   Add features like tax calculators and automated tax reminders.
*   Improve security measures, such as implementing two-factor authentication.

## Conclusion

This project successfully implements a basic tax management system with core functionalities for user registration, login, and tax record management. The system effectively utilizes a MySQL database to store and retrieve user and tax-related information.