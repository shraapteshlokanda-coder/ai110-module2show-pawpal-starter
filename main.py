from pawpal_system import Owner, Pet, Task, PawPalScheduler


def format_schedule(tasks):
    if not tasks:
        return "No tasks scheduled for today."

    lines = ["Today's Schedule:"]
    total_minutes = 0
    for task in tasks:
        lines.append(f"- {task.pet_name}: {task.summary()}")
        total_minutes += task.duration_minutes
    lines.append(f"Total scheduled time: {total_minutes} minutes")
    return "\n".join(lines)


def main():
    owner = Owner(name="Jordan", available_minutes_per_day=120)

    dog = Pet(name="Mochi", species="dog", age=4)
    cat = Pet(name="Neko", species="cat", age=2)

    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", description="Walk around the park."))
    dog.add_task(Task(title="Dinner", duration_minutes=15, priority="medium", description="Feed kibble."))
    cat.add_task(Task(title="Play session", duration_minutes=20, priority="high", description="Laser pointer time."))
    cat.add_task(Task(title="Brush fur", duration_minutes=10, priority="low", description="Grooming."))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = PawPalScheduler(owner)
    plan = scheduler.generate_daily_plan()

    print(format_schedule(plan))


if __name__ == "__main__":
    main()
