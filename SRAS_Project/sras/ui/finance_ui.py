
import streamlit as st
import yfinance as yf
import pandas as pd
import finnhub
from sras.utils.response_formatter import show_synthesis_progress, format_response

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key="d10vvmpr01qse6lee2j0d10vvmpr01qse6lee2jg")

def fetch_news_sentiment(ticker):
    try:
        sentiment = finnhub_client.news_sentiment(ticker)
        return sentiment
    except Exception as e:
        return {"error": f"Error fetching news sentiment: {e}"}

def finance_ui():
    st.subheader("📊 Finance Agent")

    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):").upper()
    option = st.selectbox("Select Option:", ["Current Price", "Historical Data", "Financial Summary", "News Sentiment"])

    if st.button("Submit"):
        if not ticker:
            st.warning("Please enter a valid ticker symbol.")
            return

        show_synthesis_progress()

        result = None
        try:
            stock = yf.Ticker(ticker)

            if option == "Current Price":
                price = stock.info.get("regularMarketPrice", "N/A")
                result = f"Current Price of {ticker}: ${price}"

            elif option == "Historical Data":
                hist = stock.history(period="1mo")
                result = hist[["Close"]]

            elif option == "Financial Summary":
                info = stock.info
                result = info

            elif option == "News Sentiment":
                result = fetch_news_sentiment(ticker)

        except Exception as e:
            result = {"error": str(e)}

        format_response("finance", result)
