# Data-Cleaning-Reporting-Automation
This repository contains a projects completed during the Thiranex internship.

# Data Cleaning & Reporting Automation Pipeline

An automated data engineering pipeline built in Python to ingest, clean, and process dirty corporate airline data into ready-to-use executive reports.

## Key Features
* **Automated Data Type Enforcement:** Standardizes string formatting (Title casing), removes hidden string artifacts (`.`), and converts inconsistent objects to `datetime` values.
* **Missing Value Imputation:** Automates null handling across key numeric performance indicators.
* **Multi-Sheet Reporting Engine:** Aggregates and groups data into tailored corporate metric sheets (Tiers & Demographics).

## Architecture & Tech Stack
* **Language:** Python 3.14
* **Libraries:** Pandas, OpenPyXL, NumPy
* **Target Source Data:** 62,000+ Frequent Flyer Program records (`flight.csv`)

## How to Run
1. Clone the repository.
2. Place your raw `flight.csv` file in the root folder.
3. Run `python transform.py`.
