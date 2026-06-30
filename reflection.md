# PawPal+ Project Reflection

## 1. System Design
Three core actions a user should be able to perform:
- Add a pet and owner profile so the system knows who is responsible for care.
- Add or edit pet care tasks with duration and priority so the schedule can reflect real needs.
- Generate and view a daily care plan that orders tasks based on available time and priority.

**a. Initial design**
I designed four main classes:
- `Owner`: stores owner information, available daily time, preferences, and pets.
- `Pet`: stores pet details and a list of associated care tasks.
- `Task`: stores task metadata such as title, duration, priority, preferred time, due date, frequency, and completion state.
- `PawPalScheduler`: generates a daily plan for a pet and explains why tasks were chosen.

**b. Design changes**

- The model stayed focused on the four classes, but I iteratively added attributes (`due_date`, `frequency`) and behaviors (`mark_task_complete`, `detect_conflicts`, `sort_by_time`) as needs arose while implementing scheduling and recurrence.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently considers these constraints and priorities:

- Time budget: `Owner.available_minutes_per_day` is the hard cap used when building a daily plan.
- Task priority: tasks are ranked by `priority` (high → medium → low) via `Task.priority_score()` and used as the primary selector.
- Duration: as a tie-breaker shorter tasks are preferred to increase the number of completed items.
- Preferred time / due date: tasks with a `due_date` and `preferred_time` are filtered for the target date and ordered for display.

These constraints were chosen to provide a pragmatic, easy-to-explain ordering: respect important tasks first while maximizing what fits into the owner's available time.

**b. Tradeoffs**

One tradeoff: the scheduler detects conflicts only when tasks have the exact same `preferred_time` and `due_date`, rather than checking for overlapping time intervals. This simplifies the implementation and keeps conflict detection lightweight and fast, but it can miss overlaps where one task runs into another (for example, a 30-minute task at 08:30 overlapping a 15-minute task at 08:45). For the scope of this project — a simple daily planner for busy owners — exact-time matching provides useful warnings without adding scheduling complexity (slot management, interval math, or calendar integration). If needed, the next iteration can add interval-based overlap checks.

Additional tradeoffs:

- Simplicity over completeness: the plan uses priority and duration heuristics rather than solving a full bin-packing or calendar allocation problem. This keeps the scheduler understandable and fast but can miss optimal combinations in tight schedules.
- Lightweight conflict detection: exact-time matching provides clear, actionable warnings without adding interval math or a timeslot model. It intentionally errs on the side of non-blocking UX.

---

## 3. AI Collaboration

**a. How you used AI**

I used the AI coding assistant in several, distinct ways:

- Design brainstorming: asked for candidate scheduling heuristics (priority-first, shortest-first, time-window aware) and pros/cons for each.
- Implementation help: requested example implementations for sorting by `HH:MM` using `lambda` keys, `timedelta` usage for recurring tasks, and lightweight conflict detection approaches.
- Test generation: asked the assistant to suggest unit tests covering sorting, recurrence, and conflict detection edge cases.

Prompts that worked best were specific and example-driven, e.g. "How do I sort a list of tasks by a 'HH:MM' string time? Show code using sorted(..., key=...)."

**b. Judgment and verification**

One AI suggestion proposed automatically resolving conflicts by shifting lower-priority tasks to the next available slot. I rejected that for now because it implicitly requires a timeslot model (start/end times) and could surprise users by mutating their intent. Instead I implemented a lightweight warning system and documented the tradeoff — this felt safer and more predictable.

I verified behaviors by writing focused unit tests (`tests/test_pawpal.py`) and running them locally. When the tests passed, I manually exercised the CLI/demo (`main.py`) and the Streamlit UI to confirm the end-to-end experience.

**c. Organizing chat sessions**

Keeping separate, focused chat sessions for design, implementation, and testing helped contain context and reduce confusion. For example, design prompts explored algorithm choices, implementation chats produced specific code snippets, and a testing chat helped generate unit-test templates. This separation made it easier to validate each phase independently.

---

## 4. Testing and Verification

**a. What you tested**

I wrote tests for these core behaviors:

- Sorting correctness: `PawPalScheduler.sort_by_time()` orders tasks with `preferred_time` correctly.
- Recurrence: completing a daily task creates a next-day occurrence via `Task.mark_complete()` and `Pet.mark_task_complete()`.
- Conflict detection: `PawPalScheduler.detect_conflicts()` returns warnings when two tasks share the same `due_date` and `preferred_time`.

These tests ensure the scheduler's most important user-facing guarantees work reliably.

**b. Confidence**

I am moderately confident (4/5). The core behaviors are covered by unit tests and quick manual verification. Next tests to add:
- Interval overlap detection (not just exact-time matches).
- Timezone handling if dates/times come from an external calendar.
- Stress tests with many tasks and tight time budgets to validate heuristic behavior.

---

## 5. Reflection

**a. What went well**

The clear separation between domain model (`Owner`/`Pet`/`Task`) and scheduler allowed incremental improvements without breaking the UI. Writing tests early helped catch API mismatches quickly.

**b. What you would improve**

I would implement a simple timeslot allocator so tasks have explicit start/end times; that would enable robust overlap detection and automatic rescheduling suggestions. I would also add persistence (e.g., JSON or a small DB) so the Streamlit app state survives full restarts.

**c. Key takeaway**

AI is a powerful accelerator for pattern-level tasks (sorting snippets, timedelta code, test templates). However, human judgment is required to keep UX predictable — I chose warnings over automatic conflict resolution to avoid hidden behavior. Organizing work into focused chat sessions (design, implementation, testing) made it easier to keep context and validate outputs incrementally.
