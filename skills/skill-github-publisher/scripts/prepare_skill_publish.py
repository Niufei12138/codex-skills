#!/usr/bin/env python3
"""Prepare local Codex skills for publication in a GitHub repository."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}
INDEX_START = "<!-- skill-github-publisher:index:start -->"
INDEX_END = "<!-- skill-github-publisher:index:end -->"


@dataclass
class SkillMeta:
    name: str
    description: str
    path: Path
    display_name: str | None = None
    short_description: str | None = None
    default_prompt: str | None = None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = read_text(skill_md)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {skill_md}")
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        data[key.strip()] = value
    return data


def parse_openai_yaml(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if ":" not in stripped or stripped.startswith("#"):
            continue
        key, value = stripped.split(":", 1)
        if key in {"display_name", "short_description", "default_prompt"}:
            data[key] = value.strip().strip('"').strip("'")
    return data


def load_skill(skill_dir: Path) -> SkillMeta:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"Not a Codex skill folder, missing SKILL.md: {skill_dir}")
    frontmatter = parse_frontmatter(skill_md)
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not name or not description:
        raise ValueError(f"SKILL.md must contain name and description: {skill_md}")
    ui = parse_openai_yaml(skill_dir / "agents" / "openai.yaml")
    return SkillMeta(
        name=name,
        description=description,
        path=skill_dir,
        display_name=ui.get("display_name"),
        short_description=ui.get("short_description"),
        default_prompt=ui.get("default_prompt"),
    )


def iter_local_skills(root: Path) -> list[SkillMeta]:
    skills: list[SkillMeta] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name == ".system":
            continue
        skill_md = child / "SKILL.md"
        if skill_md.exists():
            skills.append(load_skill(child))
    return skills


def copy_skill(skill: SkillMeta, repo_dir: Path) -> Path:
    dest = repo_dir / "skills" / skill.name
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    def ignore(_dir: str, names: list[str]) -> set[str]:
        return {name for name in names if name in SKIP_DIRS or name in SKIP_FILES}

    shutil.copytree(skill.path, dest, ignore=ignore)
    return dest


def doc_for_skill(skill: SkillMeta) -> str:
    rel = f"../skills/{skill.name}/SKILL.md"
    title = skill.display_name or skill.name
    lines = [
        f"# {title}",
        "",
        skill.short_description or skill.description,
        "",
        "## Skill",
        "",
        f"- Name: `{skill.name}`",
        f"- Source: [`skills/{skill.name}/SKILL.md`]({rel})",
    ]
    if skill.default_prompt:
        lines.extend(["", "## Example Prompt", "", f"```text\n{skill.default_prompt}\n```"])
    lines.extend(
        [
            "",
            "## Description",
            "",
            skill.description,
            "",
            "## Install",
            "",
            f"Copy `skills/{skill.name}` into your local Codex skills directory, for example `~/.codex/skills/{skill.name}`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_docs(skills: list[SkillMeta], repo_dir: Path) -> None:
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        (docs_dir / f"{skill.name}.md").write_text(doc_for_skill(skill), encoding="utf-8")


def write_index(skills: list[SkillMeta], repo_dir: Path) -> None:
    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills": [
            {
                "name": skill.name,
                "display_name": skill.display_name,
                "short_description": skill.short_description,
                "description": skill.description,
                "path": f"skills/{skill.name}",
                "docs": f"docs/{skill.name}.md",
            }
            for skill in sorted(skills, key=lambda item: item.name)
        ],
    }
    (repo_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_published_skills(repo_dir: Path) -> list[SkillMeta]:
    skills_dir = repo_dir / "skills"
    if not skills_dir.exists():
        return []
    return iter_local_skills(skills_dir)


def readme_index(skills: list[SkillMeta]) -> str:
    lines = [
        INDEX_START,
        "",
        "| Skill | Description | Docs |",
        "| --- | --- | --- |",
    ]
    for skill in sorted(skills, key=lambda item: item.name):
        label = skill.display_name or skill.name
        description = skill.short_description or skill.description
        lines.append(f"| `{skill.name}` | {description} | [docs](docs/{skill.name}.md) |")
    lines.extend(["", INDEX_END])
    return "\n".join(lines)


def write_readme(skills: list[SkillMeta], repo_dir: Path) -> None:
    readme = repo_dir / "README.md"
    generated = readme_index(skills)
    if readme.exists():
        text = read_text(readme)
        pattern = re.compile(
            re.escape(INDEX_START) + r".*?" + re.escape(INDEX_END),
            re.DOTALL,
        )
        if pattern.search(text):
            text = pattern.sub(generated, text)
        else:
            text = text.rstrip() + "\n\n## Skills\n\n" + generated + "\n"
    else:
        text = "# Codex Skills\n\nReusable Codex skills published from a local workspace.\n\n" + generated + "\n"
    readme.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, help="Single local skill folder to publish")
    parser.add_argument("--skills-root", type=Path, help="Root containing local skill folders")
    parser.add_argument("--repo-dir", type=Path, required=True, help="Local publishing repository")
    parser.add_argument("--all", action="store_true", help="Publish all local skills under --skills-root")
    args = parser.parse_args()

    if args.all:
        if not args.skills_root:
            parser.error("--all requires --skills-root")
        source_skills = iter_local_skills(args.skills_root)
    else:
        if not args.skill_dir:
            parser.error("provide --skill-dir or use --all with --skills-root")
        source_skills = [load_skill(args.skill_dir)]

    if not source_skills:
        raise SystemExit("No skills found to publish")

    args.repo_dir.mkdir(parents=True, exist_ok=True)
    for subdir in ["skills", "docs"]:
        (args.repo_dir / subdir).mkdir(parents=True, exist_ok=True)

    copied = []
    for skill in source_skills:
        copied.append(str(copy_skill(skill, args.repo_dir)))

    published_skills = read_published_skills(args.repo_dir)
    write_docs(published_skills, args.repo_dir)
    write_index(published_skills, args.repo_dir)
    write_readme(published_skills, args.repo_dir)

    summary = {
        "repo_dir": str(args.repo_dir),
        "published": [skill.name for skill in source_skills],
        "copied_to": copied,
        "total_indexed": len(published_skills),
        "generated": ["README.md", "index.json", "docs/"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
