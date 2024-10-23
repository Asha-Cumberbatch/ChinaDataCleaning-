# Data Cleaning and Processing Script for Car Owner Dataset
![datacleaning](datacleaning.jpg)

# Data Cleaning for Car Owners Nationwide

This project involves cleaning a dataset containing information about car owners, specifically focusing on various attributes such as contact information, demographics, and vehicle details. The goal is to prepare the data for further analysis by identifying and removing invalid records while preserving useful information.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Description](#dataset-description)
3. [Code Explanation](#code-explanation)
4. [Data Cleaning Process](#data-cleaning-process)
5. [Results](#results)
6. [Visualization of Cleaned Data](#visualization-of-cleaned-data)
7. [How to Run the Code](#how-to-run-the-code)

## Project Overview

This repository contains a Python script that utilizes the Pandas library for data manipulation. The script performs the following tasks:
- Loads the dataset.
- Maps Chinese column names to English.
- Cleans and normalizes the data, focusing on email addresses and identifying invalid records.
- Merges certain columns for better readability.
- Outputs cleaned and garbage data to separate CSV files.

## Dataset Description

The dataset (`CarOwnersNationwide.csv`) includes the following columns (translated to English):
- **VIN**: Vehicle Identification Number
- **Name**: Owner's Name
- **ID_Number**: Identity Number
- **Gender**: Gender of the owner
- **Phone**: Phone number
- **Email**: Email address
- **Province**: Province of residence
- **City**: City of residence
- **Address**: Full address
- **Postal_Code**: Postal code
- **Birthday**: Date of birth
- **Industry**: Industry of employment
- **Monthly_Salary**: Monthly salary
- **Marital_Status**: Marital status
- **Education**: Education level
- **Brand**: Vehicle brand
- **Car_Series**: Series of the vehicle
- **Car_Model**: Model of the vehicle
- **Configuration**: Configuration details
- **Color**: Vehicle color
- **Engine_Number**: Engine number

## Code Explanation

The main script performs the following steps:

1. **Import Necessary Libraries**: Utilizes `pandas` for data manipulation and `numpy` for handling numerical operations.
2. **Suppress Warnings**: Disables FutureWarnings for cleaner output.
3. **Load Dataset**: Reads the CSV file with `low_memory=False` to avoid data type warnings.
4. **Rename Columns**: Translates Chinese column names to English for easier handling.
5. **Normalize Email Addresses**: Strips spaces and converts emails to lowercase.
6. **Identify Invalid Emails**: Marks emails containing specific keywords as invalid and replaces them with 'NULL'.
7. **Identify Consecutive Commas**: Flags rows with four consecutive commas.
8. **Remove Duplicates**: Moves duplicate records based on specific criteria to the garbage DataFrame.
9. **Merge Address Fields**: Combines address-related fields into a single column.
10. **Save Cleaned and Garbage Data**: Outputs the cleaned data and garbage records to separate CSV files.

## Data Cleaning Process

### Invalid Email Identification
Emails containing terms like "noemail" or "nomail" are marked as invalid. The script replaces these entries with 'NULL' for further processing.

### Consecutive Commas
Rows with four consecutive commas in any field are flagged for garbage data, indicating potential issues in record formatting.

### Duplicate Handling
Records that are duplicates based on VIN, Email, or ID Number are moved to the garbage DataFrame to ensure a clean dataset.

### Address Combination
Address components (Address, City, Province, and Postal_Code) are merged into a single column called `Full_Address`, improving data usability.

## Results

The output of the data cleaning process includes two CSV files:
- `merged_cleaned_data.csv`: Contains the cleaned data ready for analysis.
- `merged_garbage_data.csv`: Contains the records identified as garbage with reasons for their exclusion.

### Cleaned Data Statistics
- **Total Cleaned Rows**: (Insert the total cleaned rows here)
- **Total Garbage Rows**: (Insert the total garbage rows here)
- **Ratio of Clean to Garbage Rows**: (Insert the ratio here)

## Visualization of Cleaned Data

![Cleaned Data Sample](clean.jpg)

*This image shows a sample of the cleaned data, highlighting the structure and fields retained for analysis.*

## How to Run the Code

1. Ensure you have Python installed along with the necessary libraries: `pandas` and `numpy`.
2. Download the repository or copy the script into your local environment.
3. Update the `file_path` variable in the script to point to the location of your `CarOwnersNationwide.csv` file.
4. Run the script to perform the data cleaning process.
5. The cleaned and garbage data files will be saved in the specified output directory.

## Conclusion

This project successfully demonstrates an effective approach to data cleaning using Python, providing a structured methodology to enhance the quality of datasets for analysis. The resulting cleaned dataset can be further utilized for analytics or machine learning applications.

## Credits
- Asha Cumberbatch
