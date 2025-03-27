import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📋 Ecology Project Tracker")

uploaded_file = st.file_uploader("Upload your Permit Tracker (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convert 'Due Date' to datetime
    df['Due Date'] = pd.to_datetime(df['Due Date'], errors='coerce')

    # Calculate Days Left
    df['Days Left'] = (df['Due Date'] - datetime.today()).dt.days

    # Update Status based on Days Left
    def label_status(days_left):
        if pd.isna(days_left):
            return "⚪ Unknown"
        elif days_left < 0:
            return "🔴 Overdue"
        elif days_left <= 7:
            return "🟠 Due Soon"
        else:
            return "🟢 On Track"

    df['Status'] = df['Days Left'].apply(label_status)

    # Display the updated DataFrame
    st.dataframe(df[['Task', 'Month', 'Status', 'Due Date', 'Days Left']])
