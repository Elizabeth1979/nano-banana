import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
NANO_BANANA_MODEL = "google/gemini-2.5-flash-image-preview"
GPT4_MINI_MODEL = "openai/gpt-4o-mini"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")