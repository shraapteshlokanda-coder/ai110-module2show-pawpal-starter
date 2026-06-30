# PawPal+ Project Reflection

## 1. System Design
Three core actions a user should be able to perform:
- Add a pet and owner profile so the system knows who is responsible for care.
- Add or edit pet care tasks with duration and priority so the schedule can reflect real needs.
- Generate and view a daily care plan that orders tasks based on available time and priority.

**a. Initial design**
I designed four main classes:
- `Owner`: stores owner information, available daily time, preferences, and pets.
- `Pet`: stores pet details and a list of associated care tasks.
- `Task`: stores task metadata such as title, duration, priority, preferred time, and completion state.
- `PawPalScheduler`: generates a daily plan for a pet and explains why tasks were chosen.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I kept the model focused on four classes, and didn't need to mke any implementations yet. I think I should be able to add the relationships and complexity within the actual methods. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff: the scheduler detects conflicts only when tasks have the exact same `preferred_time` and `due_date`, rather than checking for overlapping time intervals. This simplifies the implementation and keeps conflict detection lightweight and fast, but it can miss overlaps where one task runs into another (for example, a 30-minute task at 08:30 overlapping a 15-minute task at 08:45). For the scope of this project — a simple daily planner for busy owners — exact-time matching provides useful warnings without adding scheduling complexity (slot management, interval math, or calendar integration). If needed, the next iteration can add interval-based overlap checks.

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
