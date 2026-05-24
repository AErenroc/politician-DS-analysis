import os
import csv

TOPIC_CATEGORIES = {
    "0": "Domestic economic policy",
    "1": "Foreign economic policy",
    "2": "Diplomatic relations",
    "3": "Domestic social policy",
    "4": "Foreign social policy",
    "5": "Military policy",
    "6": "Biographic",
    "7": "Internal politics"
}

SENTIMENT_CATEGORIES = {
    "0": "Positive",
    "1": "Neutral",
    "2": "Negative",
}

POLITICIAN_NAME = "Xi Jinping" 
SAFE_NAME = POLITICIAN_NAME.replace(" ", "_")

TYPOLOGY_DIR = "typology_coding"
CSV_TO_CODE = os.path.join(TYPOLOGY_DIR, 'Erin_Xi_Jinping_Merged.csv') #"Xi_jinping_articles_for_coding.csv") 


def choose_coding_column():
    # Choose coding column from user input
    print("Choose which column to code:")
    print("  0 --> E_codings")
    print("  1 --> S_codings")
    print("  2 --> Z_codings\n")

    col_choice = input("[Enter choice]: ").strip()
    if col_choice == "0":
        coding_column = "E_codings"
    elif col_choice == "1":
        coding_column = "S_codings"
    elif col_choice == "2":
        coding_column = "Z_codings"
    else:
        print("Invalid choice.")
        return
    print("-" * 30)
    return coding_column

def display_article_info(i,rows, article, coding_column):
    print("=" * 70)
    print(f"\tArticle {i+1}/{len(rows)}")
    print(f"\tTITLE:   {article['title']}\n")
    print(f"\tDESCRIPTION: {article['description']}\n")
    print(f"\tSNIPPET: {article['snippet']}\n")
    print(f"\tURL: {article['url']}\n")
    print("\tExisting code: ", article[coding_column] or "!! None !!")
    
def display_topic_categories():
    print("\n\t _____Choose a topic category:__________")
    for key, value in TOPIC_CATEGORIES.items():
        print(f"\t\t  {key} --> {value}")

def display_sentiment_categories():
    print("\n\t _____Choose sentiment:_________ _")
    print("\t\t  0 --> Positive")
    print("\t\t  1 --> Neutral")
    print("\t\t  2 --> Negative")

def load_csv():
    with open(CSV_TO_CODE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows


def get_start_index(total_rows):
     #  GET STARTING ROW 
    print("-" * 30)
    print(f"\nEnter row number to start from (1–{total_rows})")
    print("Press Enter to start from the beginning.")
    start_input = input("[ Start from row ]: ").strip()

    if start_input.isdigit():
        start_index = max(0, min(int(start_input) - 1, total_rows - 1))
    else:
        start_index = 0
    print(f"\n Starting coding at row {start_index + 1}\n")

    return start_index



def main():

    # Check csv exists
    if not os.path.exists(CSV_TO_CODE):
        print(f"Whoops! No CSV found at {CSV_TO_CODE}")
        return



    print(f"========= {POLITICIAN_NAME} Article Typology Coding Tool ==============================\n")
   
    # First get which user we are coding for
    coding_column = choose_coding_column()
    if coding_column == None:
        print("=" * 30)
        return
    print(f"\n Coding into columns: {coding_column}")


    # Load csv
    rows = load_csv()
    fieldnames = rows[0].keys()

    total_rows = len(rows)
    start_index = get_start_index(total_rows)   # Gets start_index from user, will start coding at that index


    # Loop through articles(rows) to code
    for i in range(start_index, total_rows):             #for i, article in enumerate(rows):
        article = rows[i]

        # ============ Display article info ========================
        display_article_info(i,rows, article, coding_column)


        # ============ TOPIC CHOICE ============
        display_topic_categories()
        
        # Get choice from TOPIC_CATEGORIES and store change
        topic_choice = input("\n[ Enter code (0–7), blank to skip or 'stop' to stop coding ]: ").strip()
        if topic_choice == 'stop':
            print(" - - - - Stoped Coding - - - -")
            return
        elif topic_choice not in TOPIC_CATEGORIES:
            print("Skipped article coding\n")
            continue
            
        topic_label = TOPIC_CATEGORIES[topic_choice]        # For compining with Sentiment label


        # ============ SENTIMENT CHOICE ============
        display_sentiment_categories()

        sentiment_choice = input("\n[ Enter 0,1,2 , blank to skip or 'stop' to stop coding] : ").strip().upper()
        if sentiment_choice == 'STOP':
            print(" - - - - Stoped Coding - - - -")
            return
        elif sentiment_choice not in SENTIMENT_CATEGORIES:
            print("Skipped article coding\n")
            continue
        sentiment_label = SENTIMENT_CATEGORIES[sentiment_choice]


        # ============ Combine TOPIC and SENTIMENT labels to store in same column cell ============
        combined_coding = f"{topic_label},{sentiment_label}"
        article[coding_column] = combined_coding


        # ============ Save coding progress for current row. ============
        with open(CSV_TO_CODE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"\n||||||||   Saved to CSV : {combined_coding}   ||||||||\n")
        print("~~ You can stop and resume anytime. ~~\n")

    print("-" * 70)
    print("\nTypology coding done!")
    


if __name__ == "__main__":
    main()