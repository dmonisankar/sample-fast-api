import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

ARIZE_API_KEY = os.getenv("ARIZE_API_KEY")
ARIZE_SPACE_ID = os.getenv("ARIZE_SPACE_ID")
PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
PHOENIX_ENDPOINT = os.getenv("PHOENIX_ENDPOINT")
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"


if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env file")
