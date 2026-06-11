import logging
import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    MAX_HISTORY_TURNS,
    LOG_FILE,
    LOG_LEVEL
)

from prompts import (
    CAREER_ADVISOR_SYSTEM_PROMPT,
    FALLBACK_RESPONSE
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=CAREER_ADVISOR_SYSTEM_PROMPT
)


def trim_history(history: list) -> list:
    max_messages = MAX_HISTORY_TURNS * 2
    if len(history) > max_messages:
        return history[-max_messages:]
    return history


def build_prompt(user_message: str, chat_history: list) -> str:
    prompt = ""
    for msg in chat_history:
        role = msg["role"].capitalize()
        prompt += f"{role}: {msg['content']}\n"
    prompt += f"User: {user_message}"
    return prompt


def get_response(user_message: str, chat_history: list) -> str:
    try:
        trimmed_history = trim_history(chat_history)
        prompt = build_prompt(user_message, trimmed_history)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS
            }
        )
        return response.text

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return FALLBACK_RESPONSE


def get_streaming_response(user_message: str, chat_history: list):
    try:
        trimmed_history = trim_history(chat_history)
        prompt = build_prompt(user_message, trimmed_history)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS
            },
            stream=True
        )
        for chunk in response:
            if hasattr(chunk, "text"):
                yield chunk.text

    except Exception as e:
        logger.error(f"Gemini Streaming Error: {e}")
        yield FALLBACK_RESPONSE