import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px



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

    fig = go.Figure(data=[go.Pie(
        labels=category_sum.index,
        values=category_sum.values,
        hole=0,  # No donut
        textinfo='label+percent',
        textfont=dict(size=12),
        insidetextorientation='radial',
        marker=dict(
            colors=['#EF553B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A'],
            line=dict(color='white', width=2)
        ),
        hovertemplate='%{label}: ₹%{value:,.0f}<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text='📌 Expenses by Category', x=0.2),
        height=400,
        margin=dict(t=60, b=40, l=20, r=20),
        showlegend=False,
        template='plotly_white'
    )
    return fig


def plot_monthly_bar_chart(df):
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=summary['month'], y=summary['income'],
        name='Income', marker_color='#00B686',
        hovertemplate='Income: ₹%{y:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=summary['month'], y=summary['expense'],
        name='Expense', marker_color='#F45B69',
        hovertemplate='Expense: ₹%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text='📊 Monthly Income vs Expense', x=0.2),
        barmode='group',
        height=400,
        xaxis=dict(title='Month'),
        yaxis=dict(title='Amount (₹)'),
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=60, b=40, l=40, r=20)
    )

    return fig


def plot_cumulative_balance(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['signed_amount'] = df.apply(lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1)
    df['cumulative_balance'] = df['signed_amount'].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['cumulative_balance'],
        mode='lines+markers',
        line=dict(color='#0077B6', width=2),
        marker=dict(size=4, color='#90E0EF'),
        hovertemplate='Date: %{x|%b %d, %Y}<br>Balance: ₹%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text='📈 Cumulative Balance Over Time', x=0.2),
        xaxis=dict(title='Date'),
        yaxis=dict(title='Balance (₹)'),
        template='plotly_white',
        height=400,
        margin=dict(t=60, b=40, l=40, r=20),
        showlegend=False
    )

    return fig



def plot_daily_expense_heatmap(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['month_year'] = df['date'].dt.strftime('%b %Y')

    heatmap_data = df[df['type'] == 'expense'].pivot_table(
        index='day',
        columns='month_year',
        values='amount',
        aggfunc='sum',
        fill_value=0
    )

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Reds',
        colorbar=dict(title='₹ Spent'),
        hovertemplate='Month: %{x}<br>Day: %{y}<br>₹%{z:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text='🌡️ Daily Expense Heatmap', x=0.2),
        xaxis=dict(side='top'),
        yaxis=dict(title='Day of Month'),
        height=450,
        margin=dict(t=60, b=40, l=40, r=20),
        template='plotly_white'
    )

    return fig


def plot_cash_flow_funnel(df):
    df = df.copy()
    df['signed_amount'] = df.apply(lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1)

    total_income = df[df['type'] == 'income']['amount'].sum()
    fixed_expenses = df[df['category'].str.contains('rent|loan|emi|subscription', case=False, na=False)]['amount'].sum()
    variable_expenses = df[df['category'].str.contains('food|travel|shopping|other', case=False, na=False)]['amount'].sum()
    discretionary = total_income - fixed_expenses - variable_expenses
    savings = discretionary if discretionary > 0 else 0

    stages = ['Total Income', 'Fixed Expenses', 'Variable Expenses', 'Discretionary Balance', 'Savings']
    values = [total_income, total_income - fixed_expenses, total_income - fixed_expenses - variable_expenses, discretionary, savings]

    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent previous+percent initial",
        marker=dict(color=['#2ECC71', '#F39C12', '#E74C3C', '#3498DB', '#9B59B6'])
    ))

    fig.update_layout(
        title=dict(text='🔁 Monthly Cash Flow Funnel', x=0.3),
        height=450,
        margin=dict(t=60, b=40, l=40, r=40),
        template='plotly_white'
    )

    return fig



