from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_outliers(df):
    if df.empty or 'amount' not in df.columns:
        return pd.DataFrame(), []

    # Filter only expenses
    expenses = df[df['type'] == 'expense'].copy()
    if expenses.empty:
        return pd.DataFrame(), []

    # Use only the 'amount' column for anomaly detection
    X = expenses[['amount']].copy()
    X['amount'] = X['amount'].abs()  # use absolute value for ML

    # Fit IsolationForest
    model = IsolationForest(contamination=0.1, random_state=42)
    expenses['anomaly'] = model.fit_predict(X)

    # -1 means anomaly
    outliers = expenses[expenses['anomaly'] == -1]
    alerts = []

    for _, row in outliers.iterrows():
        alerts.append(
            f"⚠️ Unusual expense detected: ₹{abs(row['amount']):,.0f} in '{row['category']}' ({row['description']})"
        )

    return outliers, alerts

def detect_spending_spikes(df):
    if df.empty:
        return []

    df['month'] = pd.to_datetime(df['date']).dt.to_period("M")
    expenses = df[df['type'] == 'expense'].copy()

    # Group by month and category
    monthly = expenses.groupby(['month', 'category'])['amount'].sum().abs().unstack().fillna(0)

    alerts = []
    if len(monthly) < 2:
        return []  # not enough months to compare

    this_month = monthly.iloc[-1]
    last_month = monthly.iloc[-2]

    for category in this_month.index:
        prev = last_month[category]
        curr = this_month[category]

        if prev > 0 and curr > prev * 2:  # more than 2x increase
            percent = ((curr - prev) / prev) * 100
            alerts.append(f"📈 '{category}' spending rose by {percent:.0f}% compared to last month.")

    return alerts
