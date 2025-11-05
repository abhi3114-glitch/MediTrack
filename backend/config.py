import os
import pathlib
from dotenv import load_dotenv

# Get absolute path to the .env file in MEDITRACK/
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]  # backend/
ENV_PATH = ROOT_DIR / ".env"                            # backend/.env (wrong)
if not ENV_PATH.exists():
    # Move one more level up (MEDITRACK/)
    ENV_PATH = ROOT_DIR.parent / ".env"

# Load the .env file
load_dotenv(dotenv_path=ENV_PATH)

# Telegram credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Blockchain connection
GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")

# Database
DB_PATH = ROOT_DIR / "meditrack.db"

def show_loaded():
    print("✅ .env loaded from:", ENV_PATH)
    print("💬 Telegram Chat ID:", TELEGRAM_CHAT_ID)
    print("🔗 Ganache URL:", GANACHE_URL)
