import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string
import re
import os


ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(ANALYSIS_DIR)
TYPOLOGY_DIR = os.path.join(PROJECT_DIR,"typology_coding") 
OUTPUT_DIR = os.path.join(ANALYSIS_DIR, 'TFIDF_output')

CSV = os.path.join(TYPOLOGY_DIR, "Xi_Jinping_Definitive.csv")

MATRIX_OUTPUT = os.path.join(OUTPUT_DIR,"tfidf_matrix_Xi.csv")
FEATURES_OUTPUT = os.path.join(OUTPUT_DIR,"tfidf_features_Xi.txt")
TOP_10_OUTPUT = os.path.join(OUTPUT_DIR,"Other_tfidf_top10_per_topic.txt")

# List of topic categories
CATEGORIES = [
    "Domestic economic policy",
    "Foreign economic policy",
    "Diplomatic relations",
    "Domestic social policy",
    "Foreign social policy",
    "Military policy",
    "Biographic",
    "Internal politics",
 ]


na_sites = {
    "news.google.com",
    "reuters.com",
    "washingtonpost.com",
    "cnn.com",
    "thestar.com",
    "nationalpost.com",
    "globalnews.ca",
    "theglobeandmail.com",
    "nypost.com",
    "nytimes.com",
    "nbcnews.com",
    "cbc.ca",
    "cbsnews.com",
    "foxnews.com",
    "usatoday.com",
    "salon.com",
    "theatlantic.com",
    "abcnews.go.com",
    "vox.com",
    "cnbc.com",
    "jamestown.org",
    "today.com",
    "chinadigitaltimes.net",
    "breitbart.com"
}

europe_sites ={ 
    "dailymail.co.uk",
    "bbc.co.uk",
    "channel4.com",
    "france24.com",
    "news.sky.com",
    "ft.com",
    "theregister.com",
    "today.rtl.lu" # Rtl.lu is the official website for RTL Luxembourg !
}



# TOP 10 WORDS PER CATEGORY
def top_n_words_per_topic(topic, tfidf_df, n=10):
    row = tfidf_df.loc[topic]
    top_terms = row.sort_values(ascending=False).head(n)
    return top_terms


def clean_text(text):
    if pd.isna(text):
        return ""
    # Basic cleanup: lowercase, remove punctuation
    text = text.lower()
    return text.translate(str.maketrans("", "", string.punctuation))





def main():
    """
    Compute TF-IDF where: 
    Each topic category is treated as a document. 
    Each document = all articles belonging to that category concatenated. 
    TF(t, d) = frequency of term t in category d 
    IDF(t, D) = log(N / df(t)), where N = 8 categories 
    This gives TF-IDF scores for terms that define each category.
    """

    df = pd.read_csv(CSV)
    df = df[['title','source','description', 'Definitive_Topic']].dropna()  # We only need the columns required for TF-IDF

    # TODO: FIlter out North American sources vs Others
    # All unique sources from df
    all_sources = set(df["source"].unique())

    # Split into North American and other sources
    NA_sources = sorted(all_sources.intersection(na_sites))
    other_sources = sorted(all_sources.difference(na_sites))

    # Filter for either only NA or Other sources TODO: change to get both TF-IDF top 10
    df = df[df['source'].isin(other_sources)]
    



    # Combine title + description into one field of text
    df["combined_text"] = (
        df["title"].fillna("") + " " + df["description"].fillna("") #.fillna("") for empty cells
    ).apply(clean_text) 

    # Create one document per category by concatenating text of all articles in it
    category_docs = {}
    for cat in CATEGORIES:
        group_text = " ".join(df[df["Definitive_Topic"] == cat]["combined_text"]) # Get all combined_texts for that Category
        category_docs[cat] = group_text
    docs = [category_docs[c] for c in CATEGORIES]   # Convert dict to ordered list for vectorizer


    custom_stopwords = ['deals','doses','enters','jinping', 'xijinping','chinas','said','week','pm','prime','according','opens','amid','meets','joe','donald']
    all_stopwords = list( ENGLISH_STOP_WORDS.union(custom_stopwords) )

    #phrase_stopwords = ['chinas xi','china xi','trump xi','putin xi','xi calls']   # multi-word phrase to remove]
    merge_phrases = ['greek letter','hong kong', 'white house', 'north korea', 'south korea']


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def custom_preprocessor(text):
        text = text.lower()

        # Merge certain multi-word expressions into single token
        for phrase in merge_phrases:
            pattern = re.escape(phrase.lower())
            merged_token = phrase.replace(" ", "")   # e.g., "hong kong" ---> "hongkong"
            text = re.sub(pattern, merged_token, text, flags=re.IGNORECASE)
        return text
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        sublinear_tf=True,          # applies a logarithmic penalty to term frequency so repeated words matter less
        preprocessor=custom_preprocessor,
        max_features=2600,      # TODO: Adjust around to see  - -  base is 2500
        stop_words=all_stopwords,   # Remove common English words like “the”, “is”, “and”, etc
        #ngram_range=(1, 2)      # unigrams + bigrams((two-word phrases): "xi jinping", "trade war") for features
    )

    tfidf_matrix = vectorizer.fit_transform(docs)


    # Build/Convert to DataFrame
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray(),
        index=CATEGORIES,
        columns=vectorizer.get_feature_names_out()
    )


    
    

    # SAVE OUTPUTS
    with open(TOP_10_OUTPUT, "w") as f:
        
        for topic, row in tfidf_df.iterrows():
            f.write(f"\n====================\n")
            f.write(f" TOP 10 TERMS: {topic}\n")
            f.write(f"====================\n")
            top_10_for_topic = dict(top_n_words_per_topic(topic,tfidf_df, n=10))
            for term, percent  in top_10_for_topic.items(): # get term and percent from Series
                    f.write(f"\t{term}       \t\t\t{percent}\n")
      
            #print(dict(top_n_words_per_topic(topic,tfidf_df, n=10)))

    tfidf_df.to_csv(MATRIX_OUTPUT, index=False)

    with open(FEATURES_OUTPUT, "w") as f:
        for term in vectorizer.get_feature_names_out():
            f.write(term + "\n")

    print("TF-IDF matrix saved to:", MATRIX_OUTPUT)
    print("Feature names saved to:", FEATURES_OUTPUT)



    

if __name__ == "__main__":
    main()