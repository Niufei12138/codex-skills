---
name: skill-evolution-review
description: Review whether a completed or nearly completed task produced reusable lessons that should update a local Codex skill. Use after tasks that used a local skill, required repeated fixes, exposed tool quirks, revealed user preferences, produced QA failures, or prompted the user to ask for skill improvement, reflection, post-task optimization, or writing lessons back into SKILL.md.
---

# Skill Evolution Review

Use this skill to keep local skills improving without turning every one-off issue into permanent policy. The mechanism is: detect candidate lessons, filter them, propose concise updates, get user confirmation, then edit and validate the affected skill.

## End-of-Task Check

At the end of a task that used a local skill or a repeatable workflow, silently ask:

- Did the task require rework because the skill missed an important rule?
- Did a tool behave in a non-obvious way that future tasks should anticipate?
- Did the user state a durable preference, default, or quality bar?
- Did QA reveal a reusable failure mode?
- Did the task produce a better workflow than the current skill describes?

If all answers are no, do not mention this skill. If any answer is yes, add a short "Skill update candidate" note to the final response unless the user is asking for no extra commentary.

## Candidate Test

Write back only lessons that are:

- Reusable across likely future tasks, not just this dataset or file.
- Actionable as a rule, workflow step, quality gate, tool mapping, or default.
- Compatible with the skill's purpose and triggering scope.
- More likely to improve task quality than add friction.
- Specific enough to guide behavior, but not so narrow that it overfits one case.

Do not write back:

- Pure status reports.
- One-off facts about a single file, client, graph, bug, or dataset.
- The user's temporary preference for one task.
- Rules that duplicate existing skill text without improving it.
- Rules that contradict stronger system/developer instructions.
- Long retrospectives, changelogs, or implementation history.

## Conflict Check

Before editing a skill:

1. Read the target `SKILL.md` completely.
2. Read only the directly relevant reference files.
3. Identify the closest existing rule.
4. Decide whether the new lesson should replace, refine, or be rejected.
5. Prefer merging into existing sections over appending a new "lessons learned" list.

If a proposed rule conflicts with existing guidance, explain the conflict and ask before changing it.

## Proposal Format

When a candidate exists, propose at most three updates:

```text
Skill update candidates:
- Target: <skill-name>
  Lesson: <reusable lesson>
  Why it generalizes: <one short reason>
  Suggested merge point: <section/file>
```

Ask for confirmation before editing unless the user has already explicitly asked to update the skill.

## Edit Workflow

When approved:

1. Edit with minimal scope.
2. Preserve the skill's concise style.
3. Merge new guidance into the most relevant existing section.
4. Update UI metadata only if trigger behavior changes.
5. Run the skill validator:
   `python $env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill-folder>`
6. If `skill-github-publisher` is available and the edited skill is intended to be shareable, ask whether to sync the updated skill to GitHub. Do not publish without confirmation.
7. Report what changed and whether validation passed.

## Quality Bar

Skill evolution is worthwhile only when it makes future task execution better. Optimize for:

- Better defaults.
- Fewer repeated failures.
- Clearer triggering.
- Better QA.
- Less user burden.
- Less context bloat.

If an update would make a skill longer but not meaningfully better, reject it.
