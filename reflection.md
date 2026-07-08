# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial design has four main classes: Owner, Pet, Task, and Scheduler. Owner holds the pet owner's name and available time per day. Pet holds the pet's name, breed, a reference to its Owner, and a list of Tasks. Task is a dataclass holding the task name, duration in minutes, priority level, and category. Scheduler takes a Pet and available time and produces a sorted, filtered daily schedule.

- What classes did you include, and what responsibilities did you assign to each?

Owner — stores owner name and daily time available, holds a list of Pet objects.
Pet — stores pet name and breed, holds a list of Task objects, and provides methods to add and retrieve tasks.
Task — a dataclass that stores task name, duration, priority, and category. Pure data, no methods.
Scheduler — takes a pet's task list and available time, sorts by priority, filters by time, and generates a daily schedule.

**b. Design changes**

- Did your design change during implementation?

Yes, I made three design changes based on Claude Code's review of the skeleton.

- If yes, describe at least one change and why you made it.

The biggest change was removing available_time as a separate argument to Scheduler. Originally Scheduler took its own available_time int, which could drift out of sync with Owner.available_time. I changed it so Scheduler derives the budget directly from pet.owner.available_time. This ensures there is always one source of truth for how much time the owner has available.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers two main constraints: task priority (1 is highest) and available time budget in minutes. It sorts tasks by priority first, then does a cumulative pass to keep only tasks that fit within the owner's available time. Tasks with a start_time are also sorted chronologically for conflict detection.

- How did you decide which constraints mattered most?

Priority was the most important constraint because a pet owner should always complete critical tasks like feeding and medication before optional ones like grooming. Time budget was second because the scheduler needs to produce a realistic plan that fits within a day.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The find_conflicts() method only compares each task against its immediate predecessor after sorting by start time. This means it can miss conflicts between non-adjacent tasks — for example, if task A runs 8:00-10:00 and task C starts at 9:00, but task B is between them, the A-C conflict is never checked.

- Why is that tradeoff reasonable for this scenario?

For a simple pet care app, back-to-back scheduling conflicts are the most common and practical concern. A full O(n²) comparison of every pair would be more correct but adds complexity that isn't justified for this use case. The greedy adjacent check is fast, readable, and catches the most likely real-world scheduling mistakes.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used Claude Code inside VS Code throughout the entire project. I used it for design brainstorming (generating the UML diagram), scaffolding (creating class skeletons from the UML), implementation (writing the full logic for all four classes), and algorithmic improvements (adding sort_by_time, filter_by_completion, and find_conflicts).

- What kinds of prompts or questions were most helpful?

The most helpful prompts were specific and included context — attaching the relevant files and describing exactly what I wanted. For example, asking Claude Code to review the skeleton and identify missing relationships gave much more useful feedback than a vague question. Multi-step prompts like "move this function, fix this bug, and update the import" were also very efficient.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When Claude Code suggested replacing the zip-based conflict detection with itertools.pairwise for readability, I evaluated whether the change was worth making. I decided to keep the current version because it was already readable enough and the bigger issue Claude identified — adjacent-only comparison missing non-adjacent conflicts — was a design decision I chose to accept as a documented tradeoff rather than fix.

- How did you evaluate or verify what the AI suggested?

I read Claude Code's explanation carefully and ran the existing tests to confirm they still passed. I also manually traced through the conflict detection logic with a sample scenario to verify I understood the tradeoff before documenting it.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested that mark_complete() correctly sets a Task's completed status to True, that add_task() increases a Pet's task count by 1, that sort_by_time() orders timed tasks before untimed ones, and that find_conflicts() correctly identifies overlapping tasks.

- Why were these tests important?

These tests verified the core behaviors that the scheduler depends on. If mark_complete or add_task were broken, the entire system would malfunction. The sort and conflict tests confirmed that the new algorithmic features worked correctly before connecting them to the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am moderately confident. All 6 tests pass and the CLI demo produces correct output. The greedy scheduling logic is simple enough to trace manually and verify.

- What edge cases would you test next if you had more time?

I would test scheduling with zero available time, adding duplicate tasks, scheduling a pet with no tasks, and conflict detection with three or more overlapping tasks to verify the adjacent-only limitation is handled gracefully.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the design phase. Starting with a UML diagram before writing any code made the implementation much smoother. Having Claude Code review the skeleton before implementing caught three structural issues early that would have been harder to fix later.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign the conflict detection to track a running maximum end time instead of only comparing adjacent tasks. I would also add a recurring field to Task so that daily tasks like feeding automatically reset each day without manual intervention.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is most useful as a design partner when you give it specific context and ask it to explain its reasoning. The most valuable moments were not when Claude Code wrote code for me, but when it identified structural problems in my design that I hadn't noticed — like the available_time duplication and the back-reference sync issue.