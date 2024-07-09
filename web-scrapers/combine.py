import pandas as pd
import glob
import re

# Function to extract the numeric part of the filename
def extract_number(file_name):
    match = re.search(r'(\d+)', file_name)
    return int(match.group(1)) if match else 0

# Define the file pattern and get the list of files
file_pattern = 'web_scraped_content_chunk_*.csv'
file_list = glob.glob(file_pattern)

# Sort the file list using the custom function
file_list.sort(key=extract_number)

# Initialize an empty list to hold dataframes
df_list = []

# Read and store each dataframe in the list
for file in file_list:
    df = pd.read_csv(file)
    print(f"File: {file} | Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    df_list.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(df_list, ignore_index=True)

print(f"Combined DataFrame | Rows: {combined_df.shape[0]} | Columns: {combined_df.shape[1]}")

# Save the combined dataframe to a CSV file
combined_df.to_csv('fourth.csv', index=False)

print(f"Combined {len(file_list)} files into 'web_scraped_content_combined.csv'")
