import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📅 Ecology Project Gantt Chart Viewer")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load Excel
    xls = pd.ExcelFile(uploaded_file)
    sheet = xls.sheet_names[0]
    df = xls.parse(sheet)

    # Build multi-level columns and clean
    df.columns = [f"{str(col1).strip()}_{str(col2).strip()}" if i > 1 else str(col1).strip()
                  for i, (col1, col2) in enumerate(zip(df.iloc[0], df.iloc[1]))]
    df = df.iloc[2:].copy()
    df = df.rename(columns={df.columns[0]: "Task"})

    # Melt to long format
    df_long = df.melt(id_vars=["Task"], var_name="Month", value_name="Status")
    df_long['Month'] = df_long['Month'].str.extract(r'([A-Za-z]{3})')
    df_long = df_long.dropna(subset=["Status", "Month"])

    # Map months to due dates (assuming Oct 2024–Sep 2025)
    month_map = {
        'Oct': '2024-10-01', 'Nov': '2024-11-01', 'Dec': '2024-12-01',
        'Jan': '2025-01-01', 'Feb': '2025-02-01', 'Mar': '2025-03-01',
        'Apr': '2025-04-01', 'May': '2025-05-01', 'Jun': '2025-06-01',
        'Jul': '2025-07-01', 'Aug': '2025-08-01', 'Sep': '2025-09-01'
    }
    df_long['Due Date'] = pd.to_datetime(df_long['Month'].map(month_map))

    # Assume each task is 1 month long for Gantt
    df_long['End Date'] = df_long['Due Date'] + pd.DateOffset(days=29)

    # Show preview
    st.subheader("📋 Task List")
    st.dataframe(df_long[['Task', 'Month', 'Status', 'Due Date']])

    # Plot Gantt chart
    st.subheader("📊 Gantt Chart")
    fig = px.timeline(df_long, x_start="Due Date", x_end="End Date", y="Task", color="Status", title="Gantt Chart of Field Tasks")
    fig.update_yaxes(autorange="reversed")  # Gantt charts go top-down
    fig.update_layout(height=800)
    st.plotly_chart(fig, use_container_width=True)
