def generate_summary(df):
    if df.empty:
        return "No data to summarize."

    insights = []

    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()

    net_balance = total_income + total_expense  # expense is negative
    savings_rate = (net_balance / total_income * 100) if total_income else 0

    top_category = (
        df[df['type'] == 'expense']
        .groupby('category')['amount']
        .sum()
        .abs()
        .sort_values(ascending=False)
        .index[0]
    )

    insights.append(f"💰 Total income: ₹{total_income:,.0f}")
    insights.append(f"💸 Total expenses: ₹{abs(total_expense):,.0f}")
    insights.append(f"📊 Net balance: ₹{net_balance:,.0f}")
    insights.append(f"📁 Top spending category: {top_category}")
    insights.append(f"💡 You saved about {savings_rate:.1f}% of your income.")

    if abs(total_expense) > total_income:
        insights.append("⚠️ Warning: You're spending more than you earn!")

    return "\n".join(insights)


def extract_metrics_for_ai(df):
    total_income = df[df['type'] == 'income']['amount'].sum()
    total_expense = df[df['type'] == 'expense']['amount'].sum()
    net_balance = total_income + total_expense

    top_category = (
        df[df['type'] == 'expense']
        .groupby('category')['amount']
        .sum()
        .abs()
        .sort_values(ascending=False)
        .index[0]
    )

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(abs(total_expense), 2),
        "net_balance": round(net_balance, 2),
        "top_expense_category": top_category
    }
