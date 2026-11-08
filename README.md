# Study Assistant (FastAPI + Gemini Tool Calling)

Student ka sawal (e.g. "When is my next assignment due?") leta hai. LLM (Google Gemini) zaroorat parne par
`get_next_deadline(course)` tool call karta hai aur tool ke returned deadline se jawab deta hai.

## Kaise kaam karta hai

1. Student `POST /ask` par sawal bhejta hai.
2. Gemini ko sawal aur `get_next_deadline` tool ki description milti hai.
3. Agar sawal deadline ke bare mein ho, to Gemini tool ko course ke saath call karta hai.
4. Tool `deadlines.py` ke data se sab se qareeb deadline wapas karta hai.
5. Gemini us deadline se final jawab banata hai.
6. Response mein `answer` aur `tool_calls` (tool ka input/output) wapas aate hain.

Agar sawal deadline ka na ho (e.g. "What is photosynthesis?"), to tool call nahi hota aur `tool_calls` khali aati hai.

## Setup (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Agar `activate` par "running scripts is disabled" ka error aaye:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Ya `venv\Scripts\activate.bat` chalayen.

Mac/Linux par activate ke liye: `source venv/bin/activate`

## API key

1. `aistudio.google.com` par jayen, **Get API key** se key banayen.
2. Project folder mein `.env` naam ki file banayen (`.env.example` ki copy bana kar rename karein).
3. `.env` mein likhein (barabar ke ird gird space ya quotes nahi):

```
GEMINI_API_KEY=aapki-key
GEMINI_MODEL=gemini-3.8-flash
```

`GEMINI_MODEL` optional hai. Agar model ka naam purana ho ya limit khatam ho jaye, to AI Studio ki list se koi dusra available model likh dein.

`.env` ko kabhi share ya upload na karein, is mein aapki asli key hoti hai.

## Chalayen

```powershell
uvicorn main:app --reload
```

Browser mein `http://127.0.0.1:8000/docs` kholein, **POST /ask** par click karein, **Try it out** dabayen aur likhein:

```json
{"question": "When is my next Physics assignment due?"}
```

Example response:

```json
{
  "answer": "Your next Physics assignment, Lab Report 2, is due on November 12, 2026.",
  "tool_calls": [
    {
      "name": "get_next_deadline",
      "input": {"course": "Physics"},
      "output": {"found": true, "course": "Physics", "title": "Lab Report 2", "due_date": "2026-11-12", "days_left": 4}
    }
  ]
}
```

## Test sawal

- `When is my next Physics assignment due?` : course ke saath
- `When is my next assignment due?` : bina course ke, sab se qareeb deadline
- `When is my Chemistry assignment due?` : course list mein nahi, "no upcoming deadlines"
- `What is photosynthesis?` : tool call nahi hona chahiye

## Files

- `main.py` - FastAPI app, `/ask` endpoint, Gemini tool calling
- `deadlines.py` - sample assignment data aur `get_next_deadline(course)` function
- `requirements.txt` - zaroori packages
- `.env` - API key (khud banayen, share na karein)

## Notes

- `deadlines.py` mein sample (dummy) courses aur dates hain. Apne data ke liye `ASSIGNMENTS` list badal dein.
- Gemini ki free tier mein rozana requests ki limit hoti hai. Tool calling mein ek sawal par 2 requests lagti hain, is liye `429 RESOURCE_EXHAUSTED` aaye to thori der intezar karein ya `GEMINI_MODEL` badal dein.
