import os 
from openai import OpenAI

def load_env():
    """Load environment variables from .env file if available."""
    try:
        # Import dotenv only when needed, so the code doesn't break if it's missing
        from dotenv import load_dotenv
        # Find the .env file in the parent directory
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
        load_dotenv(env_path)  # Load all variables from the file into the environment
    except Exception:
        # If loading fails, just print an error but don't stop the program
        print("Error loading environment variables.")
        pass

def get_ai_response(prompt, context="", max_tokens=800, temperature=0.2):
    """
    Send a question to the AI model with optional dataset context.
    This function:
    - Loads environment variables (API key, model name, etc.)
    - Connects to the OpenAI API
    - Sends the user question along with a 'system' instruction about how to respond
    - Returns the AI's answer
    """
    load_env()  # Ensure API key and other settings are loaded

    # If there's no API key, return an error message instead of trying to connect
    if not os.getenv("OPENAI_API_KEY"):
        return "[Error: OPENAI_API_KEY not set. Please create a .env file with your API key.]"

    # Create a client to talk to OpenAI
    client = OpenAI()
    # Pick model from environment variable or use default "gpt-5-nano"
    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    # Build the conversation that will be sent to the AI
    messages = [
        {
            "role": "system",
            "content": (
                "You are a healthcare data analyst specializing in pregnancy-related data\n"
                "When asked to analyze data, you must:\n"
                "1. Use the given data context (example columns: Age, BMI, BloodPressure, Week, Glucose, ActivityLevel, SleepHours, RiskScore).\n"
                "2. Return an analysis based on real data from the context, including numbers, averages, percentages, and correlation metrics where possible.\n"
                "3. Identify trends, group comparisons, risk factors, and anomalies.\n"
                "4. Be concise yet comprehensive—provide clear conclusions and useful information.\n"
                "5. If data is missing, note it and suggest what could be examined.\n"
                "5. Try to short your answer.\n"
                "6. Goal: Provide practical insights that can be used to improve patient health."
            )
        },
        {
            "role": "user",
            "content": (
                f"Dataset Context:\n{context.strip() or '(none)'}\n\n"
                f"User Question:\n{prompt.strip()}\n\n"
                "Please analyze this data and give me the actual results and insights."
            )
        }
    ]

    try:
        # Call the OpenAI Chat API
        resp = client.chat.completions.create(
            model=model,            # The chosen AI model
            messages=messages,      # The system + user messages
            max_tokens=max_tokens,  # Limit the size of the answer
            temperature=temperature # Control creativity (low = more factual)
        )
        # Return only the AI's text answer, removing any extra whitespace
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        # If something went wrong (e.g., network error, API issue), return the error
        return f"[AI error: {e}]"
