import pandas as pd

def get_top_expense_categories(df, top_n=5):
    expense_df = df[df['type'] == 'expense']
    top_categories = (
        expense_df.groupby('category')['amount']
        .sum()
        .sort_values()
        .head(top_n)
        .abs()
        .reset_index()
        .rename(columns={'amount': 'total_spent'})
    )
    return top_categories

def get_monthly_category_trends(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    trend_data = df.groupby(['month', 'category'])['amount'].sum().unstack(fill_value=0).round(2)
    return trend_data
