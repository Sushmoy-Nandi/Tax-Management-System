# Tax-Management-System

## Project Overview

**Project Title**: Tax Management System

This project demonstrates the implementation of a Tax Management System using SQL. It includes creating and managing tables, performing CRUD operations, and executing advanced SQL queries. The goal is to showcase skills in database design, manipulation, and querying.

![ERD](https://github.com/Sushmoy-Nandi/Tax-Management-System-/blob/main/Tax_Management_System_ERD.png)

## Objectives

1. **Set up the Tax Management System Database**: Create and populate the database with tables for Citizen, Address, TaxRates, Tax, TaxPayment, Audit, UserRoles, Users.
2. **CRUD Operations**: Perform Create, Read, Update, and Delete operations on the data.
3. **CTAS (Create Table As Select)**: Utilize CTAS to create new tables based on query results.
4. **Advanced SQL Queries**: Develop complex queries to analyze and retrieve specific data.

## Project Structure

### **Database Creation**
```sql
CREATE DATABASE tax_management_system;
USE tax_management_system;
```

### **Table Creation**

1. **Address Table**
```sql
CREATE TABLE Address (
    AddressID INT PRIMARY KEY,
    Street VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    PostalCode VARCHAR(20),
    Country VARCHAR(100)
);
```
2. **Citizen Table**
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
3. **TaxRates Table**
```sql
CREATE TABLE TaxRates (
    TaxRateID INT PRIMARY KEY,
    TaxType VARCHAR(50),
    RateDescription VARCHAR(255),
    RatePercentage DECIMAL(5, 2),
    EffectiveDate DATE,
    ExpiryDate DATE
);
```
4. **Tax Table**
```sql
CREATE TABLE Tax (
    TaxID INT PRIMARY KEY,
    NID INT,
    TaxType VARCHAR(50),
    TaxDescription TEXT,
    TaxBaseAmount DECIMAL(10, 2),
    TaxRateID INT,
    TaxAmount DECIMAL(10, 2),
    DueDate DATE,
    FOREIGN KEY (NID) REFERENCES Citizen(NID) ON DELETE CASCADE,
    FOREIGN KEY (TaxRateID) REFERENCES TaxRates(TaxRateID) ON DELETE SET NULL
);
```
5. **TaxPayment Table**
```sql
CREATE TABLE TaxPayment (
    PaymentID INT PRIMARY KEY,
    TaxID INT,
    PaymentDate DATE,
    PaymentAmount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (TaxID) REFERENCES Tax(TaxID) ON DELETE CASCADE
);
```
6. **UserRoles Table**
```sql
CREATE TABLE UserRoles (
    RoleID INT PRIMARY KEY,
    RoleName VARCHAR(50)
);
```
7. **Users Table**
```sql
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    NID INT,
    RoleID INT,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(255),
    Email VARCHAR(100),
    FOREIGN KEY (NID) REFERENCES Citizen(NID) ON DELETE CASCADE,
    FOREIGN KEY (RoleID) REFERENCES UserRoles(RoleID) ON DELETE SET NULL
);
```
8. **Audit Table**
```sql
CREATE TABLE Audit (
    AuditID INT AUTO_INCREMENT PRIMARY KEY,
    EntityName VARCHAR(100) NOT NULL,
    EntityID INT NOT NULL,
    ChangeDescription TEXT NOT NULL,
    ChangedBy INT,  -- Assuming it references Users(UserID)
    ChangeDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ChangedBy) REFERENCES Users(UserID) ON DELETE SET NULL
);
```

## CRUD Operation

Below is an example of performing **CRUD (Create, Read, Update, Delete)** operations for the `tax_management_system` database:

### **1. CREATE Operation**
Add a new citizen and their related data in the `Address`, `Citizen`, and `Tax` tables.

```sql
-- Insert into Address
INSERT INTO Address (AddressID, Street, City, State, PostalCode, Country)
VALUES 
(11, 'New Market Road', 'Dhaka', 'Dhaka Division', '1215', 'Bangladesh');

-- Insert into Citizen
INSERT INTO Citizen (NID, Name, DateOfBirth, Gender, AddressID, PhoneNumber, Email)
VALUES 
(111, 'Rafiqul Islam', '1992-05-14', 'Male', 11, '01712345678', 'rafiqulislam@example.com');

-- Insert into Tax
INSERT INTO Tax (TaxID, NID, TaxType, TaxDescription, TaxBaseAmount, TaxRateID, TaxAmount, DueDate)
VALUES 
(11, 111, 'Income Tax', 'Tax on annual salary', 600000.00, 1, 60000.00, '2024-04-30');
```

---

### **2. READ Operation**
Retrieve specific or all records from various tables.

- Retrieve all citizens from Dhaka:
```sql
SELECT c.NID, c.Name, c.Email, a.Street, a.City
FROM Citizen c
JOIN Address a ON c.AddressID = a.AddressID
WHERE a.City = 'Dhaka';
```

- Retrieve all unpaid taxes with a due date in the future:
```sql
SELECT t.TaxID, t.NID, t.TaxType, t.TaxAmount, t.DueDate
FROM Tax t
WHERE t.DueDate > CURRENT_DATE;
```

- Retrieve total taxes paid by a specific citizen:
```sql
SELECT c.NID, c.Name, SUM(tp.PaymentAmount) AS TotalTaxPaid
FROM Citizen c
JOIN Tax t ON c.NID = t.NID
JOIN TaxPayment tp ON t.TaxID = tp.TaxID
WHERE c.NID = 111
GROUP BY c.NID, c.Name;
```

---

### **3. UPDATE Operation**
Update details for an existing record.

- Update phone number and email for a citizen:
```sql
UPDATE Citizen
SET PhoneNumber = '01876543210', Email = 'updatedrafiqul@example.com'
WHERE NID = 111;
```

- Update tax amount for a specific tax record:
```sql
UPDATE Tax
SET TaxAmount = 65000.00
WHERE TaxID = 11;
```

- Extend expiry date for a tax rate:
```sql
UPDATE TaxRates
SET ExpiryDate = '2026-12-31'
WHERE TaxRateID = 1;
```

---

### **4. DELETE Operation**
Remove specific records from tables.

- Delete a citizen and their associated taxes:
```sql
DELETE FROM Citizen
WHERE NID = 111;
```
> **Note**: `ON DELETE CASCADE` will automatically remove related `Tax` records for the citizen.

- Delete a tax rate that is no longer valid:
```sql
DELETE FROM TaxRates
WHERE TaxRateID = 10;
```

- Remove a tax payment record:
```sql
DELETE FROM TaxPayment
WHERE PaymentID = 1;
```

---

### Testing the CRUD Operations
Verify the results of these operations using `SELECT` queries:

- Check if the citizen was added successfully:
```sql
SELECT * FROM Citizen WHERE NID = 111;
```

- Verify the updated tax amount:
```sql
SELECT * FROM Tax WHERE TaxID = 11;
```

- Ensure that the citizen and related taxes were deleted:
```sql
SELECT * FROM Citizen WHERE NID = 111;
SELECT * FROM Tax WHERE NID = 111;
```

- Confirm if the tax payment record was removed:
```sql
SELECT * FROM TaxPayment WHERE PaymentID = 1;
```