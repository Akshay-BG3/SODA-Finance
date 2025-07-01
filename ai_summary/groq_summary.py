import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_groq_summary(metrics: dict, user_query: str, tone_instruction: str):
    prompt = f"""
You are a helpful and intelligent financial Copilot. 
Adjust your tone according to the user’s preference: {tone_instruction}

You have access to the following user financial data:
{metrics}

Use it if relevant. Otherwise, answer the user query naturally.

User Query: {user_query}
"""

#     prompt = f"""
# You are a smart financial assistant.
#
# Based on this user's financial data, generate a 3-line summary:
# - Total income vs expense
# - Top spending category
# - One suggestion to improve finances
#
# Metrics:
# {metrics}
#     """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        print("🔍 Groq API Response:", result)
        print("🔍 Response text:", response.text)

        # Safely extract the message
        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return "⚠️ Groq API returned an unexpected response. Please try again later."

    except Exception as e:
        return f"⚠️ Error reaching Groq API: {e}"