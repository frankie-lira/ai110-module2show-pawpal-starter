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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
