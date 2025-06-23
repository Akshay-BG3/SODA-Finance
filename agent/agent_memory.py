
import json
import os

MEMORY_FILE = "agent/memory_store.json"


def save_metrics_to_memory(metrics, file_path="agent/memory_store.json"):
    # Convert all values to native Python types
    clean_metrics = {k: float(v) if isinstance(v, (int, float)) else str(v) for k, v in metrics.items()}

    with open(file_path, "w") as f:
        json.dump(clean_metrics, f)

def load_previous_metrics(file_path="agent/memory_store.json"):
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None  # fallback for corrupted or empty files

def compare_metrics(current, previous):
    try:
        diff_income = float(current['total_income']) - float(previous['total_income'])
        diff_expense = float(current['total_expense']) - float(previous['total_expense'])
        diff_balance = float(current['net_balance']) - float(previous['net_balance'])

        summary = f"Compared to last session:\n"
        summary += f"💵 Income changed by ₹{diff_income:,.0f}\n"
        summary += f"💸 Expenses changed by ₹{diff_expense:,.0f}\n"
        summary += f"📊 Net balance changed by ₹{diff_balance:,.0f}"

        return summary
    except Exception as e:
        return f"⚠️ Could not compare with previous session: {e}"
