"""Dummy deadline data + the tool function the LLM can call."""
from datetime import date

# Apni asli courses/assignments yahan daal dein (ya database se load karein).
ASSIGNMENTS = [
    {"course": "Mathematics", "title": "Assignment 3 - Calculus", "due": "2026-11-10"},
    {"course": "Mathematics", "title": "Assignment 4 - Integration", "due": "2026-11-24"},
    {"course": "Physics", "title": "Lab Report 2", "due": "2026-11-12"},
    {"course": "Computer Science", "title": "Project Milestone 1", "due": "2026-11-15"},
    {"course": "Computer Science", "title": "Assignment 5 - Algorithms", "due": "2026-11-29"},
    {"course": "English", "title": "Essay Draft", "due": "2026-11-20"},
]


def get_next_deadline(course: str | None = None) -> dict:
    """Return the nearest upcoming deadline (optionally for one course)."""
    today = date.today()
    items = []
    for a in ASSIGNMENTS:
        due = date.fromisoformat(a["due"])
        if due < today:
            continue
        if course and course.strip().lower() not in a["course"].lower():
            continue
        items.append((due, a))

    if not items:
        where = f" for '{course}'" if course else ""
        return {"found": False, "message": f"No upcoming deadlines found{where}."}

    due, a = min(items, key=lambda x: x[0])
    return {
        "found": True,
        "course": a["course"],
        "title": a["title"],
        "due_date": a["due"],
        "days_left": (due - today).days,
    }
