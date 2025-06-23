import matplotlib.pyplot as plt

def plot_profit_loss_bar(df):
    fig, ax = plt.subplots()
    ax.bar(df["Stock"], df["P&L"], color=["green" if x >= 0 else "red" for x in df["P&L"]])
    ax.set_title("Profit/Loss by Stock")
    ax.set_ylabel("₹")
    ax.set_xlabel("Stock")
    ax.axhline(0, color='gray', linewidth=0.8)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_portfolio_allocation(df):
    fig, ax = plt.subplots()
    sizes = df["Invested"]
    labels = df["Stock"]
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title("Portfolio Allocation")
    plt.tight_layout()
    return fig
