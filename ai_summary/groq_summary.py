import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_groq_summary(metrics: dict):
    prompt = f"""
You are a smart financial assistant.

Based on this user's financial data, generate a 3-line summary:
- Total income vs expense
- Top spending category
- One suggestion to improve finances

Metrics:
{metrics}
    """

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        print("🔍 Groq API Response:", result)
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating Groq summary: {e}"
