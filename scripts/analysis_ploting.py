import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

import numpy as np


TYPOLOGY_DIR = " set " # TODO: remove zedbed hardcoding the dir
CSV_TO_CODE = os.path.join(TYPOLOGY_DIR, 'UPDATED_Xi_Jinping_Merged_data.csv') #"Xi_jinping_articles_for_coding.csv") 

NEW_CSV_TO_CODE = os.path.join(TYPOLOGY_DIR, 'Xi_Jinping_split.csv') 
DEFINITIVE_CSV_TO_CODE = os.path.join(TYPOLOGY_DIR, 'Xi_Jinping_Definitive.csv') 


def split_features_columns():
    df = pd.read_csv(CSV_TO_CODE)

    #E_codings	S_codings	Z_codings


    df["E_topic_coding"] = df["E_codings"].str.split(",").str[0]
    df["E_favorability_coding"] = df["E_codings"].str.split(",").str[1]

    df["S_topic_coding"] = df["S_codings"].str.split(",").str[0]
    df["S_favorability_coding"] = df["S_codings"].str.split(",").str[1]

    df["Z_topic_coding"] = df["Z_codings"].str.split(",").str[0]
    df["Z_favorability_coding"] = df["Z_codings"].str.split(",").str[1]

    print(df)

    df.to_csv(NEW_CSV_TO_CODE)

def row_mode_or_none(row):
    vals = row.dropna().tolist()
    # Pandas mode returns all modes; if unique, it will list multiple values
    m = pd.Series(vals).mode()
    # If there is exactly one mode and it appears at least twice → keep it
    if len(m) == 1 and vals.count(m.iloc[0]) >= 2:
        return m.iloc[0]
    return None




def definitive_coding():
    df = pd.read_csv(NEW_CSV_TO_CODE)

    df["Definitive_Topic"] = df[["E_topic_coding", "S_topic_coding", "Z_topic_coding"]].apply(row_mode_or_none, axis=1)
    df["Definitive_Fav"] = df[["E_favorability_coding", "S_favorability_coding", "Z_favorability_coding"]].apply(row_mode_or_none, axis=1)

    df.to_csv(DEFINITIVE_CSV_TO_CODE)



def make_table():
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)
    print(len(df)) # -> 502

    print(len(df[df["Definitive_Fav"] == "Positive"]))
    print(len(df[df["Definitive_Fav"] == "Negative"]))
    print(len(df[df["Definitive_Fav"] == "Neutral"]))



def make_pie_chart_favorability():
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    counts = df["Definitive_Topic"].value_counts().reindex(
        ["Positive", "Negative", "Neutral"], fill_value=0
    )

    labels = counts.index
    sizes = counts.values
    colors = ["green", "red", "gray"]

    plt.figure(figsize=(6,6))
    plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.8
    )
    plt.title("Favourability distribution of Articles Mentionning Xi Jinping")
    plt.axis("equal")  # ensures pie is drawn as a circle
    plt.show()



def make_pie_chart_topics():
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    print(df["Definitive_Topic"].unique())

    #exit()

    counts = df["Definitive_Topic"].value_counts().reindex(
        ["Diplomatic relations",
        "Domestic social policy",
        "Domestic economic policy",
        "Foreign social policy",
        "Foreign economic policy",
        "Biographic",
        "Military policy",
        "Internal politics"], fill_value=0
    )

    labels = counts.index
    sizes = counts.values
    #colors = ["green", "red", "gray"]

    plt.figure(figsize=(12,12))
    plt.pie(
        sizes,
        labels=labels,
        #colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=1
    )
    plt.title("Topic distribution of Articles Mentionning Xi Jinping")
    plt.axis("equal")  # ensures pie is drawn as a circle
    plt.show()



def plot_percent_table_colored():
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    # Count positive and negative per topic
    table = df.pivot_table(
        index="Definitive_Topic",
        columns="Definitive_Fav",
        aggfunc="size",
        fill_value=0
    ).reindex(columns=["Positive", "Neutral","Negative"], fill_value=0)

    # Convert to percentages
    table_percent = table.div(table.sum(axis=1), axis=0) * 100
    table_percent = table_percent.round(1)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, len(table_percent)*1 + 1))
    ax.axis('tight')
    ax.axis('off')

    # Create table in matplotlib
    tbl = ax.table(
        cellText=table_percent.reset_index().values,
        colLabels=table_percent.reset_index().columns,
        cellLoc='center',
        loc='center'
    )

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.5)

    # Apply a single color gradient (e.g., Blues)
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = plt.cm.Blues  # change to any colormap you like

    n_rows, n_cols = table_percent.shape
    for i in range(n_rows):
        for j in range(n_cols):
            val = table_percent.iloc[i, j]
            color = cmap(norm(val))
            tbl[(i+1, j+1)].set_facecolor(color)  # +1 because row=0 is header, col=0 is topic

    plt.title("Favourability of Articles per Topic", fontsize=14)
    plt.show()




def plot_topic_favorability():
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    # Count positive and negative per topic
    table = df.pivot_table(
        index="Definitive_Topic",
        columns="Definitive_Fav",
        aggfunc="size",
        fill_value=0
    ).reindex(columns=["Positive", "Negative", "Neutral"], fill_value=0)

    topics = table.index.tolist()
    positive_counts = table["Positive"].values
    negative_counts = table["Negative"].values
    neutral_counts = table["Neutral"].values

    x = np.arange(len(topics))  # positions for the groups
    width = 0.2  # width of the bars

    plt.figure(figsize=(10,6))
    plt.bar(x - width, positive_counts, width, label='Positive', color='green')
    plt.bar(x, neutral_counts, width, label='Neutral', color='grey')
    plt.bar(x +width, negative_counts, width, label='Negative', color='red')

    plt.xlabel('Topics')
    plt.ylabel('Number of Articles')
    plt.title('Favourability of Articles per Topic')
    plt.xticks(x, topics, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()



def plot_Source_percent_table_colored():
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors

    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)


    source_counts = df['source'].value_counts()
    sources_to_keep = source_counts[source_counts > 5].index
    df = df[df['source'].isin(sources_to_keep)]


    # Count positive and negative per source
    table = df.pivot_table(
        index="source",
        columns="Definitive_Fav",
        aggfunc="size",
        fill_value=0
    ).reindex(columns=["Positive", "Neutral","Negative" ], fill_value=0)

    # Convert to percentages
    table_percent = table.div(table.sum(axis=1), axis=0) * 100
    table_percent = table_percent.round(1)

    n_rows, n_cols = table_percent.shape

    # Dynamic figure sizing
    row_height = 1  # increase for more vertical spacing
    col_width = 5   # increase for longer source names
    fig_width = n_cols * col_width 
    fig_height = n_rows * row_height  # extra for title

    fig, ax = plt.subplots(figsize=(20, 6))

    ax.axis('tight')
    ax.axis('off')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    # Create table
    tbl = ax.table(
        cellText=table_percent.reset_index().values,
        colLabels=table_percent.reset_index().columns,
        cellLoc='center',
        loc='center'
    )

    # Adjust font size and cell scaling for readability
    font_size = 12
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(font_size)
    tbl.scale(1, row_height)  # wider columns and taller rows

    # Apply single color gradient
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = plt.cm.Blues

    for i in range(n_rows):
        for j in range(n_cols):
            val = table_percent.iloc[i, j]
            color = cmap(norm(val))
            tbl[(i+1, j+1)].set_facecolor(color)

    plt.title("Favourability of Articles per Source", fontsize=16, pad=20)
    plt.show()



def plot_monthly_sentiment_trends():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["published_at"], errors="coerce")
    df = df.dropna(subset=["date"])   # remove invalid dates

    # Extract year-month
    df["year_month"] = df["date"].dt.to_period("M")

    # Pivot: counts per sentiment per month
    monthly_counts = df.pivot_table(
        index="year_month",
        columns="Definitive_Fav",
        aggfunc="size",
        fill_value=0
    ).reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)

    # Convert counts → percentages per month
    monthly_percent = monthly_counts.div(monthly_counts.sum(axis=1), axis=0) * 100

    # Convert PeriodIndex → Timestamp for plotting
    monthly_percent.index = monthly_percent.index.to_timestamp()

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_percent.index, monthly_percent["Positive"], label="Positive", color="green", linewidth=2)
    plt.plot(monthly_percent.index, monthly_percent["Neutral"],  label="Neutral",  color="gray",  linewidth=2)
    plt.plot(monthly_percent.index, monthly_percent["Negative"], label="Negative", color="red",   linewidth=2)

    plt.title("Month-over-Month Sentiment Distribution (%)", fontsize=16)
    plt.ylabel("Percentage (%)")
    plt.xlabel("Month")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()



def plot_yearly_sentiment_trends():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["published_at"], errors="coerce")
    df = df.dropna(subset=["date"])   # remove invalid dates

    # Extract year-month
    df["year"] = df["date"].dt.to_period("Y")

    # Pivot: counts per sentiment per month
    monthly_counts = df.pivot_table(
        index="year",
        columns="Definitive_Fav",
        aggfunc="size",
        fill_value=0
    ).reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)

    # Convert counts → percentages per month
    monthly_percent = monthly_counts.div(monthly_counts.sum(axis=1), axis=0) * 100

    # Convert PeriodIndex → Timestamp for plotting
    monthly_percent.index = monthly_percent.index.to_timestamp()

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_percent.index, monthly_percent["Positive"], label="Positive", color="green", linewidth=2)
    plt.plot(monthly_percent.index, monthly_percent["Neutral"],  label="Neutral",  color="gray",  linewidth=2)
    plt.plot(monthly_percent.index, monthly_percent["Negative"], label="Negative", color="red",   linewidth=2)

    plt.title("Month-over-Month Sentiment Distribution (%)", fontsize=16)
    plt.ylabel("Percentage (%)")
    plt.xlabel("Year")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()



def plot_monthly_sentiment_trends_MA(window=6):
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    df = df[~df["source"].isin(na_sites)]

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["published_at"], errors="coerce")
    df = df.dropna(subset=["date"])   # remove invalid dates

    # Extract year-month
    df["year_month"] = df["date"].dt.to_period("M")

    # Pivot: counts per sentiment per month
    monthly_counts = df.pivot_table(
        index="year_month",
        columns="Definitive_Fav",
        aggfunc="size",
        fill_value=0
    ).reindex(columns=["Positive", "Neutral", "Negative"], fill_value=0)

    # Convert counts → percentages per month
    monthly_percent = monthly_counts.div(monthly_counts.sum(axis=1), axis=0) * 100

    # Convert PeriodIndex → Timestamp for plotting
    monthly_percent.index = monthly_percent.index.to_timestamp()

    # ---- Apply Moving Average ----
    monthly_smoothed = monthly_percent.rolling(window=window, min_periods=1).mean()

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_smoothed.index, monthly_smoothed["Positive"], label=f"Positive (MA {window})", color="green", linewidth=2)
    plt.plot(monthly_smoothed.index, monthly_smoothed["Neutral"],  label=f"Neutral (MA {window})",  color="gray", linewidth=2)
    plt.plot(monthly_smoothed.index, monthly_smoothed["Negative"], label=f"Negative (MA {window})", color="red",   linewidth=2)

    plt.title(f"Month-over-Month Sentiment Distribution : {window} Month Moving Average : non-North American sources", fontsize=16)
    plt.ylabel("Percentage (%)")
    plt.xlabel("Month")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()



def plot_yearly_articles_per_source():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)

    # Filter: keep sources with more than 5 articles
    source_counts = df['source'].value_counts()
    sources_to_keep = source_counts[source_counts > 5].index
    df = df[df['source'].isin(sources_to_keep)]

    # Ensure published_at is datetime
    df["date"] = pd.to_datetime(df["published_at"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Extract year
    df["year"] = df["date"].dt.year

    # Count articles per source per year
    yearly_counts = df.groupby(["year", "source"]).size().unstack(fill_value=0)

    # Plot
    plt.figure(figsize=(14, 7))

    yearly_counts.plot(kind="bar", figsize=(14, 7))

    plt.title("Yearly Number of Articles by Source", fontsize=16)
    plt.xlabel("Year")
    plt.ylabel("Number of Articles")
    plt.legend(title="Source", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.grid(axis="y", alpha=0.3)

    plt.show()

na_sites = {
    "news.google.com",
    "chinadigitaltimes.net",
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
    "thegatewaypundit.com",
    "realclearmarkets.com"
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


def make_pie_chart_topics_NA():
    df = pd.read_csv(DEFINITIVE_CSV_TO_CODE)
    df = df[~df["source"].isin(na_sites)]
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)


    print(df["source"])

    #exit()

    counts = df["Definitive_Topic"].value_counts().reindex(
        ["Diplomatic relations",
        "Domestic social policy",
        "Domestic economic policy",
        "Foreign social policy",
        "Foreign economic policy",
        "Biographic",
        "Military policy",
        "Internal politics"], fill_value=0
    )

    labels = counts.index
    sizes = counts.values
    #colors = ["green", "red", "gray"]

    plt.figure(figsize=(12,12))
    plt.pie(
        sizes,
        labels=labels,
        #colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=1
    )
    plt.title("Topic distribution of Articles Mentionning Xi Jinping: non-North American sources")
    plt.axis("equal")  # ensures pie is drawn as a circle
    plt.show()



if __name__ == "__main__":
    #split_features_columns()
    #definitive_coding()
    #make_pie_chart_favorability()
    #make_pie_chart_topics()
    #plot_topic_favorability()
    #plot_percent_table_colored()
    #plot_Source_percent_table_colored()
    #plot_topic_favorability()
    #plot_percent_table_colored()
    #plot_yearly_sentiment_trends()
    #plot_monthly_sentiment_trends_MA()
    #plot_yearly_articles_per_source()
    #make_pie_chart_topics_NA()
    plot_monthly_sentiment_trends_MA()