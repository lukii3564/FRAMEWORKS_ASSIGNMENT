"""
analysis.py
Functions to produce common analysis outputs (counts, top journals, word frequencies).
"""
import pandas as pd
import re
from collections import Counter

def load_cleaned(path="data/cleaned_metadata.csv"):
    return pd.read_csv(path, parse_dates=["publish_time"], low_memory=False)

def count_by_year(df):
    if "pub_year" in df.columns:
        return df["pub_year"].value_counts().sort_index()
    else:
        return pd.Series(dtype=int)

def top_journals(df, n=10):
    return df["journal"].value_counts().head(n)

def source_distribution(df):
    return df["source_x"].value_counts()

def title_word_freq(df, n=30):
    # Simple tokenization and stopword removal
    stopwords = set([
        "the","and","of","in","a","to","for","on","with","covid","covid-19","sars-cov-2","cov-2"
    ])
    titles = df["title"].fillna("").astype(str).str.lower()
    tokens = []
    for t in titles:
        words = re.findall(r"[a-zA-Z']+", t)
        for w in words:
            if w in stopwords or len(w) <= 2:
                continue
            tokens.append(w)
    c = Counter(tokens)
    return c.most_common(n)

if __name__ == "__main__":
    df = load_cleaned()
    print("Publications by year:\n", count_by_year(df))
    print("Top journals:\n", top_journals(df))
    print("Top title words:\n", title_word_freq(df, 20))
