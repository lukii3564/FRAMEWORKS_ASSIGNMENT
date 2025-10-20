"""
preprocess.py
Load and clean metadata.csv. Save cleaned subset as cleaned_metadata.csv
"""
import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
PREFERRED = os.path.join(DATA_DIR, "metadata.csv")
SAMPLE = os.path.join(DATA_DIR, "sample_metadata.csv")
OUT = os.path.join(DATA_DIR, "cleaned_metadata.csv")

def load_data():
    if os.path.exists(PREFERRED):
        print("Loading metadata.csv")
        df = pd.read_csv(PREFERRED, low_memory=False)
    elif os.path.exists(SAMPLE):
        print("Loading sample_metadata.csv")
        df = pd.read_csv(SAMPLE)
    else:
        raise FileNotFoundError("No metadata found. Run download or generate sample.")
    return df

def basic_cleaning(df):
    # keep common columns safely (not all CORD files have same columns)
    cols = [c for c in ["cord_uid","title","abstract","publish_time","journal","authors","source_x"] if c in df.columns]
    df = df[cols].copy()

    # Trim whitespace
    for c in ["title","abstract","journal","authors","source_x"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().replace({"nan": ""})

    # Convert publish_time to datetime where possible
    if "publish_time" in df.columns:
        df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
        df["pub_year"] = df["publish_time"].dt.year

    # Abstract word count
    if "abstract" in df.columns:
        df["abstract_word_count"] = df["abstract"].fillna("").apply(lambda x: len(str(x).split()))

    # Handle missing journals: fill with 'Unknown'
    if "journal" in df.columns:
        df["journal"] = df["journal"].replace("", "Unknown").fillna("Unknown")

    # Source fallback
    if "source_x" in df.columns:
        df["source_x"] = df["source_x"].replace("", "unknown").fillna("unknown")

    # Drop duplicates (by cord_uid if exists, else by title)
    if "cord_uid" in df.columns:
        df = df.drop_duplicates(subset=["cord_uid"])
    else:
        df = df.drop_duplicates(subset=["title"])

    return df

def save_cleaned(df):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(OUT, index=False)
    print("Saved cleaned data to", OUT)

def main():
    df = load_data()
    print("Initial shape:", df.shape)
    df_clean = basic_cleaning(df)
    print("Cleaned shape:", df_clean.shape)
    save_cleaned(df_clean)

if __name__ == "__main__":
    main()
