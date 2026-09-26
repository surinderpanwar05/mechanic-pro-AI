from dotenv import load_dotenv
from app.ai_service import AIService

load_dotenv()

ai = AIService()

print(ai.ask(""))
print(ai.ask("What does P0420 mean?"))

