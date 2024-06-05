import os

import google.generativeai as genai
from dotenv import load_dotenv

from logger import logger


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


MODEL_NAME = "gemini-1.5-flash"
SYS_INSTRUCTION = """
    你現在是一個 Discord 聊天機器人，本 Discord Server 主要使用繁體中文。
    """

generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=SYS_INSTRUCTION,
)

chat = model.start_chat()


def send_message(message):
    logger.info("Send message to Gemini.")
    try:
        response = chat.send_message(message)
        logger.info(f"From Gemini\n\b{response.text}")
        return response.text
    except Exception as e:
        logger.error(f"{e}")
        return "Please try again later..."
