# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial design has four main classes: Owner, Pet, Task, and Scheduler. Owner holds the pet owner's name and preferences. Pet holds the pet's name, type, and a list of tasks. Task holds the task name, duration, priority, and category. Scheduler takes a pet's tasks and available time and produces a sorted daily plan.

- What classes did you include, and what responsibilities did you assign to each?

Owner — stores owner name and daily time available for pet care.
Pet — stores pet name and breed, and holds a list of Task objects.
Task — stores task name, duration in minutes, priority level, and category (walk, feeding, meds, etc.).
Scheduler — takes the list of tasks and available time, sorts by priority, and generates a daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

To be filled in after implementation.

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
