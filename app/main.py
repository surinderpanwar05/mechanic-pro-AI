import os

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.ai_service import AIService


limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


ai = AIService()


class Question(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/api/ask")
@limiter.limit("20/minute")
def ask(
    request: Request,
    question: Question,
    x_api_key: str = Header(default="")
):

    if x_api_key != os.getenv("AI_API_ACCESS_KEY"):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    try:

        response = ai.ask(
            question.message
        )

        return {
            "success": True,
            "response": response
        }

    except Exception as e:

        print(
            f"AI ERROR: {type(e).__name__}: {e}",
            flush=True
        )

        raise HTTPException(
            status_code=500,
            detail="AI service error."
        )
