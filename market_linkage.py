import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

def run_market_linkage():
    # ------------------ CONFIG ------------------
    st.set_page_config(page_title="Market Linkage & Price Forecasting", page_icon="📈", layout="wide")
    st.title("📈 Market Linkage & Price Forecasting")
    st.markdown("Get mandi prices, forecasts, and alerts for buyers and contract farming opportunities.")

    # ------------------ SAMPLE DATA ------------------
    # Simulate mandi price data for demonstration
    crops = ["Wheat", "Rice", "Maize", "Tomato", "Potato"]
    base_prices = {"Wheat": 2100, "Rice": 3200, "Maize": 1800, "Tomato": 2500, "Potato": 1200}

    def generate_price_data(crop, days=14):
        today = date.today()
        data = []
        for i in range(days):
            day = today - timedelta(days=days - i)
            price = base_prices[crop] + (i * 10)  # simple trend
            data.append({"Date": day, "Price": price})
        return pd.DataFrame(data)

    # ------------------ USER INPUT ------------------
    crop_choice = st.selectbox("🌾 Select your crop:", crops)
    days_to_show = st.slider("Select days for price history & forecast:", 7, 30, 14)

    df_prices = generate_price_data(crop_choice, days=days_to_show)

    # ------------------ PRICE FORECAST ------------------
    # Simple forecast: next 7 days with same trend
    last_price = df_prices["Price"].iloc[-1]
    daily_change = df_prices["Price"].diff().mean()
    forecast = []
    for i in range(1, 8):
        forecast_date = df_prices["Date"].iloc[-1] + timedelta(days=i)
        forecast_price = last_price + daily_change * i
        forecast.append({"Date": forecast_date, "Forecast Price": round(forecast_price, 2)})
    df_forecast = pd.DataFrame(forecast)

    # ------------------ DISPLAY PRICE HISTORY ------------------
    st.subheader("💰 Mandi Prices (Past Days)")
    st.table(df_prices)

    st.subheader("📊 Price Trend & Forecast")
    df_plot = pd.DataFrame({
        "Date": list(df_prices["Date"]) + list(df_forecast["Date"]),
        "Price": list(df_prices["Price"]) + list(df_forecast["Forecast Price"]),
        "Type": ["Actual"]*len(df_prices) + ["Forecast"]*len(df_forecast)
    })
    fig = px.line(df_plot, x="Date", y="Price", color="Type", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # ------------------ ALERTS / OPPORTUNITIES ------------------
    st.subheader("📣 Nearby Buyers & Contract Farming Opportunities")
    st.markdown("""
    - **Local Cooperatives:** ABC Farmer Coop (5 km away)  
    - **Buyers:** XYZ Agro Traders (3 km away), LMN Fresh Markets (8 km away)  
    - **Contract Farming Offers:** Available for Wheat and Tomato in your region this season.  
    """)

    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#666;'>💡 Tip: Regularly check prices and forecast trends to plan your harvest and sales.</div>", unsafe_allow_html=True)
