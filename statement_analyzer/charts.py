import matplotlib.pyplot as plt
import pandas as pd

def plot_expense_pie_chart(df):
    expense_df = df[df['type'] == 'expense']
    category_sum = expense_df.groupby('category')['amount'].sum().abs()

    fig, ax = plt.subplots(figsize=(3.5, 3.5))  # Smaller figure
    wedges, texts, autotexts = ax.pie(
        category_sum,
        labels=category_sum.index,
        autopct='%1.0f%%',
        startangle=90,
        textprops=dict(color="black", fontsize=7)
    )
    ax.axis('equal')
    plt.title('Expenses by Category', fontsize=9)
    return fig


def plot_monthly_bar_chart(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(5.5, 3))  # Smaller chart
    summary.plot(kind='bar', ax=ax, width=0.5, color=['green', 'red'])

    plt.title('Monthly Income vs Expense', fontsize=9)
    plt.xlabel('Month', fontsize=8)
    plt.ylabel('Amount', fontsize=8)
    plt.xticks(rotation=30, fontsize=7)
    plt.yticks(fontsize=7)
    plt.tight_layout()
    return fig
