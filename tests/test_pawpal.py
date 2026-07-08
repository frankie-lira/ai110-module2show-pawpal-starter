"""Pytest tests for the PawPal system."""

from pawpal_system import Owner, Pet, Task, Scheduler


def _pet_with_tasks(*tasks: Task, available_time: int = 120) -> Pet:
    """Build an Owner+Pet, attach the given tasks, and return the Pet."""
    owner = Owner(name="Alex", available_time=available_time)
    pet = Pet(name="Rex", breed="Labrador", owner=owner)
    owner.add_pet(pet)
    for task in tasks:
        pet.add_task(task)
    return pet


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


def test_sort_by_time_orders_timed_then_untimed():
    """sort_by_time() orders by start time and puts untimed tasks last."""
    late = Task(name="Play", duration=30, priority=3, category="play", start_time=18 * 60)
    early = Task(name="Walk", duration=45, priority=1, category="exercise", start_time=8 * 60)
    untimed = Task(name="Vet call", duration=5, priority=2, category="admin")
    pet = _pet_with_tasks(late, untimed, early)

    ordered = Scheduler(pet).sort_by_time()

    assert ordered == [early, late, untimed]


def test_filter_by_time_skips_completed_tasks():
    """Completed tasks neither appear in the schedule nor consume the budget."""
    done = Task(name="Feed", duration=10, priority=1, category="feeding")
    done.mark_complete()
    todo = Task(name="Walk", duration=30, priority=2, category="exercise")
    pet = _pet_with_tasks(done, todo, available_time=60)

    scheduler = Scheduler(pet)
    scheduled = scheduler.generate_schedule()

    assert scheduled == [todo]


def test_find_conflicts_detects_overlap():
    """find_conflicts() returns the pair of tasks whose ranges overlap."""
    walk = Task(name="Walk", duration=45, priority=1, category="exercise", start_time=8 * 60)
    feed = Task(name="Feed", duration=15, priority=2, category="feeding", start_time=8 * 60 + 30)
    pet = _pet_with_tasks(walk, feed)

    conflicts = Scheduler(pet).find_conflicts()

    assert conflicts == [(walk, feed)]


def test_find_conflicts_ignores_adjacent_and_untimed():
    """Back-to-back timed tasks and untimed tasks do not count as conflicts."""
    walk = Task(name="Walk", duration=30, priority=1, category="exercise", start_time=8 * 60)
    feed = Task(name="Feed", duration=15, priority=2, category="feeding", start_time=8 * 60 + 30)
    untimed = Task(name="Vet call", duration=5, priority=2, category="admin")
    pet = _pet_with_tasks(walk, feed, untimed)

    assert Scheduler(pet).find_conflicts() == []
