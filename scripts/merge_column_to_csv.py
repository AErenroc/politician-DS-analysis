import pandas as pd
import os

"""
This script takes in two CSVs, CSV1 and CSV2.
It will then, for a specified column ex. 'E_codings', copy that column of CSV1 -- on to --> CSV2's respective column
"""
# File paths
TYPOLOGY_DIR = "typology_coding"
FILE1 = os.path.join(TYPOLOGY_DIR, "E_Xi_Jinping_Merged.csv")
FILE2 = os.path.join(TYPOLOGY_DIR, "Xi_Jinping_Merged.csv")
OUTPUT_FILE = os.path.join(TYPOLOGY_DIR, "UPDATED_Xi_Jinping_Merged.csv")

def copy_column(csv1_path, csv2_path, column_name, output_path):
    # Load both CSVs
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # Ensure column exists in both
    if column_name not in df1.columns:
        raise ValueError(f"{column_name} not found in {csv1_path}")
    if column_name not in df2.columns:
        raise ValueError(f"{column_name} not found in {csv2_path}")
    
    # Copy the column from CSV1 into CSV2
    df2[column_name] = df1[column_name]

    # Save result
    df2.to_csv(output_path, index=False)
    print(f"Saved updated file to {output_path}")


def main():
    copy_column(FILE1, FILE2, "codings", OUTPUT_FILE) # Can change "codings" with ex "Z_codings"

if __name__ == "__main__":
    main()