import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Maps a task category to a representative emoji for the schedule display.
CATEGORY_EMOJI = {
    "exercise": "🚶",
    "feeding": "🍽️",
    "meds": "💊",
    "grooming": "✂️",
    "play": "🎾",
    "cleaning": "🧹",
    "general": "🐾",
}


def category_label(category: str) -> str:
    """Return the category prefixed with its emoji (falls back to a paw)."""
    emoji = CATEGORY_EMOJI.get(category, "🐾")
    return f"{emoji} {category.capitalize()}"

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

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

st.subheader("Add a Pet")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    st.session_state.owner.name = owner_name
    pet = Pet(name=pet_name, breed=species, owner=st.session_state.owner)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added {pet_name} to {owner_name}'s pets.")

pets = st.session_state.owner.get_pets()
if pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "breed": p.breed} for p in pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    category = st.selectbox(
        "Category",
        ["exercise", "feeding", "meds", "grooming", "play", "cleaning", "general"],
        format_func=category_label,
    )

col4, col5 = st.columns(2)
with col4:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col5:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {
            "title": task_title,
            "duration_minutes": int(duration),
            "priority": priority,
            "category": category,
        }
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Task": t["title"],
                "Category": category_label(t.get("category", "general")),
                "Duration (min)": t["duration_minutes"],
                "Priority": t["priority"].capitalize(),
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

# priority 1 is highest; larger numbers are lower priority
PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}
# Reverse lookup so the schedule table can show a readable priority label.
PRIORITY_LABEL = {1: "High", 2: "Medium", 3: "Low"}

pets = st.session_state.owner.get_pets()
if not pets:
    st.info("Add a pet above before generating a schedule.")
else:
    pet_names = [p.name for p in pets]
    selected = st.selectbox("Schedule for pet", pet_names)

    if st.button("Generate schedule"):
        pet = next(p for p in pets if p.name == selected)

        # Attach the UI-entered tasks to the selected pet.
        pet.tasks = []
        for t in st.session_state.tasks:
            pet.add_task(
                Task(
                    name=t["title"],
                    duration=t["duration_minutes"],
                    priority=PRIORITY_MAP[t["priority"]],
                    category=t.get("category", "general"),
                )
            )

        scheduler = Scheduler(pet)
        scheduled = scheduler.generate_schedule()

        if scheduled:
            st.success(f"✅ Scheduled {len(scheduled)} task(s) for {pet.name}.")

            conflicts = scheduler.find_conflicts()
            if conflicts:
                for prev, curr in conflicts:
                    st.warning(
                        f"⚠️ Conflict: '{prev.name}' overlaps with '{curr.name}'."
                    )

            sorted_tasks = scheduler.sort_by_time()
            st.table(
                [
                    {
                        "Task": task.name,
                        "Duration (min)": task.duration,
                        "Priority": PRIORITY_LABEL.get(task.priority, task.priority),
                        "Category": category_label(task.category),
                    }
                    for task in sorted_tasks
                ]
            )
        else:
            st.warning("⚠️ No tasks fit within the available time budget.")
