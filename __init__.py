import os
from dotenv import load_dotenv

def load_environment():
    """
    Loads environment variables from a .env file if it exists.
    """
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable not found. Agents will fall back to mock implementations.")
