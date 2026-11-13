#!/usr/bin/env bash
# validate.sh — Automated consistency checks for an Engram repository.
# Uses bash with POSIX grep, find, sed, head, dirname and basename (no GNU-only
# options, so it also runs with the BSD tools on macOS). validate.py runs the
# same checks.
#
# Usage: bash validate.sh [/path/to/engram]
# Default path: the enclosing git repository root, or the current directory outside a repository

set -uo pipefail

REPO="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
ERRORS=0
WARNINGS=0

# Colours (disabled if not a terminal)
if [ -t 1 ]; then
  RED='\033[0;31m'
  YELLOW='\033[0;33m'
  GREEN='\033[0;32m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' YELLOW='' GREEN='' BOLD='' NC=''
fi

error() { echo -e "${RED}ERROR${NC}: $1"; ((ERRORS++)); }
warn()  { echo -e "${YELLOW}WARN${NC}:  $1"; ((WARNINGS++)); }
pass()  { echo -e "${GREEN}PASS${NC}:  $1"; }

echo -e "${BOLD}=== Engram Validation ===${NC}"
echo "Repository: $REPO"
echo ""

# ─── Approved status values ──────────────────────────────────────────────────
APPROVED_STATUSES="current|draft|future|in-progress|concluded|achieved|abandoned|superseded|planned|active|paused|completed|undertaken|void"

# ─── 1. Frontmatter compliance ──────────────────────────────────────────────
echo -e "${BOLD}--- Frontmatter Compliance ---${NC}"

# Find all leaf .md files (not INDEX.md, not README.md, not template.md, not SKILL.md, not AGENTS.md)
leaf_count=0
leaf_pass=0
while IFS= read -r -d '' file; do
  leaf_count=$((leaf_count + 1))
  rel="${file#$REPO/}"

  # Check for opening ---
  first_line=$(head -1 "$file")
  if [[ "$first_line" != "---" ]]; then
    error "$rel — missing frontmatter (no opening ---)"
    continue
  fi

  # Extract frontmatter block
  fm=$(sed -n '1,/^---$/{ /^---$/d; p; }' "$file" | tail -n +1)

  missing=""
  echo "$fm" | grep -q '^status:' || missing="$missing status"
  echo "$fm" | grep -q '^created:' || missing="$missing created"
  echo "$fm" | grep -q '^updated:' || missing="$missing updated"
  echo "$fm" | grep -q '^tags:' || missing="$missing tags"

  if [[ -n "$missing" ]]; then
    error "$rel — missing frontmatter fields:$missing"
  else
    # Validate status value
    status_val=$(echo "$fm" | grep '^status:' | sed 's/^status:[[:space:]]*//')
    if ! echo "$status_val" | grep -qE "^($APPROVED_STATUSES)$"; then
      error "$rel — invalid status value: '$status_val'"
    else
      leaf_pass=$((leaf_pass + 1))
    fi
  fi
done < <(find "$REPO" -name '*.md' -not -path '*/.git/*' -not -path '*/.agents/*' \
  -not -name 'INDEX.md' -not -name 'README.md' -not -name 'template.md' \
  -not -name 'AGENTS.md' -not -name 'CHANGELOG.md' \
  -not -path '*/.github/*' -not -name 'CONTRIBUTING.md' -not -name 'CODE_OF_CONDUCT.md' -not -name 'SECURITY.md' \
  -print0)

if [[ $leaf_count -eq 0 ]]; then
  warn "No leaf documents found"
else
  pass "Frontmatter: $leaf_pass/$leaf_count leaf documents compliant"
fi
echo ""

# ─── 1b. Skill frontmatter compliance ─────────────────────────────────────────
echo -e "${BOLD}--- Skill Frontmatter Compliance ---${NC}"

skill_count=0
skill_pass=0
while IFS= read -r -d '' file; do
  skill_count=$((skill_count + 1))
  rel="${file#$REPO/}"

  # Check for opening ---
  first_line=$(head -1 "$file")
  if [[ "$first_line" != "---" ]]; then
    error "$rel — missing frontmatter (no opening ---)"
    continue
  fi

  # Extract frontmatter block
  fm=$(sed -n '1,/^---$/{ /^---$/d; p; }' "$file" | tail -n +1)

  missing=""
  echo "$fm" | grep -q '^name:' || missing="$missing name"
  echo "$fm" | grep -q '^description:' || missing="$missing description"

  if [[ -n "$missing" ]]; then
    error "$rel — missing frontmatter fields:$missing"
  else
    skill_pass=$((skill_pass + 1))
  fi
done < <(find "$REPO/.agents/skills" -name 'SKILL.md' -print0 2>/dev/null)

if [[ $skill_count -eq 0 ]]; then
  warn "No skill documents found"
else
  pass "Skills: $skill_pass/$skill_count skill documents compliant"
fi
echo ""

# ─── 2. INDEX consistency — links point to real files ────────────────────────
echo -e "${BOLD}--- INDEX Link Consistency ---${NC}"

index_errors=0
index_checked=0
while IFS= read -r -d '' index_file; do
  index_dir=$(dirname "$index_file")
  rel_index="${index_file#$REPO/}"

  # Extract markdown links: [text](path) — only .md and directory links, skip navigation section
  # We extract all links from the file but filter to only content links (not ../AGENTS.md navigation)
  while IFS= read -r link; do
    [[ -z "$link" ]] && continue
    # Skip navigation links (Parent/Root references to AGENTS.md or parent INDEX)
    [[ "$link" =~ AGENTS\.md$ ]] && continue
    index_checked=$((index_checked + 1))
    # Drop any #anchor, then resolve relative to the INDEX file's directory
    target="$index_dir/${link%%#*}"

    if [[ ! -e "$target" ]]; then
      error "$rel_index — broken link: $link (target not found)"
      index_errors=$((index_errors + 1))
    fi
  done < <(grep -oE '\]\([^)]+\)' "$index_file" 2>/dev/null | sed -E 's/^\]\(//; s/\)$//' | grep -v '^http' | grep -v '^#' || true)

done < <(find "$REPO" -name 'INDEX.md' -not -path '*/.git/*' -not -path '*/.agents/*' -print0)

if [[ $index_checked -eq 0 ]]; then
  warn "No INDEX links found to check"
else
  pass "INDEX links: $((index_checked - index_errors))/$index_checked links resolve"
fi
echo ""

# ─── 3. Orphan detection — files without INDEX entries ───────────────────────
echo -e "${BOLD}--- Orphan Detection ---${NC}"

# Every directory that has an INDEX.md is checked: each .md file beside the
# INDEX (not INDEX/README/template) must be referenced in it. An orphan is an
# error, because a document no index points to is unreachable by navigation.
orphan_count=0
while IFS= read -r -d '' index_file; do
  domain_dir=$(dirname "$index_file")
  domain="${domain_dir#$REPO/}"

  while IFS= read -r -d '' file; do
    name=$(basename "$file")
    if ! grep -qF -- "$name" "$index_file" 2>/dev/null; then
      rel="${file#$REPO/}"
      error "$rel — not referenced in $domain/INDEX.md (orphan)"
      orphan_count=$((orphan_count + 1))
    fi
  done < <(find "$domain_dir" -maxdepth 1 -name '*.md' \
    -not -name 'INDEX.md' -not -name 'README.md' -not -name 'template.md' -print0)
done < <(find "$REPO" -name 'INDEX.md' -not -path '*/.git/*' -not -path '*/.agents/*' -print0)

if [[ $orphan_count -eq 0 ]]; then
  pass "No orphan files detected"
fi
echo ""

# ─── 4. Navigation links — Parent/Root references ───────────────────────────
echo -e "${BOLD}--- Navigation Links ---${NC}"

nav_errors=0
nav_checked=0
while IFS= read -r -d '' index_file; do
  index_dir=$(dirname "$index_file")
  rel_index="${index_file#$REPO/}"

  # Check Parent and Root links
  while IFS= read -r link; do
    nav_checked=$((nav_checked + 1))
    target="$index_dir/$link"
    if [[ ! -f "$target" ]]; then
      error "$rel_index — broken navigation link: $link"
      nav_errors=$((nav_errors + 1))
    fi
  done < <(grep -E '^-[[:space:]]+(Parent|Root):' "$index_file" 2>/dev/null | sed -nE 's/^[^(]*\(([^)#]+).*/\1/p')

done < <(find "$REPO" -name 'INDEX.md' -not -path '*/.git/*' -not -path '*/.agents/*' -print0)

if [[ $nav_checked -eq 0 ]]; then
  warn "No navigation links found to check"
else
  pass "Navigation: $((nav_checked - nav_errors))/$nav_checked links resolve"
fi
echo ""

# ─── Summary ─────────────────────────────────────────────────────────────────
echo -e "${BOLD}=== Summary ===${NC}"
if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
  echo -e "${GREEN}All checks passed.${NC}"
elif [[ $ERRORS -eq 0 ]]; then
  echo -e "${YELLOW}$WARNINGS warning(s), no errors.${NC}"
else
  echo -e "${RED}$ERRORS error(s), $WARNINGS warning(s).${NC}"
fi

exit $ERRORS
