"""
Collects all the articles in a politician folder (ex. data/[politician-name]) and converts 
them to a CSV where, rows -> articles. The CSV contains the columns "uuid","title","description","snippet","url",
"source", "language","published_at" as well as three new empty columns for manual coding, more can be added by 
modifying this .py and typology_coding_helper.py.
"""


import os
import json
import csv
# Paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(os.path.dirname(PROJECT_DIR), "data")

POLITICIAN_NAME = "Xi Jinping"
SAFE_NAME = POLITICIAN_NAME.replace(" ", "_")
POLITICIAN_DIR = os.path.join(DATA_DIR, 'Xi_Jinping_NA_Articles')#SAFE_NAME)


def main():
    
    # Output folder and file
    OUTPUT_DIR = "typology_coding"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'Xi_Jinping_NA_Articles_for_coding.csv') #"Xi_Jinping_articles_for_coding.csv") 

    # ---!!! DO NOT OVERWRITE EXISTING CSV !!!--- (do not want to lose all of our coding work!!! do not modify this!)
    if os.path.exists(OUTPUT_CSV):
        print(f" CSV already exists! - - not updating: {OUTPUT_CSV}")
        return

    # Collect all json files in POLITICIAN_DIR (except cache.json)
    article_files = [
        f for f in os.listdir(POLITICIAN_DIR)
        if f.endswith(".json") and f != 'cache.json'
    ]

    rows = []

    count = 1

    for filename in article_files:
        filepath = os.path.join(POLITICIAN_DIR, filename)

        try:
            with open(filepath, "r") as f:
                article = json.load(f)

            # Ensure all fields exist, if missing, insert ""
            rows.append({
                "index": count,

                "uuid": article.get("uuid", ""),
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "snippet": article.get("snippet", ""),
                "url": article.get("url", ""),
                "source": article.get("source", ""),

                "language": article.get("language", ""),
                "published_at": article.get("published_at", ""),
                "categories": ",".join(article.get("categories", [])),

                # New empty columns for manual coding
                "E_codings": "",
                "S_codings": "",
                "Z_codings": ""
            })

            count += 1

        except json.JSONDecodeError:
            print(f"Could not decode JSON in: {filename}")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # Write CSV
    if rows:
        fieldnames = rows[0].keys()

        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Saved CSV with {len(rows)} articles -> {OUTPUT_CSV}")
    else:
        print("No valid articles found!")

if __name__ == "__main__":
    main()