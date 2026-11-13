#!/usr/bin/env python3
"""
validate.py — Cross-platform consistency checks for an Engram repository.
Runs on Windows (PowerShell/CMD), macOS, and Linux using only the Python standard library.
validate.sh runs the same checks.

Usage:
    python validate.py [path/to/engram]
"""

import sys
import os
import re

# Determine repository root
if len(sys.argv) > 1:
    REPO = os.path.abspath(sys.argv[1])
else:
    # Try git root or current working directory
    try:
        import subprocess
        git_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL).decode().strip()
        REPO = git_root
    except Exception:
        REPO = os.getcwd()

# ANSI Colors
USE_COLOR = sys.stdout.isatty() and os.name != "nt" or "ANSICON" in os.environ or "WT_SESSION" in os.environ
RED = "\033[0;31m" if USE_COLOR else ""
GREEN = "\033[0;32m" if USE_COLOR else ""
YELLOW = "\033[0;33m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
NC = "\033[0m" if USE_COLOR else ""

APPROVED_STATUSES = set(
    "current|draft|future|in-progress|concluded|achieved|abandoned|superseded|planned|active|paused|completed|undertaken|void".split("|")
)

errors = []
warnings = []

def error(msg):
    errors.append(msg)
    print(f"{RED}ERROR{NC}: {msg}")

def warn(msg):
    warnings.append(msg)
    print(f"{YELLOW}WARN{NC}:  {msg}")

def pass_msg(msg):
    print(f"{GREEN}PASS{NC}:  {msg}")

print(f"{BOLD}=== Engram Validation ==={NC}")
print(f"Repository: {REPO}\n")

# 1. Frontmatter Compliance
print(f"{BOLD}--- Frontmatter Compliance ---{NC}")
leaf_count = 0
leaf_pass = 0

EXCLUDED_FILES = {
    "INDEX.md", "README.md", "template.md", "AGENTS.md", "CHANGELOG.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md"
}

for root, dirs, files in os.walk(REPO):
    # Skip hidden/tooling folders
    if any(p in root.split(os.sep) for p in [".git", ".agents", ".github"]):
        continue
    for file in files:
        if not file.endswith(".md") or file in EXCLUDED_FILES:
            continue

        leaf_count += 1
        filepath = os.path.join(root, file)
        rel = os.path.relpath(filepath, REPO).replace("\\", "/")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            error(f"{rel} — failed to read file: {e}")
            continue

        if not lines or lines[0].strip() != "---":
            error(f"{rel} — missing frontmatter (no opening ---)")
            continue

        # Extract frontmatter block
        fm_lines = []
        found_closing = False
        for line in lines[1:]:
            if line.strip() == "---":
                found_closing = True
                break
            fm_lines.append(line)

        if not found_closing:
            error(f"{rel} — unclosed frontmatter block")
            continue

        fm_text = "".join(fm_lines)
        missing = []
        for req in ["status", "created", "updated", "tags"]:
            if not re.search(rf"^{req}:", fm_text, re.MULTILINE):
                missing.append(req)

        if missing:
            error(f"{rel} — missing frontmatter fields: {' '.join(missing)}")
            continue

        m = re.search(r"^status:\s*(\S+)", fm_text, re.MULTILINE)
        if not m or m.group(1) not in APPROVED_STATUSES:
            status_val = m.group(1) if m else "none"
            error(f"{rel} — invalid status value: '{status_val}'")
            continue

        leaf_pass += 1

if leaf_count == 0:
    warn("No leaf documents found")
else:
    pass_msg(f"Frontmatter: {leaf_pass}/{leaf_count} leaf documents compliant")
print("")

# 1b. Skill Frontmatter Compliance
print(f"{BOLD}--- Skill Frontmatter Compliance ---{NC}")
skill_count = 0
skill_pass = 0
skills_dir = os.path.join(REPO, ".agents", "skills")

for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" not in files:
        continue
    skill_count += 1
    filepath = os.path.join(root, "SKILL.md")
    rel = os.path.relpath(filepath, REPO).replace("\\", "/")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        error(f"{rel} — failed to read file: {e}")
        continue

    if not lines or lines[0].strip() != "---":
        error(f"{rel} — missing frontmatter (no opening ---)")
        continue

    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    fm_text = "".join(fm_lines)

    missing = [req for req in ["name", "description"] if not re.search(rf"^{req}:", fm_text, re.MULTILINE)]
    if missing:
        error(f"{rel} — missing frontmatter fields: {' '.join(missing)}")
        continue

    skill_pass += 1

if skill_count == 0:
    warn("No skill documents found")
else:
    pass_msg(f"Skills: {skill_pass}/{skill_count} skill documents compliant")
print("")

# 2. INDEX Link Consistency
print(f"{BOLD}--- INDEX Link Consistency ---{NC}")
index_checked = 0
index_errors = 0

for root, dirs, files in os.walk(REPO):
    if any(p in root.split(os.sep) for p in [".git", ".agents"]):
        continue
    if "INDEX.md" in files:
        index_file = os.path.join(root, "INDEX.md")
        rel_index = os.path.relpath(index_file, REPO).replace("\\", "/")

        try:
            with open(index_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            error(f"{rel_index} — failed to read INDEX file: {e}")
            continue

        # Extract markdown links [text](path)
        links = re.findall(r"\]\(([^)]+)\)", content)
        for link in links:
            link = link.strip()
            # Skip external, anchor, or root/parent navigation links
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#") or link.endswith("AGENTS.md"):
                continue

            index_checked += 1
            # Clean anchor from local link if present (e.g. file.md#section)
            clean_link = link.split("#")[0]
            if not clean_link:
                continue

            target = os.path.normpath(os.path.join(root, clean_link))
            if not os.path.exists(target):
                error(f"{rel_index} — broken link: {link} (target not found)")
                index_errors += 1

if index_checked == 0:
    warn("No INDEX links found to check")
else:
    pass_msg(f"INDEX links: {index_checked - index_errors}/{index_checked} links resolve")
print("")

# 3. Orphan Detection
print(f"{BOLD}--- Orphan Detection ---{NC}")
# Every directory that has an INDEX.md is checked: each .md file beside the
# INDEX (not INDEX/README/template) must be referenced in it. An orphan is an
# error, because a document no index points to is unreachable by navigation.
orphan_count = 0

for domain_dir, dirs, files in os.walk(REPO):
    if any(p in domain_dir.split(os.sep) for p in [".git", ".agents"]):
        continue
    if "INDEX.md" not in files:
        continue

    domain = os.path.relpath(domain_dir, REPO).replace("\\", "/")
    try:
        with open(os.path.join(domain_dir, "INDEX.md"), "r", encoding="utf-8") as f:
            index_content = f.read()
    except Exception:
        continue

    for item in sorted(files):
        if not item.endswith(".md") or item in {"INDEX.md", "README.md", "template.md"}:
            continue
        if item not in index_content:
            rel = os.path.relpath(os.path.join(domain_dir, item), REPO).replace("\\", "/")
            error(f"{rel} — not referenced in {domain}/INDEX.md (orphan)")
            orphan_count += 1

if orphan_count == 0:
    pass_msg("No orphan files detected")
print("")

# 4. Navigation Links
print(f"{BOLD}--- Navigation Links ---{NC}")
nav_checked = 0
nav_errors = 0

for root, dirs, files in os.walk(REPO):
    if any(p in root.split(os.sep) for p in [".git", ".agents"]):
        continue
    if "INDEX.md" in files:
        index_file = os.path.join(root, "INDEX.md")
        rel_index = os.path.relpath(index_file, REPO).replace("\\", "/")

        try:
            with open(index_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue

        for line in lines:
            if re.match(r"^-\s+(Parent|Root):", line):
                m = re.search(r"\(([^)]+)\)", line)
                if m:
                    nav_checked += 1
                    target_rel = m.group(1).split("#")[0]
                    target = os.path.normpath(os.path.join(root, target_rel))
                    if not os.path.isfile(target):
                        error(f"{rel_index} — broken navigation link: {m.group(1)}")
                        nav_errors += 1

if nav_checked == 0:
    warn("No navigation links found to check")
else:
    pass_msg(f"Navigation: {nav_checked - nav_errors}/{nav_checked} links resolve")
print("")

# Summary
print(f"{BOLD}=== Summary ==={NC}")
total_errors = len(errors)
total_warnings = len(warnings)

if total_errors == 0 and total_warnings == 0:
    print(f"{GREEN}All checks passed.{NC}")
elif total_errors == 0:
    print(f"{YELLOW}{total_warnings} warning(s), no errors.{NC}")
else:
    print(f"{RED}{total_errors} error(s), {total_warnings} warning(s).{NC}")

sys.exit(total_errors)
