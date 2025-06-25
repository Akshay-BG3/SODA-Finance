import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# def plot_expense_pie_chart(df):
#     expense_df = df[df['type'] == 'expense']
#     category_sum = expense_df.groupby('category')['amount'].sum().abs()
#
#     fig, ax = plt.subplots(figsize=(3.5, 3.5))  # Smaller figure
#     wedges, texts, autotexts = ax.pie(
#         category_sum,
#         labels=category_sum.index,
#         autopct='%1.0f%%',
#         startangle=90,
#         textprops=dict(color="black", fontsize=7)
#     )
#     ax.axis('equal')
#     plt.title('Expenses by Category', fontsize=9)
#     return fig

def plot_expense_pie_chart(df):
    expense_df = df[df['type'] == 'expense']
    category_sum = expense_df.groupby('category')['amount'].sum().abs()

    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(
        category_sum,
        labels=category_sum.index,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.4),
        textprops=dict(color="black", fontsize=8)
    )
    ax.axis('equal')
    plt.title('Expenses by Category', fontsize=10, fontweight='bold')
    return fig


# def plot_monthly_bar_chart(df):
#     df['date'] = pd.to_datetime(df['date'])
#     df['month'] = df['date'].dt.to_period('M').astype(str)
#     summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
#
#     fig, ax = plt.subplots(figsize=(5.5, 3))  # Smaller chart
#     summary.plot(kind='bar', ax=ax, width=0.5, color=['green', 'red'])
#
#     plt.title('Monthly Income vs Expense', fontsize=9)
#     plt.xlabel('Month', fontsize=8)
#     plt.ylabel('Amount', fontsize=8)
#     plt.xticks(rotation=30, fontsize=7)
#     plt.yticks(fontsize=7)
#     plt.tight_layout()
#     return fig

def plot_monthly_bar_chart(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    colors = {'income': '#4CAF50', 'expense': '#F44336'}
    bars = summary.plot(kind='bar', ax=ax, width=0.6, color=[colors.get(x) for x in summary.columns])

    plt.title('Monthly Income vs Expense', fontsize=11, fontweight='bold')
    plt.xlabel('Month', fontsize=9)
    plt.ylabel('Amount', fontsize=9)
    plt.xticks(rotation=30, fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(axis='y', linestyle='--', linewidth=0.5)

    # Annotate bars
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=7, color='black', xytext=(0, 2), textcoords='offset points')

    plt.tight_layout()
    return fig

def plot_cumulative_balance(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['signed_amount'] = df.apply(lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1)
    df['cumulative_balance'] = df['signed_amount'].cumsum()

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df['date'], df['cumulative_balance'], color='#2196F3', linewidth=2)
    ax.set_title("Cumulative Balance Over Time", fontsize=10, fontweight='bold')
    ax.set_xlabel("Date", fontsize=8)
    ax.set_ylabel("Balance", fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.tight_layout()
    return fig

def plot_daily_expense_heatmap(df):
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.strftime('%b %Y')

    pivot = df[df['type'] == 'expense'].pivot_table(index='day', columns='month', values='amount', aggfunc='sum', fill_value=0)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(pivot, cmap="Reds", linewidths=0.2, linecolor='gray', ax=ax, cbar_kws={'label': 'Expense Amount'})
    ax.set_title('Daily Expense Heatmap', fontsize=10, fontweight='bold')
    plt.yticks(rotation=0)
    plt.tight_layout()
    return fig

