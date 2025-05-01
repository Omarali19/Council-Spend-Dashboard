import pandas as pd

def test_data_loaded():
    df = pd.read_csv("data/2024_DEC_Spend.csv", encoding="ISO-8859-1")
    df.columns = df.columns.str.strip()
    df.rename(columns={
    
        "EFEFCTIVE DATE": "Effective Date",
        "DATE PAID": "Date Paid"
    }, inplace=True)
  
    df["Date Paid"] = pd.to_datetime(df["Date Paid"], errors="coerce")
    df = df.dropna(subset=["Date Paid"])

    assert not df.empty, "DataFrame is empty after loading."
 
    assert "DIRECTORATE" in df.columns, "'DIRECTORATE' column is missing."
    assert "Date Paid" in df.columns, "'Date Paid' column is missing."

   
    assert pd.api.types.is_datetime64_any_dtype(df["Date Paid"]), "'Date Paid' is not datetime."

    assert df["Date Paid"].notna().all(), "'Date Paid' column has missing values."
