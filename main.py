"""FastAPI Study Assistant with LLM tool calling (Google Gemini)."""
import os
from datetime import date
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel

from deadlines import get_next_deadline as _get_next_deadline

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Study Assistant", version="1.0")

SYSTEM = (
    "You are a friendly study assistant. Today's date is {today}. "
    "For questions about assignment deadlines, call get_next_deadline and answer "
    "ONLY using the data it returns. For other study questions, answer normally and briefly."
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    tool_calls: list[dict]


@app.get("/")
def health():
    return {"status": "ok", "docs": "/docs"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    used_tools: list[dict] = []

    # Tool the model can call. Gemini reads the name, type hints and docstring.
    def get_next_deadline(course: Optional[str] = None) -> dict:
        """Get the next upcoming assignment deadline for a student.

        Use this whenever the student asks about due dates or deadlines.

        Args:
            course: Course name, e.g. 'Mathematics'. Leave empty if the student did not name a course.
        """
        output = _get_next_deadline(course)
        used_tools.append({"name": "get_next_deadline", "input": {"course": course}, "output": output})
        return output

    try:
        # The SDK runs the tool call and sends the result back to the model automatically.
        resp = client.models.generate_content(
            model=MODEL,
            contents=req.question,
                         config=types.GenerateContentConfig(
                system_instruction=SYSTEM.format(today=date.today().isoformat()),
                tools=[get_next_deadline],
            ),
        )
        return AskResponse(answer=resp.text or "", tool_calls=used_tools)
    except Exception as e:
        raise HTTPException(502, f"LLM error: {e}")
