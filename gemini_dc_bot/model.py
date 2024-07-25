import os

import google.generativeai as genai
from dotenv import load_dotenv

from logger import logger


# load .env
load_dotenv()

# set API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


class Model:
    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        self.model_name = model_name

        self.sys_instruction = """
            You are now a Discord chat bot in a primarily Traditional Chinese Discord Server.
            When responding to messages, you do not necessarily have to tag the person unless you want to emphasize something or need to notify someone for clarity.
            If you need to share a link, please directly paste the URL without using markdown syntax, for example, (URL)[URL] is not a good response.
            Do not use HTML or CSS syntax. If you want to share an image, please directly paste the URL.
            The message format you will receive will be: From: <user_id> in <channel_id> <content>
            Please respond to the content accordingly, considering the author and the channel.
            Use more Markdown syntax and emojis to make your responses more readable.
            If you need to tag someone, you can do so with <@user_id>, where user_id is a string of numbers.
            If you are unsure of someone's ID, do not attempt to tag anyone.
            """

        self.generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        self.model = self.create_model()
        self.chat = self.model.start_chat()

    def create_model(self) -> genai.GenerativeModel:
        return genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings=self.safety_settings,
            generation_config=self.generation_config,
            system_instruction=self.sys_instruction,
        )

    def reload_config(self):
        try:
            model = self.create_model()
        except:
            logger.error("Cannot create model")
            return
        self.model = model
        self.chat = self.model.start_chat()

    def set_model_name(self, name: str):
        if name not in [""]:
            logger.error(f'"{name}" is not a valid model name')
            return
        self.model_name = name
        self.reload_config()

    def set_system_instruction(self, instruction: str):
        self.sys_instruction = instruction
        self.reload_config()

    def set_temperature(self, t: float):
        if t < 0 or t > 1:
            logger.error(f"{t} is not a valid temperature.")
            return
        self.generation_config["temperature"] = t
        self.reload_config()

    def set_top_p(self, top_p: float):
        if top_p < 0 or top_p > 1:
            logger.error(f"{top_p} is not a valid Top P.")
            return
        self.generation_config["top_p"] = top_p
        self.reload_config()

    def set_top_k(self, top_k: int):
        if top_k <= 0:
            logger.error(f"{top_k} is not a valid Top K.")
            return
        self.generation_config["top_k"] = top_k
        self.reload_config()

    def set_max_output_tokens(self, max_len: int):
        if max_len <= 0:
            logger.error(f"{max_len} is not a valid max output tokens.")
            return
        self.generation_config["max_output_tokens"] = max_len
        self.reload_config()

    def send_message(self, message):
        try:
            response = self.chat.send_message(message)
            logger.info("Received response from Gemini.")
            return response.text
        except Exception as e:
            logger.error(f"Gemini Error:\n\t{e}")
            return "Please try again later..."
