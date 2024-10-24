import pandas as pd
import numpy as np
import warnings
import os

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Load the dataset with low_memory set to False to prevent DtypeWarning
file_path = 'C:/Users/aaack/OneDrive/Desktop/ProtexxaAI/DataCleaning/CarOwnersNationwide.csv'
data = pd.read_csv(file_path, low_memory=False)

# Mapping of Chinese column names to English
column_mapping = {
    '车架号': 'VIN',
    '姓名': 'Name',
    '身份证': 'ID_Number',
    '性别': 'Gender',
    '手机': 'Phone',
    '邮箱': 'Email',
    '省': 'Province',
    '城市': 'City',
    '地址': 'Address',
    '邮编': 'Postal_Code',
    '生日': 'Birthday',
    '行业': 'Industry',
    '月薪': 'Monthly_Salary',
    '婚姻': 'Marital_Status',
    '教育': 'Education',
    'BRAND': 'Brand',
    '车系': 'Car_Series',
    '车型': 'Car_Model',
    '配置': 'Configuration',
    '颜色': 'Color',
    '发动机号': 'Engine_Number'
}

# Rename the columns
data.rename(columns=column_mapping, inplace=True)

# Normalize the email addresses by stripping spaces and converting to lowercase
data['Email'] = data['Email'].str.strip().str.lower()

# Create a column for garbage reasons, initialized with empty strings
garbage_reasons = [''] * len(data)

# Replace the entire email with 'NULL' if it contains 'noemail' or 'nomail'
invalid_email_mask = data['Email'].replace(to_replace=r'.*(noemai|nomai|noemia|nomea|noemal|noeami|nomei|noma|noemil|noeai).*', value='NULL', regex=True) == 'NULL'
garbage_reasons = np.where(invalid_email_mask, 'Invalid Email', garbage_reasons)

# Identify rows with invalid emails (excluding NULL)
valid_email_mask = data['Email'].str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)
invalid_email_mask = ~((data['Email'] == 'NULL') | valid_email_mask)

# Keep invalid email records if VIN, Name, ID_Number, and Full_Address are present
required_columns_mask = data[['VIN', 'Name', 'ID_Number']].notnull().all(axis=1)
data['Full_Address'] = data['Address'].astype(str).fillna('') + ', ' + \
                       data['City'].astype(str).fillna('') + ', ' + \
                       data['Province'].astype(str).fillna('') + ', ' + \
                       data['Postal_Code'].astype(str).fillna('')

full_address_mask = data['Full_Address'].str.strip() != ', , , '

# Records to be moved to garbage due to invalid email, if key fields are missing
invalid_email_garbage_mask = invalid_email_mask & ~(required_columns_mask & full_address_mask)
garbage_reasons = np.where(invalid_email_garbage_mask, 'Invalid Email', garbage_reasons)

# Identify rows with four consecutive commas
consecutive_comma_mask = data.apply(lambda x: ',,,,' in ','.join(x.dropna().astype(str)), axis=1)
garbage_reasons = np.where(consecutive_comma_mask, 'Consecutive Commas', garbage_reasons)

# Combine invalid email (for records without required fields) and consecutive comma masks
combined_mask = invalid_email_garbage_mask | consecutive_comma_mask

# Create garbage DataFrame with reasons
garbage = data[combined_mask].copy()
garbage['Reason'] = garbage_reasons[combined_mask]

# Identify and move duplicates based on VIN, Email, and ID_Number to the garbage DataFrame
duplicates_mask = data.duplicated(subset=['VIN', 'Email', 'ID_Number'], keep=False)
duplicates = data[duplicates_mask].copy()
duplicates['Reason'] = 'Duplicate Record'

# Combine original garbage DataFrame with duplicates
garbage = pd.concat([garbage, duplicates], ignore_index=True)

# Save the columns to be dropped into a separate DataFrame for garbage
dropped_columns = data[['Postal_Code', 'Province', 'City', 'Address', 'Monthly_Salary', 'Marital_Status', 'Education', 'Color', 'Unnamed: 21', 'Gender', 'Industry', 'Configuration']].copy()
dropped_columns['Reason'] = 'Dropped Column'

# Append the dropped columns to the garbage DataFrame but exclude them from the final garbage row count
garbage_with_dropped_columns = pd.concat([garbage, dropped_columns], ignore_index=True)

# Now create the cleaned data by removing garbage rows and duplicates
data_cleaned = data[~(combined_mask | duplicates_mask)].copy()

# Drop the specified columns after merging into Full_Address
columns_to_drop = ['Postal_Code', 'Province', 'City', 'Address', 'Monthly_Salary', 'Marital_Status', 'Education', 'Color', 'Unnamed: 21', 'Gender', 'Industry', 'Configuration']
data_cleaned.drop(columns=columns_to_drop, inplace=True)

# Save cleaned and garbage data to CSV files
output_dir = 'C:/Users/aaack/OneDrive/Desktop/ProtexxaAI/DataCleaning/'

data_cleaned.to_csv(f'{output_dir}merged_cleaned_data.csv', index=False, encoding='utf-8-sig')
garbage_with_dropped_columns.to_csv(f'{output_dir}merged_garbage_data.csv', index=False, encoding='utf-8-sig')

# Calculate and display the total cleaned and garbage rows, excluding dropped columns from garbage count
total_cleaned_rows = len(data_cleaned)
total_garbage_rows = len(garbage)  # Count rows in the garbage DataFrame before appending dropped columns

# Calculate and display the ratio of clean to garbage rows
if total_garbage_rows > 0:
    ratio = total_cleaned_rows / total_garbage_rows
else:
    ratio = float('inf')  # Avoid division by zero

print(f"Total cleaned rows: {total_cleaned_rows}")
print(f"Total garbage rows (excluding dropped columns): {total_garbage_rows}")
print(f"Ratio of clean rows to garbage rows: {ratio:.2f}")

print("Merged cleaned and garbage files saved successfully.")
