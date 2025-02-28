import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
HUGGING_TOKEN = os.getenv("HUGGING_TOKEN")