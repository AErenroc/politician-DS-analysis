import os
import argparse
import requests
import json
import time
"""
What this file (fetch_articles.py) does:
    fetch_articles.py) collects a specified number of articles for a given politician using thenewsapi. 
    It tracks articles and pages that have already been fetched using a cache in that politicians folder. 
    This script it built with page caching to try and deal with rate limits of TheNewsAPI Free Tier, and allow 
    for the user to remember pages/articles already fetched to avoid getting the same articles each use. 
    
    NOTE: On the free tier page articles can change, often within days, so the cache can quickly become outdated.

Things to use:
    1 page = first 3 articles (ON THE FREE TEIR of thenewsapi)
    'uuids' are a way of tracking articles
    indent=2 for json for clarity
    TODO: description, snippet, keywords can be used for typology helper code (speed up process later)
"""

THENEWSAPI_URL = "https://api.thenewsapi.com/v1/news/all"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data") # Location of saved articles



def load_cache(cache_file):
    """
    Load cache of saved articles, pages
    """
    # Ensure parent directory exists (politician folder)
    cache_dir = os.path.dirname(cache_file)
    os.makedirs(cache_dir, exist_ok=True)

    if not os.path.exists(cache_file): #CACHE_FILE
        return {"cached_articles": 0,"seen_pages": [], "seen_uuids": []}
    
    with open(cache_file, "r") as f:
        cache = json.load(f)

    # Ensure both keys always exist
    if "cached_articles" not in cache:
        cache["cached_articles"] = 0
    if "seen_pages" not in cache:
        cache["seen_pages"] = []
    if "seen_uuids" not in cache:
        cache["seen_uuids"] = []
    
    return cache


def save_cache(cache, cache_file):
    """
    Save cache to disk (cache.json).
    """
    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=2)



def fetch_articles_with_key(api_key, politician_name, page=1, limit=3):  
    """
    Fetch one page of 'en' articles on given politician using api_key
    """
    params = {
        "api_token": api_key,
        "search": politician_name, # "Xi Jinping"
        "language": "en",
        "page": page,              
        "limit": limit, 
        "locale": "us,ca",  # Restrict to North America 
        "domains": "news.google.com,reuters.com,washingtonpost.com,cnn.com,thestar.com,nationalpost.com,globalnews.ca,theglobeandmail.com,nypost.com,nytimes.com,nbcnews.com,cbc.ca,cbsnews.com,foxnews.com,usatoday.com,salon.com,theatlantic.com,abcnews.go.com,dailymail.co.uk",
        "exclude_domains": "aljazeera.com,china.org.cn,pakistantoday.com.pk,dnaindia.com,ecns.cn,ndtv.com,en.kremlin.ru,timesofindia.indiatimes.com,thejakartapost.com,hindustantimes.com"
    }
    response = requests.get(THENEWSAPI_URL, params=params)
    response.raise_for_status() # Check response was succsessful 
    return response.json()

# "domains": "nypost.com,nytimes.com,nbcnews.com,cbc.ca,cbsnews.com,foxnews.com,salon.com,theatlantic.com"
# "exclude_domains": "tass.com,dnaindia.com,ecns.cn,ndtv.com,en.kremlin.ru,timesofindia.indiatimes.com,india.com"


def save_article(article, politician_dir):
    """ 
    Save a single article to politician_dir folder. 
    """
    filename = os.path.join(DATA_DIR, politician_dir, f"article_{article['uuid']}.json")
    with open(filename, "w") as f:
        json.dump(article, f, indent=2)



def print_cache_data(cache, goal):
    print(f"\n\t\t~~~~~ Article Cache ~~~~~~~~~~~~~~~~~~~~ ")
    print(f"\t\t\tAlready cached pages : {set(cache["seen_pages"])}")
    print(f"\t\t\tAlready cached articles : {len(set(cache["seen_uuids"]))}")
    print(f"\t\t\tGoal: {goal} articles")
    print(" \t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ")




def main():

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("api_key", help="Your TheNewsAPI key, should be a string of letters and numbers")
    parser.add_argument("politician_name", help="Name of the politician to query (proper capitilization required and String)")
    parser.add_argument("num_articles", type=int, help="The number of articles to fetch (will round up to a factor of 3)")
    args = parser.parse_args()
    print(f" \nArguments [api_key]: {args.api_key}\t[politician_name]: {args.politician_name}\t[num_articles]: {args.num_articles} \n")

    # Prep politicians dir and cache in data folder - - 1 cache per politician eg. 'data/Xi Jinping/cache.json
    safe_name = args.politician_name.replace(" ", "_")

    Xipolitician_dir = os.path.join(DATA_DIR, safe_name) #TODO: revert back (remove Xi at front)
    Xicache_file = os.path.join(Xipolitician_dir, "cache.json") #TODO: revert back (remove Xi at front)
    
    politician_dir = os.path.join(DATA_DIR, 'Xi_Jinping_NA_Articles') # TODO: revert.     for savingn NA articles
    cache_file = os.path.join(politician_dir, "cache.json")
    

    # Load and check cache
    cache = load_cache(cache_file)
    Xicache = load_cache(Xicache_file) #TODO: remove line

    seen_uuids = set(cache["seen_uuids"]) # track uuids to avoid saving repeats
    seen_pages = set(cache["seen_pages"]) # track pages to avoid API limits

    Xiseen_uuids = set(Xicache["seen_uuids"]) # TODO: remove line
    Xiseen_pages = set(Xicache["seen_pages"])

    
    print_cache_data(cache, args.num_articles)

    # If we already have enough articles, dont fetch more.
    """
    TODO: uncomment this block
    if len(seen_uuids) >= args.num_articles:
        print(f"You already have enough cached articles (articles seen: {len(seen_uuids)}).")
        return
"""

    print("\n - - - - - -Collecting articles... - - - - - -\n")

    # Go page-by-page, saving all articles in each page. (if num_articles is 7, then it will collect 9 articles )
    page = 1
    total_saved = len(seen_uuids)
    while total_saved < args.num_articles :

        # Skip entire page if it has already fetched (for avoiding API limits)
        if page in seen_pages or page in Xiseen_pages: 
            print(f"Page {page} is cached. Skipping.")
            page += 1
            continue

        print(f"\nFetching page {page}...")

        # Fetch page's articles, using API      (FREE teir, limit=3 articles per page)
        page_data = fetch_articles_with_key(args.api_key, args.politician_name, page=page)
        articles = page_data.get("data", [])
        if not articles:
            print(f" \n\t > > > COULD NOT FIND ARTICLES FOR page: {page} < < <\n")
            break

        # Save all article UUIDs in page.
        for article in articles:
            uuid = article["uuid"]

            # Skip if already saved
            if uuid in Xiseen_uuids or uuid in seen_uuids: 
                print(f"\n\t\t uuid: {uuid} already seen, skipping...\n")
                continue
            # Save if new uuid
            save_article(article, politician_dir)   # Saves article to politician's folder
            cache["seen_uuids"].append(uuid)        # Prep cache to store new uuid.  
            total_saved += 1                        # Track how many uuids are saved 
            seen_uuids.add(uuid)                    # For tracking uuids (faster then opening cache each time)

        
        cache["seen_pages"].append(page)        # Prep cache to store page.  
        cache["cached_articles"] = total_saved  # Store how many uuids saved
        save_cache(cache, cache_file)           # Save updated cache (new uuids and page) to disk

        # Go to next page of articles, with a polite delay for the API
        page += 1                   
        time.sleep(1)


if __name__ == "__main__":
    main()