import streamlit as st
import pandas as pd
import base64
import re
import requests
import os
from datetime import datetime
from streamlit import session_state



from statement_analyzer.file_handler import load_csv, clean_dataframe
from statement_analyzer.classifier import classify_transactions, calculate_monthly_totals
from statement_analyzer.analyzer import get_top_expense_categories, get_monthly_category_trends
from statement_analyzer.charts import plot_expense_pie_chart, plot_monthly_bar_chart, plot_cumulative_balance, plot_daily_expense_heatmap, plot_cash_flow_funnel
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


# st.set_page_config(page_title="SODA-Finance", layout="wide")
st.set_page_config(page_title="SODA Ultra", layout="wide")

with open("style/ultra.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)



# Branding Topbar
col1, col2 = st.columns([1.5, 8])
with col1:
    st.image("logo.png", width=190)
with col2:
    st.markdown("<h1 class='hero-title'>SODA-Finance</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='hero-subtitle'>Your Self-Operating Data Intelligence Agent</h4>", unsafe_allow_html=True)

st.markdown(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
# st.markdown("---")


# Paths to your renamed demo data files
DEMO_BANK_PATH = "demo_data/demo_bank_statement.csv"
DEMO_PORTFOLIO_PATH = "demo_data/demo_stocks_portfolio.csv"

# Ensure the demo_data folder exists
os.makedirs("demo_data", exist_ok=True)

# Load demo files (these are the ones you uploaded)
# bank_demo_df = pd.read_csv("/mnt/data/sample.csv")
# portfolio_demo_df = pd.read_csv("/mnt/data/sample_portfolio.csv")
bank_demo_df = pd.read_csv("demo_data/demo_bank_statement.csv")
portfolio_demo_df = pd.read_csv("demo_data/demo_stocks_portfolio.csv")


# Save them with the correct custom names
bank_demo_df.to_csv(DEMO_BANK_PATH, index=False)
portfolio_demo_df.to_csv(DEMO_PORTFOLIO_PATH, index=False)


# Sidebar toggle
use_demo = st.sidebar.checkbox("🔁 Use Demo Dataset", value=False)

if use_demo:
    st.success("✅ Demo Mode Enabled – Download the example CSVs below.")

    # Download buttons with custom filenames
    st.subheader("⬇️ Download Demo CSV Files")

    bank_csv = bank_demo_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Demo Bank Statement",
        data=bank_csv,
        file_name="demo_bank_statement.csv",
        mime="text/csv"
    )

    portfolio_csv = portfolio_demo_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Demo Portfolio (Stocks)",
        data=portfolio_csv,
        file_name="demo_stocks_portfolio.csv",
        mime="text/csv"
    )

    st.info("You can now upload these files manually to test the system.")



uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file is not None:
    df = load_csv(uploaded_file)
    if isinstance(df, pd.DataFrame):
        df = clean_dataframe(df)
        df = classify_transactions(df)
        df['date'] = pd.to_datetime(df['date'])

        # ───────────────────────────
        # 🧭 Sidebar Filters
        # ───────────────────────────
        st.sidebar.header("🔧 Dashboard Filters")

        min_date = df['date'].min()
        max_date = df['date'].max()

        date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

        categories = sorted(df['category'].dropna().unique())
        selected_categories = st.sidebar.multiselect("Select Categories", categories, default=categories)

        # Filtered data to be used across app
        filtered_df = df[
            (df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1])) &
            (df['category'].isin(selected_categories))
            ]

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


        # ───────────────────────────
        # 📌 Key Financial Highlights
        # ───────────────────────────
        st.markdown("### 💼 Key Highlights", unsafe_allow_html=True)
        total_income = filtered_df[filtered_df['type'] == 'income']['amount'].sum()
        total_expense = filtered_df[filtered_df['type'] == 'expense']['amount'].sum()
        savings = total_income - total_expense
        savings_rate = (savings / total_income) * 100 if total_income > 0 else 0

        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     st.metric(label="📥 Total Income", value=f"₹{total_income:,.0f}")
        # with col2:
        #     st.metric(label="💸 Total Expense", value=f"₹{total_expense:,.0f}")
        # with col3:
        #     st.metric(label="💰 Savings Rate", value=f"{savings_rate:.1f}%")

        st.markdown("### Key Highlights", unsafe_allow_html=True)
        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.markdown("""
                <div class='kpi-card'>
                    <div class='kpi-label'>Total Income</div>
                    <div class='kpi-value'>₹{:,.0f}</div>
                </div>
            """.format(total_income), unsafe_allow_html=True)

        with kpi2:
            st.markdown("""
                <div class='kpi-card'>
                    <div class='kpi-label'>Total Expense</div>
                    <div class='kpi-value'>₹{:,.0f}</div>
                </div>
            """.format(total_expense), unsafe_allow_html=True)

        with kpi3:
            st.markdown("""
                <div class='kpi-card'>
                    <div class='kpi-label'>Savings Rate</div>
                    <div class='kpi-value'>{:.1f}%</div>
                </div>
            """.format(savings_rate), unsafe_allow_html=True)

        # ───────────────────────────
        # 📊 Visualization Tabs
        # ───────────────────────────

        st.markdown("## 📊 Visual Analysis", unsafe_allow_html=True)
        tabs = st.tabs(["📊 Trends", "📈 Distribution", "🔁 Flow"])

        # 📊 Trends Tab
        with tabs[0]:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Monthly Income vs Expense", unsafe_allow_html=True)
                st.plotly_chart(plot_monthly_bar_chart(filtered_df), use_container_width=True)
            with col2:
                st.markdown("#### 📉 Cumulative Balance Over Time", unsafe_allow_html=True)
                st.plotly_chart(plot_cumulative_balance(filtered_df), use_container_width=True)

        # 📈 Distribution Tab
        with tabs[1]:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🥧 Expense Distribution", unsafe_allow_html=True)
                st.plotly_chart(plot_expense_pie_chart(filtered_df), use_container_width=True)
            with col2:
                st.markdown("#### 🌡️ Daily Expense Heatmap", unsafe_allow_html=True)
                st.plotly_chart(plot_daily_expense_heatmap(filtered_df), use_container_width=True)

        # 🔁 Flow Tab
        with tabs[2]:
            st.markdown("#### 🔁 Cash Flow Funnel", unsafe_allow_html=True)
            st.plotly_chart(plot_cash_flow_funnel(filtered_df), use_container_width=True)


        # st.markdown("---")
        # st.subheader("🧐 Summary Insights")
        # summary = generate_summary(df)
        # st.text(summary)
        #
        # st.markdown("---")
        # st.subheader("🤖 AI-Generated Financial Report")
        # try:
        #     metrics = extract_metrics_for_ai(df)
        #     ai_summary = generate_groq_summary(metrics, user_query, personality_instruction)
        #     st.text(ai_summary)
        # except Exception as e:
        #     st.warning("⚠️ AI summary not available.\n" + str(e))


        # ───────────────────────────
        # 🤖 Copilot in Sidebar
        # ───────────────────────────
        # with st.sidebar:
        #     st.markdown("### 🤖 SODA Copilot")
        #
        #     # Tone selector
        #     tone = st.selectbox("Choose Tone", ["Professional", "Friendly", "Blunt Analyst"])
        #     personality_instruction = {
        #         "Professional": "Respond formally and clearly, like a financial advisor.",
        #         "Friendly": "Speak with encouragement and warmth, like a coach.",
        #         "Blunt Analyst": "Be direct and focus strictly on numbers and logic."
        #     }[tone]
        #
        #     # User input
        #     user_query = st.text_input("Ask me anything about your finances:")
        #
        #     if user_query:
        #         # You can place these earlier in the script too
        #         metrics = extract_metrics_for_ai(filtered_df)
        #         risks = detect_risks(filtered_df)
        #
        #         base_prompt = generate_agent_brief(metrics, risks) + "\nUser Query: " + user_query
        #         prompt = personality_instruction + "\n\n" + base_prompt
        #
        #         try:
        #             # ai_response = generate_groq_summary({"prompt": prompt})
        #             ai_response = generate_groq_summary(metrics, user_query, personality_instruction)
        #             st.markdown("##### 💬 SODA Says")
        #             st.write(ai_response)
        #         except Exception as e:
        #             st.warning(f"⚠️ Couldn’t generate a response:\n{e}")
        with st.sidebar:
            st.markdown("### 🤖 SODA Copilot")

            # Tone selector
            tone = st.selectbox("Choose Tone", ["Professional", "Friendly", "Blunt Analyst"])
            personality_instruction = {
                "Professional": "Respond formally and clearly, like a financial advisor.",
                "Friendly": "Speak with encouragement and warmth, like a coach.",
                "Blunt Analyst": "Be direct and focus strictly on numbers and logic."
            }[tone]

            # Session state setup
            if "copilot_response" not in st.session_state:
                st.session_state.copilot_response = None
                st.session_state.last_query = ""

            user_query = st.text_input("Ask me anything about your finances:")

            if st.button("Ask SODA"):
                if user_query.strip() and user_query != st.session_state.last_query:
                    metrics = extract_metrics_for_ai(filtered_df)
                    risks = detect_risks(filtered_df)
                    try:
                        st.session_state.copilot_response = generate_groq_summary(metrics, user_query,
                                                                                  personality_instruction)
                        st.session_state.last_query = user_query
                    except Exception as e:
                        st.session_state.copilot_response = f"⚠️ Couldn’t generate response:\n{e}"

            if st.session_state.copilot_response:
                st.markdown("##### 💬 SODA Says")
                st.write(st.session_state.copilot_response)

        # if user_query:
        #     st.markdown("### 🤖 AI-Generated Financial Report")
        #     try:
        #         metrics = extract_metrics_for_ai(df)
        #         ai_summary = generate_groq_summary(metrics, user_query, personality_instruction)
        #         st.text(ai_summary)
        #     except Exception as e:
        #         st.warning("⚠️ AI summary not available.\n" + str(e))
        # else:
        #     st.info("💬 Enter a query in the Copilot panel to get an AI response.")


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

        #
        # st.markdown("---")
        # st.subheader("🧐 SODA Agent Suggestion")
        #
        # try:
        #     metrics = extract_metrics_for_ai(df)
        #     risks = detect_risks(df)
        #     agent_prompt = "What key risks or financial opportunities do you see in this data?"
        #     # Pass tone and dummy user_query for compatibility
        #     agent_response = generate_groq_summary(metrics, agent_prompt, personality_instruction)
        #     st.text(agent_response)
        # except Exception as e:
        #     st.warning("⚠️ Agent failed: " + str(e))
        st.markdown("---")
        st.subheader("🧐 SODA Agent Suggestion")

        if "agent_suggestion" not in st.session_state:
            try:
                metrics = extract_metrics_for_ai(df)
                risks = detect_risks(df)
                agent_prompt = "What key risks or financial opportunities do you see in this data?"
                st.session_state.agent_suggestion = generate_groq_summary(metrics, agent_prompt,
                                                                          personality_instruction)
            except Exception as e:
                st.session_state.agent_suggestion = f"⚠️ Agent failed: {e}"

        st.text(st.session_state.agent_suggestion)

        st.markdown("---")
        st.subheader("📋 SODA Suggested Next Steps")

        try:
            plan_prompt = "Based on this data, suggest 3 next financial steps."
            ai_plan = generate_groq_summary(metrics, plan_prompt, personality_instruction)
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

        summary = generate_summary(df)

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
        # graphs


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
        # result_
        st.markdown(f"🥇 **Top Gainer:** {best['Stock']} (+{best['ROI (%)']}%)")
        st.markdown(f"🥀 **Top Loser:** {worst['Stock']} ({worst['ROI (%)']}%)")

    else:
        st.error(df)
else:
    st.info("⬆️ Please upload a CSV file to get started.")
