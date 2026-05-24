# politician-DS-analysis
Understand how a chosen political figure is being covered in the media.

Politician: `Xi Jinping`

## analysis/
Contains code to plot and explore data, as well as TF-IDF analysis results.
- `TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical method used in natural language processing to evaluate how important a word is to a document within a larger collection`

## data/
Contains the articles retrieved using **theNewsAPI** , as well as a cache for tracking article IDs.

##  images/
Contains the generated graphs and plots for the Finalreport.tex to reference.

##  scripts/
| Script | Functionality |
| -------- | -------- |
| `fetch_articles.py` | Collects a specified number of articles for a given politician using **theNewsAPI**. It tracks articles and pages that have already been fetched using a cache in that politicians folder (ex. data/[politician-name]). This script it built with page caching to try and deal with rate limits of **theNewsAPI** free tier, and allow for the user to remember pages/articles that have already been fetched to avoid repeated page fetching.| 
| `articles_to_csv.py` | Collects all the articles in a politician folder (ex. data/[politician-name]) and then converts them to a CSV where, rows --> articles. The CSV contains the columns "uuid","title","description","snippet","url","source", "language","published_at" as well as three new empty columns for manual coding, more can be added by modifying this `.py` and `typology_coding_helper.py`. | 
| `typology_coding_helper.py` | Loads article data from a CSV file and allows a user to assign both a topic category *(such as domestic policy, foreign relations, etc)* and a sentiment label *(positive, neutral, or negative)* to each article. The program displays article details including the **title, description, snippet, and URL** then prompts the user to enter classification codes. The selected labels are combined and saved into a chosen coding column within the CSV file. The tool supports resuming from a specific row, skipping articles, and saving progress continuously so coding can be paused and resumed at any time. | 


##  typology_coding/
Contains the directories `toCode` (uncoded articles) and `Coded`(the coded article / output from running typology_coding_helper.py)

##  typology categories/
| NumberRep | Category |
| -------- | -------- |
| `0` | `Domestic economic policy`| 
| `1` | `Foreign economic policy`| 
| `2` | `Diplomatic relations`| 
| `3` | `Domestic social policy`| 
| `4` | `Foreign social policy`| 
| `5` | `Military policy`| 
| `6` | `Biographic`| 
| `7` | `Internal politics`| 
- *Refer to typology_instruction.pdf for category definitions and how to deal with edge case scenarios*
