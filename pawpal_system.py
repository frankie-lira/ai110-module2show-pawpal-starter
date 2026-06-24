"""PawPal system class skeletons generated from the UML diagram.

Defines the core domain model: Owner, Pet, Task, and Scheduler.
Method bodies are intentionally left unimplemented.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single care task for a pet."""

    name: str
    duration: int
    priority: int
    category: str


@dataclass
class Pet:
    """A pet owned by an Owner, with a list of associated tasks."""

    name: str
    breed: str
    owner: "Owner"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        ...

    def get_tasks(self) -> List[Task]:
        """Return all tasks associated with this pet."""
        ...


class Owner:
    """A pet owner with a limited amount of available time."""

    def __init__(self, name: str, available_time: int) -> None:
        self.name = name
        self.available_time = available_time
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's collection of pets."""
        ...

    def get_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        ...


class Scheduler:
    """Builds a care schedule for a pet within an available time budget."""

    def __init__(self, pet: Pet, available_time: int) -> None:
        self.pet = pet
        self.available_time = available_time

    def generate_schedule(self) -> List[Task]:
        """Generate an ordered schedule of tasks that fits the time budget."""
        ...

    def sort_by_priority(self) -> List[Task]:
        """Return the pet's tasks sorted by priority."""
        ...

    def filter_by_time(self) -> List[Task]:
        """Return tasks that fit within the available time budget."""
        ...
