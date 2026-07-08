"""Demo driver for the PawPal system.

Creates an owner with a limited time budget, a couple of pets, several tasks
of varying duration, priority, and start time, then runs the Scheduler and
prints, for each pet:

  * the priority-based schedule that fits the time budget (completed tasks
    are skipped),
  * a chronological (start-time) view of the day, and
  * any conflicts where two timed tasks overlap.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def fmt_time(minutes: int) -> str:
    """Format minutes-since-midnight as HH:MM (24h)."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def main() -> None:
    # Owner with a 120-minute time budget for the day.
    owner = Owner("Alex", available_time=120)

    # At least two pets.
    rex = Pet(name="Rex", breed="Labrador", owner=owner)
    mittens = Pet(name="Mittens", breed="Tabby", owner=owner)
    owner.add_pet(rex)
    owner.add_pet(mittens)

    # Rex's tasks. The morning walk (08:00-08:45) and feed breakfast
    # (08:30-08:45) deliberately overlap to demonstrate conflict detection.
    rex.add_task(
        Task(name="Morning walk", duration=45, priority=1,
             category="exercise", start_time=8 * 60)
    )
    rex.add_task(
        Task(name="Feed breakfast", duration=15, priority=2,
             category="feeding", start_time=8 * 60 + 30)
    )
    rex.add_task(
        Task(name="Grooming", duration=60, priority=4,
             category="grooming", start_time=17 * 60)
    )

    # Mittens's tasks. "Feed" is already completed today, so it should be
    # skipped by the scheduler.
    feed = Task(name="Feed", duration=10, priority=1,
                category="feeding", start_time=9 * 60)
    feed.mark_complete()
    mittens.add_task(feed)
    mittens.add_task(
        Task(name="Clean litter box", duration=20, priority=2,
             category="cleaning", start_time=12 * 60)
    )
    mittens.add_task(
        Task(name="Play time", duration=30, priority=3,
             category="play", start_time=18 * 60)
    )

    print("Today's Schedule")
    print("=" * 40)
    print(f"Owner: {owner.name}  (available time: {owner.available_time} min)\n")

    for pet in owner.get_pets():
        scheduler = Scheduler(pet)
        scheduled_tasks = scheduler.generate_schedule()

        print(f"{pet.name} the {pet.breed}:")

        # Priority-based schedule that fits the budget.
        print("  Scheduled (by priority, within budget):")
        if not scheduled_tasks:
            print("    (no tasks fit the available time)")
        total = 0
        for task in scheduled_tasks:
            total += task.duration
            print(
                f"    - {task.name} "
                f"(priority {task.priority}, {task.duration} min, {task.category})"
            )
        print(f"    Total scheduled time: {total} min")

        # Chronological view of the whole day.
        print("  Timeline (by start time):")
        for task in scheduler.sort_by_time():
            when = fmt_time(task.start_time) if task.start_time is not None else "  --"
            status = " [done]" if task.completed else ""
            print(f"    {when}  {task.name} ({task.duration} min){status}")

        # Overlap detection.
        conflicts = scheduler.find_conflicts()
        if conflicts:
            print("  ⚠ Conflicts:")
            for prev, curr in conflicts:
                print(
                    f"    {prev.name} ({fmt_time(prev.start_time)}-"
                    f"{fmt_time(prev.end_time)}) overlaps "
                    f"{curr.name} ({fmt_time(curr.start_time)}-"
                    f"{fmt_time(curr.end_time)})"
                )
        print()


if __name__ == "__main__":
    main()
