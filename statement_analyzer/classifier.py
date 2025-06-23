import pandas as pd


def classify_transactions(df):
    df['type'] = df['amount'].apply(lambda x: 'income' if x >= 0 else 'expense')
    return df


def calculate_monthly_totals(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')

    summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
    summary.reset_index(inplace=True)
    summary['month'] = summary['month'].astype(str)

    return summary
