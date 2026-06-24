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
    priority: int  # priority 1 is highest; larger numbers are lower priority
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
        """Add a pet to this owner's collection of pets.

        Sets ``pet.owner = self`` so the back-reference stays in sync with
        this owner's ``pets`` list (single source of truth).
        """
        ...

    def get_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        ...


class Scheduler:
    """Builds a care schedule for a pet within an available time budget."""

    def __init__(self, pet: Pet) -> None:
        self.pet = pet
        # Budget is derived from the owner so the two never drift apart.
        self.available_time = pet.owner.available_time

    def generate_schedule(self) -> List[Task]:
        """Generate an ordered schedule of tasks that fits the time budget."""
        ...

    def sort_by_priority(self) -> List[Task]:
        """Return the pet's tasks sorted by priority."""
        ...

    def filter_by_time(self) -> List[Task]:
        """Return tasks that fit within the available time budget.

        NOTE: This must do a *cumulative* pass — accumulate each task's
        duration against a running total and stop once the budget is
        exhausted. Do NOT filter tasks independently (each task fitting on
        its own does not mean the set fits together). Expects the tasks to
        already be sorted by priority.
        """
        ...
