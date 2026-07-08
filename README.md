# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Today's Schedule
========================================
Owner: Alex  (available time: 120 min)
Rex the Labrador:
  - Morning walk (priority 1, 45 min, exercise)
  - Feed breakfast (priority 2, 15 min, feeding)
  - Grooming (priority 4, 60 min, grooming)
  Total scheduled time: 120 min
Mittens the Tabby:
  - Feed (priority 1, 10 min, feeding)
  - Clean litter box (priority 2, 20 min, cleaning)
  - Play time (priority 3, 30 min, play)
  Total scheduled time: 60 min
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest tests/test_pawpal.py -v
```

Tests cover: task sorting by priority and time, conflict detection, time budget filtering, and completed task handling.

**Confidence Level: ⭐⭐⭐⭐ (4/5)**
All 17 tests pass. The scheduler handles edge cases like empty lists, zero budgets, and exact-fit tasks. The one known limitation is conflict detection only checks adjacent tasks, not all pairs.

```
platform darwin -- Python 3.13.13, pytest-9.0.3
collected 17 items

tests/test_pawpal.py::test_mark_complete_sets_completed_true PASSED           [  5%]
tests/test_pawpal.py::test_add_task_increases_task_count PASSED               [ 11%]
tests/test_pawpal.py::test_sort_by_time_orders_timed_then_untimed PASSED      [ 17%]
tests/test_pawpal.py::test_filter_by_time_skips_completed_tasks PASSED        [ 23%]
tests/test_pawpal.py::test_find_conflicts_detects_overlap PASSED              [ 29%]
tests/test_pawpal.py::test_find_conflicts_ignores_adjacent_and_untimed PASSED [ 35%]
tests/test_pawpal.py::test_sort_by_priority_breaks_ties_by_shorter_duration PASSED [ 41%]
tests/test_pawpal.py::test_sort_by_priority_is_stable_on_full_ties PASSED    [ 47%]
tests/test_pawpal.py::test_sort_by_time_places_midnight_before_untimed PASSED [ 52%]
tests/test_pawpal.py::test_sort_by_time_orders_untimed_among_themselves_by_priority PASSED [ 58%]
tests/test_pawpal.py::test_sorts_handle_empty_task_list PASSED                [ 64%]
tests/test_pawpal.py::test_find_conflicts_detects_identical_start_times PASSED [ 70%]
tests/test_pawpal.py::test_find_conflicts_zero_duration_at_same_start_conflicts PASSED [ 76%]
tests/test_pawpal.py::test_filter_by_time_skips_overflow_but_keeps_later_fitting_task PASSED [ 82%]
tests/test_pawpal.py::test_filter_by_time_includes_exact_fit PASSED          [ 88%]
tests/test_pawpal.py::test_filter_by_time_zero_budget_schedules_nothing PASSED [ 94%]
tests/test_pawpal.py::test_filter_by_time_completed_task_frees_budget_for_later_task PASSED [100%]

==================== 17 passed in 0.02s ====================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting by priority | sort_by_priority() | Sorts by priority, 1 is highest; ties broken by shorter duration |
| Task sorting by time | sort_by_time() | Chronological order; untimed tasks fall to the end |
| Filtering by time budget | filter_by_time() | Cumulative pass, drops tasks that exceed available time |
| Filtering completed tasks | filter_by_completion() | Skips tasks already marked complete |
| Conflict detection | find_conflicts() | Detects overlapping tasks by start time; adjacent comparison |
| Schedule generation | generate_schedule() | Greedy algorithm — sorts by priority then filters by time |

## 🎨 UI Formatting Features

| Feature | Implementation | Notes |
|---------|---------------|-------|
| Category emojis | CATEGORY_EMOJI map in app.py | 🚶 exercise, 🍽️ feeding, 💊 meds, ✂️ grooming, 🎾 play, 🧹 cleaning |
| Priority labels | PRIORITY_LABEL map in app.py | High/Medium/Low instead of 1/2/3 |
| Conflict warnings | st.warning() | Shows which tasks overlap |
| Schedule table | st.table() | Clean columns for task, duration, priority, category |

## 📸 Demo Walkthrough

1. User opens the app and sees the PawPal+ interface with an Add a Pet form
2. User enters owner name "Frankie" and pet name "Miyuki" (cat), then clicks Add Pet
3. Miyuki appears in the Current Pets table
4. User adds tasks — Feed (20 min, high), Clean litter box (15 min, medium), Play time (30 min, low)
5. User selects Miyuki from the Schedule for Pet dropdown and clicks Generate Schedule
6. App displays the scheduled tasks in priority order with total time used