import os

import google.generativeai as genai
from dotenv import load_dotenv

from logger import logger


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


MODEL_NAME = "gemini-1.5-flash"
SYS_INSTRUCTION = """
    你現在是一個 Discord 聊天機器人叫做「聰明BOT」，本 Discord Server 主要使用繁體中文。
    回應對方的訊息時，不一定要 tag 對方，除非你想增強語氣，或是語意上要通知別人。
    如果要分享連結，請直接貼上 URL，不要使用 markdown 語法，例如 [URL](URL) 是一個不好的回覆。
    請勿使用 HTML 或 CSS 語法，若要分享圖片，請直接貼上 URL。
    你收到的訊息格式將為: From: <user_id> in <channel_id> <content>
    請針對 content 做回覆。並同時考慮訊息的作者和頻道。
    多使用 Markdown 語法和 emoji 讓回應更好閱讀。
    如要 tag 其他人，可以用 <@user_id> 達成，其中 user_id 是一連串的數字。
    在不確定其他人 ID 的情況下，請勿嘗試 tag 任何人。
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
    try:
        response = chat.send_message(message)
        logger.info("Received response from Gemini.")
        return response.text
    except Exception as e:
        logger.error(f"{e}")
        return "Please try again later..."
