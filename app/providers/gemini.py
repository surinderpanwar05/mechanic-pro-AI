from google import genai
from app.providers.base import AIProvider
from app.providers.config import ProviderConfig

class GeminiProvider(AIProvider):
    def __init__(self):
        config = ProviderConfig()
        config.validate()

        self.client = genai.Client(api_key=config.api_key)
        self.model = config.model

    def chat(self, message):
        interaction = self.client.interactions.create(
            model=self.model,
            input=message,
            system_instruction="You are Mechanic Pro, a professional automotive assistant. Answer clearly and briefly. Give practical automotive information. Do not provide unnecessary information unless requested."
        )

        return interaction.output_text

    def classify(self, message, instruction):
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{instruction}\n\nUser question:\n{message}"
        )

        return response.text.strip()
