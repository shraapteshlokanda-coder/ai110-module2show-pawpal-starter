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

    def summary(self) -> str:
        raise NotImplementedError

    def priority_score(self) -> int:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, title: str) -> None:
        raise NotImplementedError

    def update_task(self, title: str, **kwargs) -> None:
        raise NotImplementedError

    def list_tasks(self) -> List[Task]:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def remove_pet(self, pet_name: str) -> None:
        raise NotImplementedError

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        raise NotImplementedError


class PawPalScheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_daily_plan(self, pet_name: str, date: Optional[str] = None) -> List[Task]:
        raise NotImplementedError

    def explain_plan(self, tasks: List[Task]) -> str:
        raise NotImplementedError
