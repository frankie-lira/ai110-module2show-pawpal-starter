"""Pytest tests for the PawPal system."""

from pawpal_system import Owner, Pet, Task


def test_mark_complete_sets_completed_true():
    """Calling mark_complete() on a Task sets completed to True."""
    task = Task(name="Walk", duration=30, priority=1, category="exercise")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_task_count():
    """Adding a Task via add_task() increases the pet's task count by 1."""
    owner = Owner(name="Alex", available_time=60)
    pet = Pet(name="Rex", breed="Labrador", owner=owner)
    initial_count = len(pet.get_tasks())

    pet.add_task(Task(name="Feed", duration=10, priority=1, category="food"))

    assert len(pet.get_tasks()) == initial_count + 1
