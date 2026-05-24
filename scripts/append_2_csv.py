import os
import pandas as pd

"""
TODO: Merges two csv of articles without repeating uuids 
( (union of csv's uuid) - (intersection of csv's uudis) )
or just track already visited uuids
"""
# File paths
TYPOLOGY_DIR = "typology_coding"
FILE1 = os.path.join(TYPOLOGY_DIR, "Xi_jinping_articles_for_coding.csv")
FILE2 =  os.path.join(TYPOLOGY_DIR, "Xi_Jinping_NA_Articles_for_coding.csv")
OUTPUT_FILE = os.path.join(TYPOLOGY_DIR, "Xi_Jinping_Merged.csv")

# Load CSVs
df1 = pd.read_csv(FILE1)
df2 = pd.read_csv(FILE2)

# Take first 250 rows of df1
df1_subset = df1.head(250)

# Append df1_subset before df2
merged = pd.concat([df1_subset, df2], ignore_index=True)

# Save
merged.to_csv(OUTPUT_FILE, index=False)

print(f"Merged file saved as {OUTPUT_FILE}")