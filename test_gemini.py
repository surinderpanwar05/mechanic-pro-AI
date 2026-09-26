from dotenv import load_dotenv
from app.providers.gemini import GeminiProvider

load_dotenv()

ai = GeminiProvider()

response = ai.chat("What is a P0420 fault code?")
print(response)
