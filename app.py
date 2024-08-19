import streamlit as st
import requests
import json

# Ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to fetch announcements using HTTP requests
def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        announcements = json_data.get('data', [])
        return announcements
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch announcements for {ticker}: {str(e)}")
        return None

# Fetch all announcements
all_announcements = {ticker: fetch_announcements(ticker) for ticker in tickers}

# Streamlit UI
st.title("ASX Announcements Viewer")

# Dropdown to select ticker
selected_ticker = st.selectbox("Select a Ticker Symbol", tickers)

# Display announcements for the selected ticker
if selected_ticker:
    announcements = all_announcements.get(selected_ticker, [])
    if announcements:
        st.write(f"Recent announcements for {selected_ticker}:")
        for announcement in announcements:
            st.write(announcement['header'])  # Display the announcement header
    else:
        st.write(f"No announcements found for {selected_ticker}")

# Function to check for "Trading Halt"
def has_trading_halt(announcements):
    return any("Trading Halt" in announcement['header'] for announcement in announcements)

# Display tickers with "Trading Halt"
st.write("Tickers with a Trading Halt:")
for ticker, announcements in all_announcements.items():
    if announcements and has_trading_halt(announcements):
        st.write(ticker)
