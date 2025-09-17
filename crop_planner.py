import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from datetime import timedelta, date

def run_crop_planner():

    # ------------------ CONFIG ------------------
    st.set_page_config(page_title="Crop Planner", page_icon="📅", layout="wide")
    st.title("📅 Crop Planning Calendar")
    st.markdown("Plan your crop activities with a clear timeline and calendar view.")

    # ------------------ SAMPLE CROP PLANS ------------------
    crop_plans = {
        "Wheat": [
            ("Sowing", 0),
            ("First Irrigation", 20),
            ("Fertilizer (Urea)", 30),
            ("Second Irrigation", 40),
            ("Weeding", 50),
            ("Pesticide Spray", 70),
            ("Harvesting", 120),
        ],
        "Rice": [
            ("Nursery Preparation", 0),
            ("Transplanting", 20),
            ("First Fertilizer Dose", 30),
            ("Irrigation", 40),
            ("Weeding", 60),
            ("Second Fertilizer Dose", 70),
            ("Harvesting", 150),
        ],
        "Maize": [
            ("Sowing", 0),
            ("First Irrigation", 15),
            ("Fertilizer (DAP)", 20),
            ("Second Irrigation", 30),
            ("Pesticide Spray", 45),
            ("Harvesting", 100),
        ]
    }

    # ------------------ USER INPUT ------------------
    crop_choice = st.selectbox("🌱 Select your crop:", list(crop_plans.keys()))
    start_date = st.date_input("📅 Select sowing date:", date.today())

    # ------------------ BUILD SCHEDULE ------------------
    plan = crop_plans[crop_choice]
    schedule = []
    for activity, offset in plan:
        activity_date = start_date + timedelta(days=offset)
        schedule.append({"Task": activity, "Date": activity_date})

    df = pd.DataFrame(schedule)

    # ------------------ DISPLAY ------------------
    st.subheader("🗒️ Crop Activity Schedule")
    st.table(df)

    # ------------------ TIMELINE VIEW ------------------
    st.subheader("📊 Timeline View")
    df_timeline = pd.DataFrame({
        "Task": df["Task"],
        "Start": df["Date"],
        "Finish": df["Date"] + timedelta(days=1)  # one-day events
    })

    fig = px.timeline(df_timeline, x_start="Start", x_end="Finish", y="Task", color="Task")
    fig.update_yaxes(autorange="reversed")  # tasks top-down
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#666;'>🌾 Plan efficiently for better yields!</div>", unsafe_allow_html=True)
