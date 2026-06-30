from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional, Tuple
from datetime import date, timedelta, datetime


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    description: Optional[str] = None
    preferred_time: Optional[str] = None
    due_date: Optional[date] = None
    frequency: Optional[str] = None  # e.g. 'daily', 'weekly', None
    completed: bool = False
    pet_name: Optional[str] = None

    def summary(self) -> str:
        """Return a short human-readable description of the task."""
        parts = [f"{self.title} ({self.duration_minutes} min)", f"[priority: {self.priority}]"]
        if self.preferred_time:
            parts.append(f"@ {self.preferred_time}")
        if self.due_date:
            parts.append(f"on {self.due_date.isoformat()}")
        return " ".join(parts)

    def priority_score(self) -> int:
        """Return a numeric score for sorting based on priority."""
        ranking = {"low": 1, "medium": 2, "high": 3}
        return ranking.get(self.priority.lower(), 0)

    def mark_complete(self) -> Optional['Task']:
        """Mark the task as completed.

        If the task has a `frequency` (e.g. 'daily' or 'weekly'), create and
        return a new Task instance representing the next occurrence. Otherwise
        return None.
        """
        self.completed = True
        if not self.frequency:
            return None

        if self.frequency.lower() == "daily":
            delta = timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None

        # Create next-occurrence task with same metadata but reset completion
        next_due = (self.due_date or date.today()) + delta
        new_task = replace(self, completed=False, due_date=next_due)
        return new_task


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet, rejecting duplicate titles."""
        # Accept same title if it refers to a different due_date (recurring tasks)
        if any(existing.title == task.title and existing.due_date == task.due_date for existing in self.tasks):
            raise ValueError(f"Task with title '{task.title}' already exists for pet {self.name} on that date.")
        task.pet_name = task.pet_name or self.name
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task from this pet by title."""
        self.tasks = [task for task in self.tasks if task.title != title]

    def update_task(self, title: str, **kwargs) -> None:
        """Update task fields by title."""
        task = next((task for task in self.tasks if task.title == title), None)
        if task is None:
            raise ValueError(f"Task with title '{title}' not found for pet {self.name}.")
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

    def mark_task_complete(self, title: str) -> Optional[Task]:
        """Mark a task complete by title. If it creates a recurring next-task,
        add that new task and return it; otherwise return None."""
        task = next((task for task in self.tasks if task.title == title), None)
        if task is None:
            raise ValueError(f"Task with title '{title}' not found for pet {self.name}.")
        new_task = task.mark_complete()
        if new_task:
            # Add the next occurrence
            self.tasks.append(new_task)
            return new_task
        return None

    def list_tasks(self) -> List[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner, rejecting duplicate pet names."""
        if any(existing.name == pet.name for existing in self.pets):
            raise ValueError(f"Pet with name '{pet.name}' already exists for owner {self.name}.")
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet from the owner by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        return next((pet for pet in self.pets if pet.name == pet_name), None)

    def all_tasks(self, include_completed: bool = False) -> List[Task]:
        """Return all tasks for all pets, optionally filtering completed tasks."""
        tasks = [task for pet in self.pets for task in pet.tasks]
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        return tasks


class PawPalScheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def _time_key(self, task: Task) -> Tuple[date, int]:
        """Return a sort key for a task using due_date then preferred_time.

        preferred_time is expected in "HH:MM" format. If missing, it sorts
        earlier than tasks with a specified time on the same date.
        """
        d = task.due_date or date.min
        if task.preferred_time:
            try:
                dt = datetime.strptime(task.preferred_time, "%H:%M")
                minutes = dt.hour * 60 + dt.minute
            except Exception:
                minutes = 0
        else:
            minutes = -1
        return (d, minutes)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by due_date then preferred_time (HH:MM)."""
        return sorted(tasks, key=lambda t: self._time_key(t))

    def filter_tasks(self, tasks: List[Task], pet_name: Optional[str] = None, include_completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status.

        - `pet_name`: only tasks for that pet (if provided)
        - `include_completed`: if True include completed; if False exclude; if None ignore
        """
        results = tasks
        if pet_name:
            results = [t for t in results if t.pet_name == pet_name]
        if include_completed is True:
            pass
        elif include_completed is False:
            results = [t for t in results if not t.completed]
        return results

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Lightweight conflict detection: same due_date and same preferred_time.

        Returns a list of warning strings for groups of conflicting tasks.
        """
        groups: Dict[Tuple[Optional[date], Optional[str]], List[Task]] = {}
        for t in tasks:
            key = (t.due_date, t.preferred_time)
            groups.setdefault(key, []).append(t)

        warnings: List[str] = []
        for key, group in groups.items():
            if key[1] is None:
                continue
            if len(group) > 1:
                titles = ", ".join(f"{g.pet_name}:{g.title}" for g in group)
                d = key[0].isoformat() if key[0] else "unspecified date"
                warnings.append(f"Conflict on {d} at {key[1]}: {titles}")
        return warnings

    def get_all_tasks(self, include_completed: bool = False) -> List[Task]:
        """Retrieve all tasks from every pet belonging to the owner."""
        return self.owner.all_tasks(include_completed=include_completed)

    def generate_daily_plan(self, pet_name: Optional[str] = None, date: Optional[str] = None) -> List[Task]:
        """Generate a schedule of tasks for a single pet or all pets within the owner's available time."""
        # Interpret date param (ISO YYYY-MM-DD) or use today
        target_date = date and datetime.strptime(date, "%Y-%m-%d").date() or datetime.today().date()

        if pet_name:
            pet = self.owner.find_pet(pet_name)
            if pet is None:
                raise ValueError(f"Pet '{pet_name}' not found for owner {self.owner.name}.")
            tasks = [task for task in pet.tasks if not task.completed]
        else:
            tasks = self.get_all_tasks()

        # Only consider tasks for the target_date (or tasks without a due_date)
        tasks = [t for t in tasks if (t.due_date is None or t.due_date == target_date)]
        # Primary sort: priority (high->low), secondary: shorter duration first
        tasks = sorted(tasks, key=lambda task: (-task.priority_score(), task.duration_minutes))

        # After selecting by priority/duration, sort by preferred time for display
        tasks = self.sort_by_time(tasks)
        plan: List[Task] = []
        available = self.owner.available_minutes_per_day
        current_minutes = 0

        for task in tasks:
            if current_minutes + task.duration_minutes > available:
                continue
            plan.append(task)
            current_minutes += task.duration_minutes

        return plan
