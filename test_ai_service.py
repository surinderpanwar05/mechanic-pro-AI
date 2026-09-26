from dotenv import load_dotenv
from app.ai_service import AIService

load_dotenv()

ai = AIService()

response = ai.ask("What does P0420 mean in a vehicle?")

print(response)
