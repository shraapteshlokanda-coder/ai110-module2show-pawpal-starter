from pawpal_system import Pet, Task


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
