# testing-data-etl
ETL workflows for transforming and preparing student data for reporting and analysis.

# Student Data ETL Pipeline

## Overview
This project demonstrates an ETL (Extract, Transform, Load) workflow for processing student assessment data into a structured format for reporting and system integration.

The script reads raw testing data from an Excel file, transforms it into standardized records, and outputs clean datasets ready for downstream systems.

---

## Problem
Raw assessment data often contains:

- inconsistent formatting
- combined fields (e.g., names, score ranges)
- missing or invalid identifiers
- multiple score types within a single dataset

These issues make it difficult to load data into reporting systems or vendor platforms.

---

## Solution
This script performs:

- Data extraction from Excel files using pandas
- Data cleaning and normalization
- Name parsing and formatting
- Score transformation (numeric and range-based)
- Date standardization
- Handling of missing or invalid student IDs
- Generation of structured output records for multiple test components

The output is formatted for compatibility with downstream systems and vendor integrations.

---

## Features

- Splits student names into first/last format
- Handles missing or invalid student identifiers with fallback logic
- Converts date formats into standardized YYYY-MM-DD format
- Supports both numeric scores and score ranges
- Generates multiple test records per student based on defined test structures
- Outputs data in multiple formats:
  - CSV
  - TSV
  - TXT

---

## Technologies Used

- Python
- pandas
- openpyxl (for Excel input)
