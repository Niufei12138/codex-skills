---
name: skill-github-publisher
description: Publish or sync local Codex skills to a GitHub repository. Use when the user asks to share a skill, publish a skill to GitHub, sync updated skills, create a skills repository, update README/index/docs for shared skills, or push local skill changes after creating or updating SKILL.md.
---

# Skill GitHub Publisher

Use this skill to publish local Codex skills from the user's Codex skills directory, usually `$env:USERPROFILE\.codex\skills` on Windows, to a GitHub repository. This is a user-confirmed publishing workflow, not a background watcher.

## Safety Rules

- Confirm whether the target repository should be public or private before creating it.
- Inspect skill contents before publishing; do not publish secrets, tokens, private data, local machine paths, or user-specific credentials.
- Publish only skills the user created or intentionally modified. Do not publish third-party skills installed from outside unless the user has forked, adapted, and explicitly approved sharing that adapted version.
- Do not push automatically when the worktree contains unrelated changes.
- Prefer a single skills monorepo unless the user requests one repo per skill.
- For batch publishing, use `publish-manifest.json` as the allowlist. Do not run unrestricted `--all` over the entire local skills directory.
- Keep generated docs concise and derived from the skill files.

## Recommended Repository Layout

```text
codex-skills/
  README.md
  index.json
  publish-manifest.json
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
   - Multiple skills: use the skills listed in `publish-manifest.json`.
   - All skills: publish only allowlisted skills from `publish-manifest.json`; never publish every local skill just because it exists under the user's Codex skills directory.

2. Resolve target repository:
   - If a local repo path is provided, use it.
   - Otherwise create or use a local publishing repo named `codex-skills` in the current workspace.
   - Ensure GitHub CLI is installed and authenticated before creating or pushing a remote repository.
   - If the GitHub repo does not exist, use `gh repo create` after confirming name and visibility.

3. Validate source skill:
   - Run `quick_validate.py` on each skill before publishing.
   - Confirm each selected skill is self-created or user-modified before copying it into the publishing repo.
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
  --manifest .\codex-skills\publish-manifest.json `
  --all
```

## Publish Manifest

Use `publish-manifest.json` to record which skills are intentionally shareable:

```json
{
  "skills": [
    {
      "name": "origin-publication-figure",
      "status": "created-or-modified-by-user",
      "reason": "Created locally and maintained as a shareable Origin figure workflow."
    }
  ]
}
```

When a new self-created or user-modified skill should be shared, add it to this manifest before batch syncing. External skills remain local unless explicitly listed and approved.

## GitHub CLI Notes

- Check `gh --version` and `gh auth status` before creating repos or pushing.
- If `gh` is missing on Windows, install it with:

```powershell
winget install --id GitHub.cli -e --accept-package-agreements --accept-source-agreements
```

- If the current terminal cannot find `gh` after installation, open a new terminal or use the full path:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" --version
```

- If `gh auth status` says the user is not logged in, use the quickest browser/device-code flow:

```powershell
gh auth login --hostname github.com --git-protocol https --web --clipboard --scopes repo
```

Then open `https://github.com/login/device`, paste the copied one-time code, and approve GitHub CLI. Recheck with:

```powershell
gh auth status
```

- If browser login fails because GitHub is unreachable or times out, use a personal access token instead:

```powershell
gh auth login --hostname github.com --git-protocol https --with-token
```

Paste a GitHub token with at least `repo` permission. Do not save or print the token in project files or chat logs.

- For a new public repository:

```powershell
gh repo create <owner-or-user>/codex-skills --public --source <repo-dir> --remote origin --push
```

Use `--private` instead of `--public` when needed.

## Update Behavior

When a skill changes later, rerun the prepare script for that skill. It replaces the published copy of that skill, regenerates that skill's docs, and updates the central index. It does not delete unrelated skills unless their folders are explicitly removed from the publishing repo by the user.
