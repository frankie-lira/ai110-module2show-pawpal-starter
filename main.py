"""Demo driver for the PawPal system.

Creates an owner with a limited time budget, a couple of pets, several tasks
of varying duration and priority, then runs the Scheduler and prints the
resulting schedule for each pet.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # Owner with a 120-minute time budget for the day.
    owner = Owner("Alex", available_time=120)

    # At least two pets.
    rex = Pet(name="Rex", breed="Labrador", owner=owner)
    mittens = Pet(name="Mittens", breed="Tabby", owner=owner)
    owner.add_pet(rex)
    owner.add_pet(mittens)

    # At least three tasks with different durations and priorities.
    rex.add_task(Task(name="Morning walk", duration=45, priority=1, category="exercise"))
    rex.add_task(Task(name="Feed breakfast", duration=15, priority=2, category="feeding"))
    rex.add_task(Task(name="Grooming", duration=60, priority=4, category="grooming"))

    mittens.add_task(Task(name="Feed", duration=10, priority=1, category="feeding"))
    mittens.add_task(Task(name="Clean litter box", duration=20, priority=2, category="cleaning"))
    mittens.add_task(Task(name="Play time", duration=30, priority=3, category="play"))

    print("Today's Schedule")
    print("=" * 40)
    print(f"Owner: {owner.name}  (available time: {owner.available_time} min)\n")

    for pet in owner.get_pets():
        scheduler = Scheduler(pet)
        scheduled_tasks = scheduler.generate_schedule()

        print(f"{pet.name} the {pet.breed}:")
        if not scheduled_tasks:
            print("  (no tasks fit the available time)")
        total = 0
        for task in scheduled_tasks:
            total += task.duration
            print(
                f"  - {task.name} "
                f"(priority {task.priority}, {task.duration} min, {task.category})"
            )
        print(f"  Total scheduled time: {total} min\n")


if __name__ == "__main__":
    main()
