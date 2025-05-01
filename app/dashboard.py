import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Council Spend Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/2024_DEC_Spend.csv", encoding="ISO-8859-1")
    df.columns = df.columns.str.strip()  # Clean column names
    df.rename(columns={
        "AMOUNT (£)": "Amount",
        "EFEFCTIVE DATE": "Effective Date",
        "DATE PAID": "Date Paid"
    }, inplace=True)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")  
    df["Date Paid"] = pd.to_datetime(df["Date Paid"], errors="coerce")  
    return df.dropna(subset=["Amount", "Date Paid"])  

df = load_data()

st.title("📊 Council Spending Dashboard - December 2024")
st.markdown("Use the filters below to explore spending data by directorate, supplier, and purpose.")

st.sidebar.header("🔎 Filters")

directorates = df["DIRECTORATE"].dropna().unique()
selected_directorates = st.sidebar.multiselect("Select Directorate(s):", directorates, default=directorates)

suppliers = df["SUPPLIER NAME"].dropna().unique()
selected_suppliers = st.sidebar.multiselect("Select Supplier(s):", suppliers, default=suppliers[:10])

min_date = df["Date Paid"].min()
max_date = df["Date Paid"].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])


filtered_df = df[
    (df["DIRECTORATE"].isin(selected_directorates)) &
    (df["SUPPLIER NAME"].isin(selected_suppliers)) &
    (df["Date Paid"] >= pd.Timestamp(start_date)) &
    (df["Date Paid"] <= pd.Timestamp(end_date))
]

with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(filtered_df)


st.subheader("💷 Total Spend by Directorate")
spend_by_directorate = (
    filtered_df.groupby("DIRECTORATE")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=spend_by_directorate.values, y=spend_by_directorate.index, palette="viridis", ax=ax1)
ax1.set_xlabel("Total Spend (£)")
ax1.set_title("Spend by Directorate")
st.pyplot(fig1)

if "PURPOSE" in filtered_df.columns:
    st.subheader("📌 Spend by Purpose")
    top_purposes = (
        filtered_df.groupby("PURPOSE")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_purposes.values, y=top_purposes.index, palette="magma", ax=ax2)
    ax2.set_xlabel("Total Spend (£)")
    ax2.set_title("Top 10 Spending Purposes")
    st.pyplot(fig2)

csv = filtered_df.to_csv(index=False)
st.download_button("📥 Download Filtered Data", csv, "filtered_spending_data.csv", "text/csv")

st.markdown("---")
st.markdown("✅ Dashboard created with Streamlit | Data: Council Spending December 2024")
