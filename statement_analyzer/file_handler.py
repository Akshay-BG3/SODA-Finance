import pandas as pd

def load_csv(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        return f"Error loading file: {e}"

def clean_dataframe(df):
    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    # Remove completely empty rows
    df.dropna(how='all', inplace=True)
    # Fill missing cells with blank
    df.fillna('', inplace=True)
    return df
