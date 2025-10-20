# FRAMEWORKS_ASSIGNMENT — CORD-19 Basic Analysis & Streamlit App

## Overview
This repository implements a beginner-friendly analysis of the CORD-19 `metadata.csv` and a simple Streamlit app to display results.

## Contents
- `src/generate_sample.py` — generates a small `data/sample_metadata.csv` for testing.
- `src/download_metadata.py` — download only the metadata.csv via Kaggle API (optional).
- `src/preprocess.py` — cleaning and derive columns (pub_year, abstract_word_count).
- `src/analysis.py` — helper analysis functions.
- `app/streamlit_app.py` — Streamlit application.
- `requirements.txt` — Python dependencies.

## Quick start (no big download)
1. Create virtual env (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # linux/mac
   venv\Scripts\activate     # windows
   pip install -r requirements.txt


2. Generate sample data (for development):
python src/generate_sample.py
python src/preprocess.py


3. Run Streamlit:
streamlit run app/streamlit_app.py
