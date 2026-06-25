# Codex Skills

Reusable Codex skills for scientific plotting, skill maintenance, and GitHub publishing workflows.

## Install

Copy the skill folder you need from `skills/` into your local Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\<skill-name> $env:USERPROFILE\.codex\skills\<skill-name>
```

Restart Codex after installing or updating a skill.

## Skills

<!-- skill-github-publisher:index:start -->

| Skill | Description | Docs |
| --- | --- | --- |
| `origin-publication-figure` | Create journal-ready Origin figures with QA. | [docs](docs/origin-publication-figure.md) |
| `skill-evolution-review` | Review task lessons and update skills safely. | [docs](docs/skill-evolution-review.md) |
| `skill-github-publisher` | Publish local Codex skills to GitHub. | [docs](docs/skill-github-publisher.md) |

<!-- skill-github-publisher:index:end -->
