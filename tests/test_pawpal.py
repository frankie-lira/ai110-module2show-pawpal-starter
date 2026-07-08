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


# --- Sorting correctness ---------------------------------------------------


def test_sort_by_priority_breaks_ties_by_shorter_duration():
    """Equal priority: the shorter task is scheduled first."""
    long_task = Task(name="Groom", duration=40, priority=2, category="grooming")
    short_task = Task(name="Feed", duration=10, priority=2, category="feeding")
    pet = _pet_with_tasks(long_task, short_task)

    assert Scheduler(pet).sort_by_priority() == [short_task, long_task]


def test_sort_by_priority_is_stable_on_full_ties():
    """Equal priority and equal duration preserve insertion order."""
    first = Task(name="Feed A", duration=10, priority=1, category="feeding")
    second = Task(name="Feed B", duration=10, priority=1, category="feeding")
    pet = _pet_with_tasks(first, second)

    assert Scheduler(pet).sort_by_priority() == [first, second]


def test_sort_by_time_places_midnight_before_untimed():
    """A real start_time of 0 (midnight) sorts ahead of untimed tasks."""
    midnight = Task(name="Med", duration=5, priority=3, category="meds", start_time=0)
    untimed = Task(name="Vet call", duration=5, priority=1, category="admin")
    pet = _pet_with_tasks(untimed, midnight)

    assert Scheduler(pet).sort_by_time() == [midnight, untimed]


def test_sort_by_time_orders_untimed_among_themselves_by_priority():
    """Untimed tasks trail timed ones and sort by priority among themselves."""
    timed = Task(name="Walk", duration=30, priority=3, category="exercise", start_time=8 * 60)
    low = Task(name="Bath", duration=20, priority=5, category="grooming")
    high = Task(name="Pill", duration=2, priority=1, category="meds")
    pet = _pet_with_tasks(low, timed, high)

    assert Scheduler(pet).sort_by_time() == [timed, high, low]


def test_sorts_handle_empty_task_list():
    """Both sorts return an empty list when the pet has no tasks."""
    pet = _pet_with_tasks()
    scheduler = Scheduler(pet)

    assert scheduler.sort_by_priority() == []
    assert scheduler.sort_by_time() == []


# --- Conflict detection: identical start times -----------------------------


def test_find_conflicts_detects_identical_start_times():
    """Two tasks beginning at the same minute overlap and are reported."""
    walk = Task(name="Walk", duration=30, priority=1, category="exercise", start_time=8 * 60)
    feed = Task(name="Feed", duration=15, priority=2, category="feeding", start_time=8 * 60)
    pet = _pet_with_tasks(walk, feed)

    conflicts = Scheduler(pet).find_conflicts()

    assert len(conflicts) == 1
    assert walk in conflicts[0] and feed in conflicts[0]


def test_find_conflicts_zero_duration_at_same_start_conflicts():
    """A zero-duration task sharing a start time still counts as an overlap."""
    marker = Task(name="Note", duration=0, priority=2, category="admin", start_time=9 * 60)
    walk = Task(name="Walk", duration=30, priority=1, category="exercise", start_time=9 * 60)
    pet = _pet_with_tasks(walk, marker)

    conflicts = Scheduler(pet).find_conflicts()

    assert len(conflicts) == 1
    assert walk in conflicts[0] and marker in conflicts[0]


# --- Time budget filtering -------------------------------------------------


def test_filter_by_time_skips_overflow_but_keeps_later_fitting_task():
    """A task too big for the remaining budget is skipped; a smaller later one still fits."""
    big = Task(name="Walk", duration=50, priority=1, category="exercise")
    over = Task(name="Groom", duration=30, priority=2, category="grooming")
    small = Task(name="Feed", duration=10, priority=3, category="feeding")
    pet = _pet_with_tasks(big, over, small, available_time=60)

    scheduled = Scheduler(pet).generate_schedule()

    assert scheduled == [big, small]


def test_filter_by_time_includes_exact_fit():
    """A task whose duration exactly equals the remaining budget is included."""
    task = Task(name="Walk", duration=60, priority=1, category="exercise")
    pet = _pet_with_tasks(task, available_time=60)

    assert Scheduler(pet).generate_schedule() == [task]


def test_filter_by_time_zero_budget_schedules_nothing():
    """With no available time, no task is scheduled."""
    task = Task(name="Walk", duration=10, priority=1, category="exercise")
    pet = _pet_with_tasks(task, available_time=0)

    assert Scheduler(pet).generate_schedule() == []


def test_filter_by_time_completed_task_frees_budget_for_later_task():
    """A completed task consumes no budget, leaving room for a task that would not otherwise fit."""
    done = Task(name="Groom", duration=40, priority=1, category="grooming")
    done.mark_complete()
    todo = Task(name="Walk", duration=50, priority=2, category="exercise")
    pet = _pet_with_tasks(done, todo, available_time=60)

    assert Scheduler(pet).generate_schedule() == [todo]
