import yfinance as yf
import pandas as pd

def analyze_portfolio(df):
    results = []

    for _, row in df.iterrows():
        stock = row['stock']
        qty = row['quantity']
        buy_price = row['buy_price']

        try:
            ticker = yf.Ticker(stock + ".NS")  # NSE ticker
            current_price = ticker.history(period="1d")['Close'].iloc[-1]
        except Exception:
            current_price = 0

        current_value = current_price * qty
        invested_value = buy_price * qty
        profit_loss = current_value - invested_value
        roi = (profit_loss / invested_value) * 100 if invested_value else 0

        results.append({
            "Stock": stock,
            "Qty": qty,
            "Buy Price": buy_price,
            "Current Price": round(current_price, 2),
            "Invested": round(invested_value, 2),
            "Current Value": round(current_value, 2),
            "P&L": round(profit_loss, 2),
            "ROI (%)": round(roi, 2)
        })

    return pd.DataFrame(results).sort_values(by="ROI (%)", ascending=False)
