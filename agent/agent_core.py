

def generate_agent_brief(metrics: dict, risks: list) -> str:
    """
    Creates a smart prompt for the AI agent to suggest next action.
    """
    brief = f"""
You are SODA, a smart financial assistant.

User Financial Summary:
- Total Income: ₹{metrics['total_income']}
- Total Expenses: ₹{metrics['total_expense']}
- Net Balance: ₹{metrics['net_balance']}
- Top Expense Category: {metrics['top_expense_category']}

Identified Risks:
"""
    if risks:
        for risk in risks:
            brief += f"- {risk}\n"
    else:
        brief += "- None\n"

    brief += """
Based on this, what should the user do next? 
Give one or two useful financial suggestions.
Be clear and simple.
"""
    return brief.strip()


def generate_agent_full_plan_prompt(metrics: dict, risks: list) -> str:
    """
    Builds a prompt asking the LLM to generate a full improvement plan.
    """
    prompt = f"""
You are a smart financial planning assistant.

Here’s the user’s financial summary:
- Total Income: ₹{metrics['total_income']}
- Total Expenses: ₹{metrics['total_expense']}
- Net Balance: ₹{metrics['net_balance']}
- Top Expense Category: {metrics['top_expense_category']}

Risks/Issues Detected:
"""
    if risks:
        for risk in risks:
            prompt += f"- {risk}\n"
    else:
        prompt += "- No major risks detected.\n"

    prompt += """
Generate a personalized 2–3 step improvement plan for the user.
Make it clear, short, and friendly.
Each step should be actionable and use emojis.
"""
    return prompt.strip()


def fallback_agent_plan(metrics: dict, risks: list) -> str:
    """
    Rule-based fallback plan (used only if AI fails).
    """
    suggestions = []

    if abs(metrics['total_expense']) > metrics['total_income']:
        suggestions.append("📉 Create a spending cap for top 2 categories.")

    savings_rate = (
        (metrics['net_balance'] / metrics['total_income']) * 100
        if metrics['total_income'] else 0
    )
    if 0 < savings_rate <= 10:
        suggestions.append("💸 Move 10% of your income to a savings account automatically.")

    if 'Food' in metrics['top_expense_category']:
        suggestions.append("🍽️ Limit food delivery spending to ₹2000 per month.")

    if not suggestions:
        suggestions.append("✅ No urgent actions. You can focus on investment planning.")

    return "\n".join(suggestions)
