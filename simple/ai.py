import os
from openai import OpenAI

def load_env():
    """Load environment variables from .env file if available"""
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
        load_dotenv(env_path)
    except Exception:
        print("Error loading environment variables.")
        pass

def get_ai_response(prompt, context="", max_tokens=800, temperature=0.2):
    """Get AI response for data analysis questions"""
    load_env()

    if not os.getenv("OPENAI_API_KEY"):
        return "[Error: OPENAI_API_KEY not set. Please create a .env file with your API key.]"

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    messages = [
        {"role": "system",
         "content": ("You are a healthcare data analyst specializing in pregnancy-related data\n"
                     "When asked to analyze data, you must:\n"
                    "1. Use the given data context (example columns: Age, BMI, BloodPressure, Week, Glucose, ActivityLevel, SleepHours, RiskScore).\n"
                    "2. Return an analysis based on real data from the context, including numbers, averages, percentages, and correlation metrics where possible.\n"
                    "3. Identify trends, group comparisons, risk factors, and anomalies.\n"
                    "4. Be concise yet comprehensive—provide clear conclusions and useful information.\n"
                    "5. If data is missing, note it and suggest what could be examined.\n"
                    "5. Try to short your answer.\n"
                    "6. Goal: Provide practical insights that can be used to improve patient health.")},
        {"role": "user",
         "content": f"Dataset Context:\n{context.strip() or '(none)'}\n\nUser Question:\n{prompt.strip()}\n\nPlease analyze this data and give me the actual results and insights."}
    ]

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"[AI error: {e}]"
