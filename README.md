# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule:
- Neko: Play session (20 min) [priority: high]
- Mochi: Morning walk (30 min) [priority: high]
- Mochi: Dinner (15 min) [priority: medium]
- Neko: Brush fur (10 min) [priority: low]
Total scheduled time: 75 minutes

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

### Testing PawPal+

Run the automated tests that verify sorting, recurring tasks, and conflict detection:

```bash
python -m pytest
```

Sample successful test output from my run:

```text
.....                                                                    [100%]
5 passed in 0.01s
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — Core behaviors are covered (sorting, recurrence, conflict detection); more edge-case and stress tests could further raise confidence.

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `PawPalScheduler.sort_by_time()` plus priority-based selection in `generate_daily_plan()` | Primary selection by priority/duration; displayed ordered by time (HH:MM). |
| Filtering | `PawPalScheduler.filter_tasks()` | Filter by `pet_name` and `include_completed` flags. |
| Conflict handling | `PawPalScheduler.detect_conflicts()` | Lightweight detection of tasks sharing the same date and time; returns warnings. |
| Recurring tasks | `Task.frequency` + `Task.mark_complete()` + `Pet.mark_task_complete()` | When a recurring task is completed, a new instance for the next occurrence is created automatically. |

## 📸 Demo Walkthrough

Follow these steps to try the app locally and see the scheduler behaviors:

1. Start the Streamlit UI:
2. Add an owner name, then add a pet using the "Add pet" button.
3. Use the task inputs to add tasks for your pet(s). You can set a `preferred_time` and (optionally) a `due_date` if you modify the inputs to include them — the scheduler will prefer tasks by time and date.
4. In the "Build Schedule" area choose a date and a pet filter (or "All"). Click "Generate schedule" to run the scheduler.
	- If two tasks share the same `preferred_time` and `due_date`, the UI displays a clear warning using `st.warning()`.
	- The schedule table shows tasks ordered by priority and time, with columns for pet, title, duration, priority, time, date, and completion state.
5. Mark a recurring task complete  and the system will automatically create the next occurrence for the following day or week depending on the task `frequency`.

Sample Output:
All tasks (unsorted):
- Dinner (15 min) [priority: medium] @ 19:00 on 2026-06-30
- Morning walk (30 min) [priority: high] @ 08:00 on 2026-06-30
- Brush fur (10 min) [priority: low] @ 08:00 on 2026-06-30
- Play session (20 min) [priority: high] @ 09:00 on 2026-06-30

Conflicts detected:
- Conflict on 2026-06-30 at 08:00: Mochi:Morning walk, Neko:Brush fur

 Today's Schedule:
- Mochi: Morning walk (30 min) [priority: high] @ 08:00 on 2026-06-30
- Neko: Play session (20 min) [priority: high] @ 09:00 on 2026-06-30
Total scheduled time: 50 minutes
```


