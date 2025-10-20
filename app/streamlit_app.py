"""
streamlit_app.py
Run: streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from src.analysis import count_by_year, top_journals, source_distribution, title_word_freq
import os

DATA_CLEAN = os.path.join("data", "cleaned_metadata.csv")
SAMPLE = os.path.join("data", "sample_metadata.csv")

st.set_page_config(page_title="CORD-19 Basic Analysis", layout="wide")

@st.cache_data
def load_data():
    if os.path.exists(DATA_CLEAN):
        df = pd.read_csv(DATA_CLEAN, parse_dates=["publish_time"], low_memory=False)
    elif os.path.exists(SAMPLE):
        df = pd.read_csv(SAMPLE, parse_dates=["publish_time"], low_memory=False)
    else:
        st.error("No data found. Run generate_sample.py or download metadata.csv.")
        return pd.DataFrame()
    return df

df = load_data()

st.title("CORD-19 — Basic Metadata Analysis")
st.markdown("""
This app is a minimal example for the Frameworks assignment.
You can use a small sample dataset (`data/sample_metadata.csv`) or a real `metadata.csv` downloaded.
""")

if df.empty:
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
years = sorted([int(y) for y in df["publish_time"].dt.year.dropna().unique()]) if "publish_time" in df.columns else []
selected_year = st.sidebar.selectbox("Publication year", options=["All"] + (years if years else []))
selected_source = st.sidebar.selectbox("Source", options=["All"] + list(df["source_x"].fillna("unknown").unique()))

# apply filters
df_filtered = df.copy()
if selected_year != "All":
    df_filtered = df_filtered[df_filtered["publish_time"].dt.year == int(selected_year)]
if selected_source != "All":
    df_filtered = df_filtered[df_filtered["source_x"] == selected_source]

st.subheader("Key numbers")
col1, col2, col3 = st.columns(3)
col1.metric("Total papers (filtered)", int(len(df_filtered)))
col2.metric("Unique journals", int(df_filtered["journal"].nunique()))
col3.metric("Avg abstract words", round(df_filtered["abstract"].astype(str).apply(lambda x: len(str(x).split())).mean(), 1))

# Plot: publications over time
st.subheader("Publications over time")
year_counts = df["publish_time"].dt.year.value_counts().sort_index() if "publish_time" in df.columns else pd.Series()
fig1, ax1 = plt.subplots(figsize=(8,3))
if not year_counts.empty:
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o", ax=ax1)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Papers")
else:
    ax1.text(0.5,0.5,"No publish_time column available", ha='center')
st.pyplot(fig1)

# Top journals
st.subheader("Top journals")
tj = df["journal"].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(8,3))
sns.barplot(x=tj.values, y=tj.index, ax=ax2)
ax2.set_xlabel("Number of papers")
st.pyplot(fig2)

# Title word cloud / frequency
st.subheader("Title word cloud (top words)")

# Prepare tokens
from collections import Counter
import re
titles = df_filtered["title"].fillna("").astype(str).str.lower()
words = []
stopwords = set(["the","and","of","in","a","to","for","on","with","covid","covid-19","sars-cov-2","cov-2"])
for t in titles:
    words += [w for w in re.findall(r"[a-zA-Z']+", t) if w not in stopwords and len(w)>2]
freq = Counter(words)
if freq:
    wc = WordCloud(width=800, height=300, background_color="white").generate_from_frequencies(freq)
    fig3, ax3 = plt.subplots(figsize=(12,3))
    ax3.imshow(wc, interpolation="bilinear")
    ax3.axis("off")
    st.pyplot(fig3)
else:
    st.write("No title words to show.")

# Show sample of data
st.subheader("Sample data")
st.dataframe(df_filtered.head(20))
