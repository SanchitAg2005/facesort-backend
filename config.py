import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
MODE = os.getenv("MODE")  # CPU | GPU

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

SLEEP_SECONDS = 5

REQUIRED = [
    ENV, MODE,
    MONGO_URI, MONGO_DB,
    SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_BUCKET,
    TELEGRAM_BOT_TOKEN
]

if not all(REQUIRED):
    raise RuntimeError("Missing environment variables")
