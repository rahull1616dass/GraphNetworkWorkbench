import openai

from config import Settings


settings = Settings()
openai.api_key = settings.chatgpt_api_key
