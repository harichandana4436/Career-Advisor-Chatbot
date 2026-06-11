import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

# Generation Parameters
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 1024

# Conversation Management
MAX_HISTORY_TURNS = 10

# App Metadata
APP_TITLE = "Career Advisor Chatbot"
APP_SUBTITLE = "Your AI-powered career guidance companion"
APP_ICON = "💼"
BOT_NAME = "CareerBot"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "chatbot.log"