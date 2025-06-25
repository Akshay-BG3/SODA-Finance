import streamlit as st
import pandas as pd
import base64
import re
import requests
from datetime import datetime

from statement_analyzer.file_handler import load_csv, clean_dataframe
from statement_analyzer.classifier import classify_transactions, calculate_monthly_totals
from statement_analyzer.analyzer import get_top_expense_categories, get_monthly_category_trends
from statement_analyzer.charts import plot_expense_pie_chart, plot_monthly_bar_chart, plot_cumulative_balance, plot_daily_expense_heatmap
from statement_analyzer.insights import generate_summary, extract_metrics_for_ai
from ai_summary.groq_summary import generate_groq_summary
from risk_detection.alerts import detect_risks, detect_spending_spikes
from risk_detection.outliers import detect_outliers
from portfolio.portfolio_handler import load_portfolio
from portfolio.portfolio_analyzer import analyze_portfolio
from portfolio.portfolio_charts import plot_profit_loss_bar, plot_portfolio_allocation
from agent.agent_core import generate_agent_brief, generate_agent_full_plan_prompt, fallback_agent_plan
from agent.agent_memory import save_metrics_to_memory, load_previous_metrics, compare_metrics
from agent.pdf_report import generate_pdf

st.set_page_config(page_title="SODA-Finance", layout="wide")

# Function to set background image
# def set_bg(image_file):
#     with open(image_file, "rb") as f:
#         encoded_img = base64.b64encode(f.read()).decode()
#
#     st.markdown(f"""
#         <style>
#         body {{
#             background-image: url("data:image/png;base64,{encoded_img}");
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#         }}
#         .stApp::before {{
#             content: "";
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             background-color: rgba(255, 255, 255, 0.6);
#             z-index: -1;
#         }}
#         </style>
#     """, unsafe_allow_html=True)
#
#     set_bg(r"C:\Users\USER\PycharmProjects\Project DARA\background.jpg.jpg")
#
#     st.markdown("""
#         <style>
#         .stMarkdown, .stDataFrame, .stImage, .stSubheader, .stText, .stPlotlyChart, .stPyplotChart {
#             background-color: rgba(255, 255, 255, 0.85);
#             padding: 1rem;
#             border-radius: 1rem;
#             margin-bottom: 1rem;
#             box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
#         }
#         </style>
#     """, unsafe_allow_html=True)




def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# st.set_page_config(page_title="SODA-Finance", layout="wide")


st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #f0f0f0;
        color: #1e1e1e;
    }}

    html, body, [class*="css"] {{
        color: #1e1e1e !important;
        font-family: 'Montserrat', sans-serif;
    }}

    .stMarkdown, .stDataFrame, .stImage, .stSubheader, .stText, .stPlotlyChart, .stPyplotChart {{
        background-color: #ffffff;
        padding: 1rem;
         border-radius: 1rem;
        margin-bottom: 1rem;
        color: #1e1e1e !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    }}

    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap');
    </style>
    """,
    unsafe_allow_html=True
)



col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown(
        "<h1 style='color:#004d4d;'>SODA-Finance</h1>"
        "<h4 style='margin-top:-10px;color:#2e2e3a;'>Self-Operating Data Intelligence Agent</h4>",
        unsafe_allow_html=True,
    )
st.markdown(f"**🕒 Report Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

st.markdown("---")



uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file is not None:
    df = load_csv(uploaded_file)
    if isinstance(df, pd.DataFrame):
        df = clean_dataframe(df)
        df = classify_transactions(df)

        st.success("✅ File loaded, cleaned, and classified!")
        st.markdown("---")
        st.subheader("📄 Cleaned Transactions")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Monthly Income/Expense Summary")
        monthly_summary = calculate_monthly_totals(df)
        st.dataframe(monthly_summary, use_container_width=True)

        st.markdown("---")
        st.subheader("💸 Top 5 Expense Categories")
        top_expenses = get_top_expense_categories(df)
        st.dataframe(top_expenses, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Monthly Category Trend")
        trend_data = get_monthly_category_trends(df)
        st.dataframe(trend_data, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Expense Distribution (Pie Chart)")
        pie_chart = plot_expense_pie_chart(df)
        st.pyplot(pie_chart)

        st.markdown("---")
        st.subheader("📈 Monthly Income vs Expense (Bar Chart)")
        bar_chart = plot_monthly_bar_chart(df)
        st.pyplot(bar_chart)

        st.markdown("---")
        st.subheader("🧐 Summary Insights")
        summary = generate_summary(df)
        st.text(summary)

        st.markdown("---")
        st.subheader("🤖 AI-Generated Financial Report")
        try:
            metrics = extract_metrics_for_ai(df)
            ai_summary = generate_groq_summary(metrics)
            st.text(ai_summary)
        except Exception as e:
            st.warning("⚠️ AI summary not available.\n" + str(e))

        st.markdown("---")
        st.subheader("⚠️ Risk & Opportunity Detection")
        alerts = detect_risks(df)
        for alert in alerts:
            st.markdown(alert)

        st.markdown("---")
        st.subheader("🧪 Suspicious Transactions (Outlier Detection)")
        outliers_df, outlier_alerts = detect_outliers(df)

        if outlier_alerts:
            for alert in outlier_alerts:
                st.markdown(alert)
            st.dataframe(outliers_df[['date', 'description', 'amount', 'category']], use_container_width=True)
        else:
            st.success("✅ No suspicious transactions found.")

        st.markdown("---")
        st.subheader("📈 Spending Spikes")
        spike_alerts = detect_spending_spikes(df)

        if spike_alerts:
            for spike in spike_alerts:
                st.warning(spike)
        else:
            st.success("✅ No abnormal monthly spending spikes.")

        st.markdown("---")
        st.subheader("🧐 SODA Agent Suggestion")
        try:
            metrics = extract_metrics_for_ai(df)
            risks = detect_risks(df)
            agent_prompt = generate_agent_brief(metrics, risks)
            agent_response = generate_groq_summary({"prompt": agent_prompt})
            st.text(agent_response)
        except Exception as e:
            st.warning("⚠️ Agent failed: " + str(e))

        st.markdown("---")
        st.subheader("📋 SODA Suggested Next Steps")
        try:
            plan_prompt = generate_agent_full_plan_prompt(metrics, risks)
            ai_plan = generate_groq_summary({"prompt": plan_prompt})
            st.text(ai_plan)
        except Exception as e:
            st.warning("⚠️ AI plan generation failed. Showing fallback plan.")
            fallback = fallback_agent_plan(metrics, risks)
            st.markdown(fallback)

        prev_metrics = load_previous_metrics()
        memory_insight = compare_metrics(metrics, prev_metrics)

        st.markdown("---")
        st.subheader("🧠 Memory Insight")
        st.markdown(memory_insight)

        save_metrics_to_memory(metrics)

        st.markdown("---")
        st.subheader("📤 Export Report as PDF")
        try:
            cleaned_summary = remove_emojis(summary)
            cleaned_ai_summary = remove_emojis(ai_summary)
            cleaned_alerts = remove_emojis("\n".join(alerts))
            pdf_data = generate_pdf(summary, ai_summary, memory_insight)
            b64 = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="SODA_Report.pdf">📅 Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.warning("⚠️ Could not generate PDF: " + str(e))

        st.markdown("---")
        st.subheader("📥 Upload Portfolio CSV")
        portfolio_file = st.file_uploader("Upload your investment portfolio", type=["csv"], key="portfolio")

        if portfolio_file:
            portfolio_df = load_portfolio(portfolio_file)
            if isinstance(portfolio_df, pd.DataFrame):
                st.success("✅ Portfolio loaded successfully")
                st.dataframe(portfolio_df, use_container_width=True)
            else:
                st.error(portfolio_df)

            if portfolio_file and isinstance(portfolio_df, pd.DataFrame):
                st.markdown("---")
                st.subheader("📉 Portfolio Performance")
                result_df = analyze_portfolio(portfolio_df)
                st.dataframe(result_df, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Profit/Loss Chart")
        bar_chart = plot_profit_loss_bar(result_df)
        st.pyplot(bar_chart)

        st.markdown("---")
        st.subheader("🦁 Investment Allocation")
        pie_chart = plot_portfolio_allocation(result_df)
        st.pyplot(pie_chart)

        best = result_df.iloc[0]
        worst = result_df.iloc[-1]

        st.markdown(f"🥇 **Top Gainer:** {best['Stock']} (+{best['ROI (%)']}%)")
        st.markdown(f"🥀 **Top Loser:** {worst['Stock']} ({worst['ROI (%)']}%)")

    else:
        st.error(df)
else:
    st.info("⬆️ Please upload a CSV file to get started.")
