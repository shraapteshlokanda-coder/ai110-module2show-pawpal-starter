import streamlit as st
from pawpal_system import Owner, Pet, Task, PawPalScheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
available_minutes = st.number_input("Available minutes per day", min_value=1, max_value=1440, value=120)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=int(available_minutes))

# Keep owner name and available minutes in sync with inputs
st.session_state.owner.name = owner_name
st.session_state.owner.available_minutes_per_day = int(available_minutes)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Add pet"):
        try:
            new_pet = Pet(name=pet_name, species=species)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added pet {pet_name}.")
        except ValueError as e:
            st.error(str(e))
with col_b:
    if st.button("Add task"):
        pet = st.session_state.owner.find_pet(pet_name)
        if pet is None:
            st.error(f"Pet '{pet_name}' not found. Add the pet first.")
        else:
            try:
                task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
                pet.add_task(task)
                st.success(f"Added task '{task_title}' to {pet_name}.")
            except ValueError as e:
                st.error(str(e))

# Display current pets and their tasks
owner = st.session_state.owner
if owner.pets:
    for pet in owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species})")
        if pet.tasks:
            for t in pet.tasks:
                st.write(f"- {t.summary()} {'(completed)' if t.completed else ''}")
        else:
            st.write("- No tasks")
else:
    st.info("No pets yet. Add one using the 'Add pet' button.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

# Scheduling controls
col_date, col_pet, col_show = st.columns(3)
with col_date:
    selected_date = st.date_input("Schedule date", value=None)
    # If user didn't pick, use today
    if selected_date is None:
        from datetime import date as _d
        selected_date = _d.today()
with col_pet:
    pet_options = ["All"] + [p.name for p in owner.pets]
    pet_filter = st.selectbox("Pet filter", pet_options)
with col_show:
    include_completed = st.checkbox("Include completed", value=False)

scheduler = PawPalScheduler(owner)

if st.button("Generate schedule"):
    # Gather tasks according to filters
    all_tasks = owner.all_tasks(include_completed=include_completed)

    # Detect conflicts and show warnings
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for c in conflicts:
            st.warning(c)

    # Optionally filter by pet
    pet_name = None if pet_filter == "All" else pet_filter

    # Generate plan for the selected date
    plan = scheduler.generate_daily_plan(pet_name=pet_name, date=selected_date.isoformat())

    if not plan:
        st.info("No tasks scheduled — either none exist or they don't fit available time.")
    else:
        st.subheader("Today's Plan")
        # Build a table-friendly list of dicts
        rows = []
        for t in plan:
            rows.append({
                "pet": t.pet_name,
                "title": t.title,
                "duration": t.duration_minutes,
                "priority": t.priority,
                "time": t.preferred_time or "-",
                "date": t.due_date.isoformat() if t.due_date else "-",
                "completed": t.completed,
            })
        st.table(rows)

        st.success(f"Generated {len(plan)} tasks for {selected_date.isoformat()}.")
