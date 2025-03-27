import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📋 Ecology Project Tracker")

uploaded_file = st.file_uploader("Upload your Permit Tracker (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Assume the file has columns: 'Task', 'Due Date', 'Assigned To'
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['Days Left'] = (df['Due Date'] - datetime.today()).dt.days

    def label_status(days_left):
        if days_left < 0:
            return "🔴 Overdue"
        elif days_left <= 7:
            return "🟠 Due Soon"
        else:
            return "🟢 On Track"

    df['Status'] = df['Days Left'].apply(label_status)

    st.dataframe(df[['Task', 'Due Date', 'Days Left', 'Assigned To', 'Status']])
