import pandas as pd

def detect_risks(df):
    if df.empty:
        return ["No data to analyze."]

    alerts = []

    # Calculate total income and expense
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()

    # 1. Overspending Alert
    if abs(total_expense) > total_income:
        alerts.append("🔴 You're spending more than you earn! Try reducing expenses.")

    # 2. Low Savings Rate Alert
    net_balance = total_income + total_expense  # Expense is negative
    savings_rate = (net_balance / total_income) * 100 if total_income else 0

    if savings_rate <= 10:
        alerts.append(f"🟠 Your savings rate is low ({savings_rate:.1f}%). Try saving at least 20%.")

    # 3. Spending Concentration Alert
    category_spending = (
        df[df['type'] == 'expense']
        .groupby('category')['amount']
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    if not category_spending.empty:
        top_category = category_spending.index[0]
        top_share = category_spending.iloc[0] / category_spending.sum()
        if top_share > 0.5:
            alerts.append(f"🔵 Over 50% of your expenses are in '{top_category}'. Try diversifying your spending.")

    if not alerts:
        alerts.append("✅ No major risks detected. You're doing well!")

    return alerts

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




