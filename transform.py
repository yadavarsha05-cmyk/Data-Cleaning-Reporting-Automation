import pandas as pd
import numpy as np

def clean_flight_data(file_path):
    # 1. Load the raw file
    df = pd.read_csv(file_path)
    
    # 2. Convert date strings to standardized datetime objects
    date_cols = ['FFP_DATE', 'FIRST_FLIGHT_DATE', 'LAST_FLIGHT_DATE', 'LOAD_TIME']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # 3. Handle hidden string placeholders (like '.') and whitespace in text fields
    text_cols = ['WORK_CITY', 'WORK_PROVINCE', 'WORK_COUNTRY', 'GENDER']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        # Replace lone dots or empty strings with actual NaN values
        df[col] = df[col].replace(['.', 'nan', ''], np.nan)
        # Standardize capitalization (Title Case looks best for reports)
        df[col] = df[col].str.title()

    # 4. Impute missing numeric values using medians
    df['AGE'] = df['AGE'].fillna(df['AGE'].median())
    df['SUM_YR_1'] = df['SUM_YR_1'].fillna(0) # Assume 0 revenue if blank
    df['SUM_YR_2'] = df['SUM_YR_2'].fillna(0)
    
    # 5. Drop rows missing critical tracking info (like missing Gender or Country if required)
    df.dropna(subset=['GENDER', 'WORK_COUNTRY'], inplace=True)
    
    return df
# Call the function with your specific file
cleaned_df = clean_flight_data('flight.csv')

# Print the first few rows to confirm it works
print(cleaned_df.head())

# --- RUN THE CLEANING PIPELINE ---
cleaned_df = clean_flight_data('flight.csv')

# --- GENERATE AUTOMATED REPORTS ---
print("Generating automated summaries...")

# 1. Tier Metrics (How much revenue/points do different frequent flyer tiers generate?)
tier_summary = cleaned_df.groupby('FFP_TIER').agg(
    Total_Members=('MEMBER_NO', 'count'),
    Total_Flights=('FLIGHT_COUNT', 'sum'),
    Total_Points=('Points_Sum', 'sum'),
    Avg_Discount=('avg_discount', 'mean')
).reset_index()

# 2. Gender Demographics Summary
gender_summary = cleaned_df.groupby('GENDER').agg(
    Total_Members=('MEMBER_NO', 'count'),
    Total_Flights=('FLIGHT_COUNT', 'sum')
).reset_index()

# --- EXPORT TO EXCEL ---
output_filename = 'flight_automation_report.xlsx'

with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
    # Save the main pristine cleaned data
    cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
    
    # Save your summary insights sheets
    tier_summary.to_excel(writer, sheet_name='Tier Summary', index=False)
    gender_summary.to_excel(writer, sheet_name='Demographics Summary', index=False)

print(f"🎉 Success! Automated report generated and saved as '{output_filename}'")