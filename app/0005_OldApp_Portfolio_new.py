import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Portfolio Holdings", page_icon="📁", layout="wide")

st.title("Portfolio Holdings")

# Path to the JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "portfolio_holdings.json")

st.markdown("""
Use this page to view the contents of `data/portfolio_holdings.json`.

- **Open Compare view**: it will use the Compare Stock Performance page.
- **Open Market Profile**: it will use the Market Profile page for candlestick + volume profile charts.
""")

# Quick navigation links (open in new tab)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<a href='/?page=Compare Stock performance' target='_blank'><button>Open Compare Stock Performance</button></a>", unsafe_allow_html=True)
with col2:
    st.markdown("<a href='/?page=Market Profile Chart' target='_blank'><button>Open Market Profile Chart</button></a>", unsafe_allow_html=True)

st.write("---")

# Load JSON safely
def load_portfolio_json(path: str):
    if not os.path.exists(path):
        return None, None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    return data, mtime

portfolio_data, modified = load_portfolio_json(DATA_FILE)

if portfolio_data is None:
    st.error(f"Portfolio holdings file not found at {DATA_FILE}")
else:
    st.write(f"**Last modified:** {modified.strftime('%Y-%m-%d %H:%M:%S')}")

    # Show raw JSON
    with st.expander("Raw JSON"):
        st.json(portfolio_data)

    # Try to normalize to DataFrames for portfolio and watchlist
    df_portfolio = None
    df_watchlist = None
    try:
        if isinstance(portfolio_data, list):
            # old format: top-level is a list of holdings
            df_portfolio = pd.json_normalize(portfolio_data)
        elif isinstance(portfolio_data, dict):
            # Handle common keys
            if "portfolio" in portfolio_data:
                df_portfolio = pd.json_normalize(portfolio_data.get("portfolio", []))
            if "watchlist" in portfolio_data:
                df_watchlist = pd.json_normalize(portfolio_data.get("watchlist", []))
            # Fallback: show top-level dict as single-row table
            if df_portfolio is None and df_watchlist is None:
                df_portfolio = pd.DataFrame([portfolio_data])
        else:
            df_portfolio = pd.DataFrame([portfolio_data])
    except Exception as e:
        st.warning("Could not parse JSON into a table: " + str(e))
        df_portfolio = None
        df_watchlist = None

    # Display portfolio holdings
    if df_portfolio is not None and not df_portfolio.empty:
        st.subheader("Portfolio holdings")
        st.dataframe(df_portfolio, width='stretch')

        q = st.text_input("Filter holdings by symbol, notes, or date (substring)", key="holdings_filter")
        if q:
            mask = df_portfolio.apply(lambda row: row.astype(str).str.contains(q, case=False, na=False).any(), axis=1)
            st.dataframe(df_portfolio[mask], width='stretch')

    # Display watchlist if present
    if df_watchlist is not None and not df_watchlist.empty:
        st.subheader("Watchlist")
        st.dataframe(df_watchlist, width='stretch')

        q2 = st.text_input("Filter watchlist by symbol or reason (substring)", key="watchlist_filter")
        if q2:
            mask2 = df_watchlist.apply(lambda row: row.astype(str).str.contains(q2, case=False, na=False).any(), axis=1)
            st.dataframe(df_watchlist[mask2], width='stretch')

    # Build combined tickers list
    combined = []
    seen = set()
    if df_portfolio is not None and 'ticker' in df_portfolio.columns:
        for t in df_portfolio['ticker'].astype(str).tolist():
            if t not in seen:
                combined.append(t)
                seen.add(t)
    if df_watchlist is not None and 'ticker' in df_watchlist.columns:
        for t in df_watchlist['ticker'].astype(str).tolist():
            if t not in seen:
                combined.append(t)
                seen.add(t)

    st.subheader("Quick actions")
    sel = st.multiselect("Select tickers from holdings/watchlist", options=combined)

    import urllib.parse
    tickers_param = urllib.parse.quote(",".join(sel)) if sel else ""

    # Open Compare with selected tickers (opens in new tab)
    if sel:
        st.markdown(f"<a href='/?page=Compare%20Stock%20performance&tickers={tickers_param}' target='_blank'><button>Open Compare with selected</button></a>", unsafe_allow_html=True)
    else:
        st.markdown(f"<button disabled>Open Compare with selected</button>", unsafe_allow_html=True)

    # Market Profile requires a single ticker
    if len(sel) == 1:
        tparam = urllib.parse.quote(sel[0])
        st.markdown(f"<a href='/?page=Market%20Profile%20Chart&ticker={tparam}' target='_blank'><button>Open Market Profile for {sel[0]}</button></a>", unsafe_allow_html=True)
    elif len(sel) > 1:
        st.info("Select a single ticker to open Market Profile (pick one from the multiselect).")
    else:
        st.markdown(f"<button disabled>Open Market Profile</button>", unsafe_allow_html=True)

    # Download button
    st.download_button(label="Download JSON", data=json.dumps(portfolio_data, indent=2), file_name="portfolio_holdings.json", mime="application/json")

    if st.button("Refresh"):
        st.experimental_rerun()

    st.write("---")
    st.info("To compare tickers or view market profiles, use the actions above.")
