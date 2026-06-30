from pawpal_system import Owner, Pet, Task, PawPalScheduler
from datetime import date


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

    # Add tasks out of chronological order, include preferred_time and due_date
    today = date.today()
    dog.add_task(Task(title="Dinner", duration_minutes=15, priority="medium", description="Feed kibble.", preferred_time="19:00", due_date=today))
    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", description="Walk around the park.", preferred_time="08:00", due_date=today))
    cat.add_task(Task(title="Brush fur", duration_minutes=10, priority="low", description="Grooming.", preferred_time="08:00", due_date=today))
    cat.add_task(Task(title="Play session", duration_minutes=20, priority="high", description="Laser pointer time.", preferred_time="09:00", due_date=today, frequency="daily"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = PawPalScheduler(owner)
    # Show unsorted tasks
    print("All tasks (unsorted):")
    for t in owner.all_tasks():
        print("-", t.summary())

    # Detect conflicts (two tasks at 08:00)
    conflicts = scheduler.detect_conflicts(owner.all_tasks())
    if conflicts:
        print("\nConflicts detected:")
        for c in conflicts:
            print("-", c)

    # Generate today's plan (it will sort by priority -> duration, then by time)
    plan = scheduler.generate_daily_plan()
    print("\n", format_schedule(plan))

    # Mark a recurring task complete and show that a new occurrence is added
    print("\nMarking 'Play session' complete for Neko (recurring daily)")
    new_task = cat.mark_task_complete("Play session")
    if new_task:
        print("New recurring task created for:", new_task.due_date)

    # Show tasks after marking complete
    print("\nTasks after completing recurring task:")
    for t in owner.all_tasks(include_completed=True):
        print("-", t.summary(), "- completed:" , t.completed)


if __name__ == "__main__":
    main()
