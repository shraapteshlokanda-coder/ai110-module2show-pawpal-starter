from pawpal_system import Pet, Task
from pawpal_system import Owner, PawPalScheduler
from datetime import date, timedelta


def test_mark_complete_changes_status():
    task = Task(title="Feed", duration_minutes=10, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    original_count = len(pet.tasks)

    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium"))

    assert len(pet.tasks) == original_count + 1


def test_sort_by_time_orders_tasks_chronologically():
    owner = Owner(name="Jordan", available_minutes_per_day=120)
    scheduler = PawPalScheduler(owner)
    today = date.today()
    t1 = Task(title="A", duration_minutes=10, priority="low", preferred_time="09:30", due_date=today)
    t2 = Task(title="B", duration_minutes=10, priority="low", preferred_time="08:15", due_date=today)
    s = scheduler.sort_by_time([t1, t2])
    assert s[0].title == "B" and s[1].title == "A"


def test_recurring_task_creates_next_occurrence():
    pet = Pet(name="Neko", species="cat")
    today = date.today()
    pet.add_task(Task(title="Play", duration_minutes=15, priority="high", preferred_time="10:00", due_date=today, frequency="daily"))
    new_task = pet.mark_task_complete("Play")
    assert new_task is not None
    assert new_task.due_date == today + timedelta(days=1)
    # original task marked completed
    orig = next(t for t in pet.tasks if t.title == "Play" and t.due_date == today)
    assert orig.completed is True


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(name="Jordan", available_minutes_per_day=120)
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Neko", species="cat")
    today = date.today()
    dog.add_task(Task(title="Walk", duration_minutes=30, priority="high", preferred_time="08:00", due_date=today))
    cat.add_task(Task(title="Feed", duration_minutes=10, priority="medium", preferred_time="08:00", due_date=today))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = PawPalScheduler(owner)
    warnings = scheduler.detect_conflicts(owner.all_tasks())
    assert len(warnings) >= 1
