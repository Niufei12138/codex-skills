---
name: skill-github-publisher
description: Publish or sync local Codex skills to a GitHub repository. Use when the user asks to share a skill, publish a skill to GitHub, sync updated skills, create a skills repository, update README/index/docs for shared skills, or push local skill changes after creating or updating SKILL.md.
---

# Skill GitHub Publisher

Use this skill to publish local Codex skills from the user's Codex skills directory, usually `$env:USERPROFILE\.codex\skills` on Windows, to a GitHub repository. This is a user-confirmed publishing workflow, not a background watcher.

## Safety Rules

- Confirm whether the target repository should be public or private before creating it.
- Inspect skill contents before publishing; do not publish secrets, tokens, private data, local machine paths, or user-specific credentials.
- Do not push automatically when the worktree contains unrelated changes.
- Prefer a single skills monorepo unless the user requests one repo per skill.
- Keep generated docs concise and derived from the skill files.

## Recommended Repository Layout

```text
codex-skills/
  README.md
  index.json
  docs/
    <skill-name>.md
  skills/
    <skill-name>/
      SKILL.md
      agents/openai.yaml
      references/
      scripts/
      assets/
```

## Workflow

1. Resolve scope:
   - One skill: use the requested skill folder.
   - All skills: publish all non-system local skills under the user's Codex skills directory.

2. Resolve target repository:
   - If a local repo path is provided, use it.
   - Otherwise create or use a local publishing repo named `codex-skills` in the current workspace.
   - If the GitHub repo does not exist, use `gh repo create` after confirming name and visibility.

3. Validate source skill:
   - Run `quick_validate.py` on each skill before publishing.
   - Stop on validation failure and fix the skill first.

4. Generate publish artifacts:
   - Run `scripts/prepare_skill_publish.py` to copy skill files into the publishing repo and update `README.md`, `docs/<skill>.md`, and `index.json`.
   - Inspect generated output before committing.

5. Commit and push:
   - Run `git status -sb` and inspect diffs.
   - Stage only generated publishing files.
   - Commit with a focused message such as `Publish origin-publication-figure skill` or `Sync Codex skills`.
   - Push to GitHub.

6. Final response:
   - Report repo path, GitHub URL if known, commit hash, published skills, and validation status.

## Commands

Prepare one skill:

```powershell
python $env:USERPROFILE\.codex\skills\skill-github-publisher\scripts\prepare_skill_publish.py `
  --skill-dir $env:USERPROFILE\.codex\skills\origin-publication-figure `
  --repo-dir .\codex-skills
```

Prepare all local skills:

```powershell
python $env:USERPROFILE\.codex\skills\skill-github-publisher\scripts\prepare_skill_publish.py `
  --skills-root $env:USERPROFILE\.codex\skills `
  --repo-dir .\codex-skills `
  --all
```

## GitHub CLI Notes

- Check `gh --version` and `gh auth status` before creating repos or pushing.
- For a new public repository:

```powershell
gh repo create <owner-or-user>/codex-skills --public --source <repo-dir> --remote origin --push
```

Use `--private` instead of `--public` when needed.

## Update Behavior

When a skill changes later, rerun the prepare script for that skill. It replaces the published copy of that skill, regenerates that skill's docs, and updates the central index. It does not delete unrelated skills unless their folders are explicitly removed from the publishing repo by the user.
