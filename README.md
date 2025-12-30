# Python_2026_mk1

Repository for the Stock Portfolio Tracking & Analysis App.

Contents overview (copied from data/README.md):

Python_2026_mk1/
├── streamlit_app.py          # Main Streamlit entry point
├── pyproject.toml            # Project configuration (uv compatible)
├── README.md                 # This file
├── .gitignore                # Git ignore rules
├── app/
│   ├── 0001_Home_*.py       # Home page
│   ├── 0002_Learning_*.py   # Learning resources
│   ├── 0003_Resume_*.py     # Resume/CV
│   ├── 0004_Stock_*.py      # Stock analysis
│   └── 0004_Portfolio_Mk1.py # Portfolio tracker (NEW)
├── data/
│   └── portfolio.json        # Portfolio data storage
└── assets/
    └── *.json                # Lottie animations

## Description

This project contains Streamlit pages and helper modules for tracking and analyzing stock portfolios.

## Quick fix

Added this top-level `README.md` because the build backend expects it (see `pyproject.toml: readme = "README.md").
