import os
from dotenv import load_dotenv

load_dotenv("/var/www/mechanic-ai/.env")

class ProviderConfig:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "gemini").lower()
        self.api_key = os.getenv("AI_API_KEY")
        self.model = os.getenv("AI_MODEL")

    def validate(self):
        if not self.api_key:
            raise ValueError("AI_API_KEY is not configured.")

        if not self.model:
            raise ValueError("AI_MODEL is not configured.")
