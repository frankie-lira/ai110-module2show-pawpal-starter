"""PawPal system class skeletons generated from the UML diagram.

Defines the core domain model: Owner, Pet, Task, and Scheduler.
Method bodies are intentionally left unimplemented.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Task:
    """A single care task for a pet."""

    name: str
    duration: int
    priority: int  # priority 1 is highest; larger numbers are lower priority
    category: str
    completed: bool = False
    # Minutes since midnight (e.g. 8 * 60 == 8:00am). ``None`` means the task
    # is unscheduled in time and is ordered after all timed tasks.
    start_time: Optional[int] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    @property
    def end_time(self) -> Optional[int]:
        """Minutes since midnight when this task ends, or ``None`` if untimed."""
        if self.start_time is None:
            return None
        return self.start_time + self.duration


@dataclass
class Pet:
    """A pet owned by an Owner, with a list of associated tasks."""

    name: str
    breed: str
    owner: "Owner"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks associated with this pet."""
        return self.tasks


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
        self.pets.append(pet)
        pet.owner = self

    def get_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


class Scheduler:
    """Builds a care schedule for a pet within an available time budget."""

    def __init__(self, pet: Pet) -> None:
        self.pet = pet
        # Budget is derived from the owner so the two never drift apart.
        self.available_time = pet.owner.available_time
        # Holds the priority-sorted tasks produced by ``sort_by_priority`` so
        # ``filter_by_time`` can consume them without re-sorting.
        self._sorted: List[Task] = []

    def generate_schedule(self) -> List[Task]:
        """Generate an ordered schedule of tasks that fits the time budget."""
        self.sort_by_priority()
        return self.filter_by_time()

    def sort_by_priority(self) -> List[Task]:
        """Return the pet's tasks sorted by priority.

        Ties are broken by shorter duration first so quick wins get scheduled
        ahead of long tasks of equal priority.
        """
        self._sorted = sorted(
            self.pet.get_tasks(), key=lambda task: (task.priority, task.duration)
        )
        return self._sorted

    def sort_by_time(self) -> List[Task]:
        """Return the pet's tasks ordered chronologically by start time.

        Untimed tasks (``start_time is None``) are placed after all timed
        tasks, ordered among themselves by priority.
        """
        return sorted(
            self.pet.get_tasks(),
            key=lambda task: (
                task.start_time is None,
                task.start_time if task.start_time is not None else 0,
                task.priority,
            ),
        )

    def filter_by_completion(self, tasks: List[Task]) -> List[Task]:
        """Return only the tasks that are not yet completed."""
        return [task for task in tasks if not task.completed]

    def filter_by_time(self) -> List[Task]:
        """Return tasks that fit within the available time budget.

        NOTE: This must do a *cumulative* pass — accumulate each task's
        duration against a running total and stop once the budget is
        exhausted. Do NOT filter tasks independently (each task fitting on
        its own does not mean the set fits together). Expects the tasks to
        already be sorted by priority.

        Completed tasks are skipped entirely so they neither appear in the
        schedule nor consume the time budget.
        """
        scheduled: List[Task] = []
        remaining = self.available_time
        for task in self.filter_by_completion(self._sorted):
            if task.duration <= remaining:
                scheduled.append(task)
                remaining -= task.duration
        return scheduled

    def find_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pairs of timed tasks whose time ranges overlap.

        Only tasks with a ``start_time`` are considered. Tasks are sorted
        chronologically and each is compared against the previous one: an
        overlap exists when a task begins before the previous one ends.
        """
        timed = [task for task in self.pet.get_tasks() if task.start_time is not None]
        timed.sort(key=lambda task: task.start_time)

        conflicts: List[Tuple[Task, Task]] = []
        for prev, curr in zip(timed, timed[1:]):
            if curr.start_time < prev.end_time:
                conflicts.append((prev, curr))
        return conflicts
