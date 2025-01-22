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