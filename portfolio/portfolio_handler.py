import pandas as pd

def load_portfolio(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        df.dropna(inplace=True)

        # Check required columns
        required = {"stock", "quantity", "buy_price"}
        if not required.issubset(df.columns):
            raise ValueError("CSV must have: stock, quantity, buy_price")

        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['buy_price'] = pd.to_numeric(df['buy_price'], errors='coerce')
        df.dropna(inplace=True)

        return df
    except Exception as e:
        return f"Error loading portfolio: {e}"
