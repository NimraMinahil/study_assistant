# Study Assistant (FastAPI + Gemini Tool Calling)

A FastAPI app that answers student questions about assignment deadlines using the Google Gemini API. The model uses tool calling: when a question is about deadlines, it calls a Python function (`get_next_deadline(course)`) and builds its answer from the returned data.

**Tech stack:** Python, FastAPI, Google Gemini API (tool calling), Uvicorn, python-dotenv

## How it works

1. The student sends a question to `POST /ask`.
2. Gemini receives the question and the description of the `get_next_deadline` tool.
3. If the question is about a deadline, Gemini calls the tool with the course name.
4. The tool returns the nearest upcoming deadline from the data in `deadlines.py`.
5. Gemini writes the final answer from that deadline.
6. The response contains the `answer` and `tool_calls` (the tool's input and output).

If the question is not about deadlines (for example, "What is photosynthesis?"), no tool is called and `tool_calls` is empty.

## Setup (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If `activate` fails with a "running scripts is disabled" error, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Or run `venv\Scripts\activate.bat` instead.

On Mac/Linux, activate with: `source venv/bin/activate`

## API key

1. Go to `aistudio.google.com` and create a key with **Get API key**.
2. In the project folder, create a file named `.env` (copy `.env.example` and rename it).
3. Add the following to `.env` (no spaces or quotes around the `=`):

```
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-3.5-flash-lite
```

`GEMINI_MODEL` is optional. If it is not set, the app uses `gemini-2.5-flash`. If a model name is outdated or you hit the usage limit, pick another available model from the AI Studio list.

Never share or upload your `.env` file. It contains your real API key.

## Run

```powershell
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` in your browser, click **POST /ask**, click **Try it out**, and enter:

```json
{"question": "When is my next Physics assignment due?"}
```

Example response:

```json
{
  "answer": "Your next Physics assignment, Lab Report 2, is due on January 12, 2027.",
  "tool_calls": [
    {
      "name": "get_next_deadline",
      "input": {"course": "Physics"},
      "output": {"found": true, "course": "Physics", "title": "Lab Report 2", "due_date": "2027-01-12", "days_left": 64}
    }
  ]
}
```

(`days_left` depends on today's date.)

## Test questions

- `When is my next Physics assignment due?`: with a course name
- `When is my next assignment due?`: no course, returns the nearest deadline overall
- `When is my Chemistry assignment due?`: course not in the list, returns "no upcoming deadlines"
- `What is photosynthesis?`: no tool call expected

## Files

- `main.py`: FastAPI app, `/ask` endpoint and Gemini tool calling
- `deadlines.py`: sample assignment data and the `get_next_deadline(course)` function
- `requirements.txt`: required packages
- `.env.example`: template for the `.env` file
- `.env`: your API key (create it yourself, do not share it)

## Notes

- `deadlines.py` contains sample (dummy) courses and dates. Edit the `ASSIGNMENTS` list to use your own data.
- Gemini's free tier has a daily request limit. Tool calling uses 2 requests per question, so if you see `429 RESOURCE_EXHAUSTED`, wait a while or change `GEMINI_MODEL`.
