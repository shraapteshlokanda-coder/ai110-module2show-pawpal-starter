from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    description: Optional[str] = None
    preferred_time: Optional[str] = None
    completed: bool = False
    pet_name: Optional[str] = None

    def summary(self) -> str:
        """Return a short human-readable description of the task."""
        return f"{self.title} ({self.duration_minutes} min) [priority: {self.priority}]"

    def priority_score(self) -> int:
        """Return a numeric score for sorting based on priority."""
        ranking = {"low": 1, "medium": 2, "high": 3}
        return ranking.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet, rejecting duplicate titles."""
        if any(existing.title == task.title for existing in self.tasks):
            raise ValueError(f"Task with title '{task.title}' already exists for pet {self.name}.")
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

    def get_all_tasks(self, include_completed: bool = False) -> List[Task]:
        """Retrieve all tasks from every pet belonging to the owner."""
        return self.owner.all_tasks(include_completed=include_completed)

    def generate_daily_plan(self, pet_name: Optional[str] = None, date: Optional[str] = None) -> List[Task]:
        """Generate a schedule of tasks for a single pet or all pets within the owner's available time."""
        if pet_name:
            pet = self.owner.find_pet(pet_name)
            if pet is None:
                raise ValueError(f"Pet '{pet_name}' not found for owner {self.owner.name}.")
            tasks = [task for task in pet.tasks if not task.completed]
        else:
            tasks = self.get_all_tasks()

        tasks = sorted(tasks, key=lambda task: (-task.priority_score(), task.duration_minutes))
        plan: List[Task] = []
        available = self.owner.available_minutes_per_day
        current_minutes = 0

        for task in tasks:
            if current_minutes + task.duration_minutes > available:
                continue
            plan.append(task)
            current_minutes += task.duration_minutes

        return plan
