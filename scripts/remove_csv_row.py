"""
For removing repeated articles found after coding
"""
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Remove a specific row from a CSV and reset index."
    )

    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("row_index", type=int, help="Index of the row to remove")
    parser.add_argument("output_csv", help="Path to save the updated CSV")

    args = parser.parse_args()

    # Load CSV normally — do NOT use index_col
    df = pd.read_csv(args.input_csv)

    if "index" not in df.columns:
        raise ValueError("The CSV does not contain an 'index' column.")

    # Ensure the index_value exists
    if args.index_value not in df["index"].values:
        raise ValueError(f"Row with index={args.index_value} not found in CSV.")

    # Remove the row where the explicit 'index' column matches
    df = df[df["index"] != args.index_value]

    # Reset the index column to 0 -- N-1
    df = df.reset_index(drop=True)
    df["index"] = df.index

    # Save
    df.to_csv(args.output_csv, index=False)

    print(f"Removed row with index={args.index_value}. Saved to {args.output_csv}")
    

if __name__ == "__main__":
    main()