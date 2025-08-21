import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("💼 Job Market Trend Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload Job Market CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show original columns
    st.write("📂 Original Columns:", df.columns.tolist())

    # Standardize column names
    rename_map = {
        "Job title": "Job_Title",
        "Job Title": "Job_Title",
        "Job_Titles": "Job_Title",

        "Company": "Company",
        "Company Name": "Company",
        "Company_Names": "Company",

        "salary": "Salary",
        "Salary": "Salary",
        "Package_Details": "Salary",

        "postedDate": "Posted_Date",
        "PostedDate": "Posted_Date",
        "Posted date": "Posted_Date",
        "Posted_Date": "Posted_Date",
        "Post_Time": "Posted_Date",

        "Experience_Required": "Experience",
        "Locations": "Location",
        "Skills": "Skills",
        "Post_Url": "Post_Url"
    }
    df.rename(columns=rename_map, inplace=True)

    st.subheader("📋 Cleaned Dataset Preview")
    st.dataframe(df.head())

    # 🔹 Top 10 Job Titles
    if "Job_Title" in df.columns:
        st.subheader("🏢 Top 10 Job Titles")
        top_jobs = df["Job_Title"].value_counts().head(10)
        st.bar_chart(top_jobs)

    # 🔹 Top 10 Companies Hiring
    if "Company" in df.columns:
        st.subheader("🏬 Top 10 Companies Hiring")
        top_companies = df["Company"].value_counts().head(10)
        st.bar_chart(top_companies)

    # 🔹 Job Locations Distribution
    if "Location" in df.columns:
        st.subheader("📍 Job Locations Distribution")
        top_locations = df["Location"].value_counts().head(10)
        st.bar_chart(top_locations)

    # 🔹 Salary Distribution
    if "Salary" in df.columns:
        st.subheader("💰 Salary Distribution")
        try:
            # Handle non-numeric salaries
            df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
            fig, ax = plt.subplots()
            sns.histplot(df["Salary"].dropna(), bins=20, kde=True, ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"Salary distribution failed: {e}")

    # 🔹 Jobs Posted Over Time
    if "Posted_Date" in df.columns:
        st.subheader("📆 Jobs Posted Over Time")
        try:
            df["Posted_Date"] = pd.to_datetime(df["Posted_Date"], errors="coerce")
            timeline = df["Posted_Date"].value_counts().sort_index()
            st.line_chart(timeline)
        except Exception as e:
            st.warning(f"Date parsing failed: {e}")

    # 🔹 Extra Features (Only Naukri Data)
    if "Experience" in df.columns:
        st.subheader("🎯 Experience Required Distribution")
        st.write(df["Experience"].value_counts().head(10))

    if "Skills" in df.columns:
        st.subheader("🛠 Top Skills in Demand")
        top_skills = df["Skills"].str.split(",").explode().str.strip().value_counts().head(10)
        st.bar_chart(top_skills)
