#!/bin/bash
# Hurmoz Skill Linter — checks all 63 skills for quality issues
# Run: bash lint.sh
# Exit 0 = all pass, Exit 1 = failures found

set -euo pipefail

RED='\033[0;31m'
YEL='\033[0;33m'
GRN='\033[0;32m'
DIM='\033[0;90m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0
ERRORS=""

check_skill() {
  local dir="$1"
  local file="$dir/SKILL.md"
  local name=$(basename "$dir")
  local issues=""
  local severity="PASS"

  # Skip non-skill directories
  [ ! -f "$file" ] && return

  # 1. Frontmatter check
  if ! head -1 "$file" | grep -q "^---"; then
    issues+="  FAIL: missing YAML frontmatter\n"
    severity="FAIL"
  fi

  # 2. Required fields
  for field in "name:" "description:" "version:" "author:" "license:" "platforms:"; do
    if ! head -20 "$file" | grep -q "$field"; then
      issues+="  FAIL: missing field: $field\n"
      severity="FAIL"
    fi
  done

  # 3. Word count
  local words=$(wc -w < "$file" | tr -d ' ')
  if [ "$words" -lt 150 ]; then
    issues+="  FAIL: only $words words (minimum 150)\n"
    severity="FAIL"
  elif [ "$words" -lt 200 ]; then
    issues+="  WARN: only $words words (recommended 200+)\n"
    [ "$severity" = "PASS" ] && severity="WARN"
  fi

  # 4. Arabic content check (use python for Unicode on macOS)
  if ! python3 -c "
import sys
text = open('$file', encoding='utf-8').read()
has_arabic = any('\u0600' <= c <= '\u06FF' for c in text)
sys.exit(0 if has_arabic else 1)
" 2>/dev/null; then
    issues+="  FAIL: no Arabic text found\n"
    severity="FAIL"
  fi

  # 5. Env var drift — check body vars vs frontmatter
  local body_vars=$(grep -oE '\$\{?[A-Z][A-Z_]{2,}\}?' "$file" | sed 's/[${}]//g' | sort -u)
  local front_vars=$(head -20 "$file" | grep "env_vars:" | grep -oE '[A-Z][A-Z_]{2,}' | sort -u)
  for var in $body_vars; do
    # Skip common non-env patterns
    [[ "$var" =~ ^(GET|POST|PUT|DELETE|HEAD|OPTIONS|JSON|XML|HTML|URL|API|SDK|CLI|TTS|STT|OCR|NLP|RAG|PDF|CSV|SQL|SSH|TLS|SSL|DNS|HTTP|HTTPS|CORS|CSRF|IBAN|SWIFT|SAR|USD|EUR|MAD|SAU|UAE|EGP|HIJRI|DIGEST|HOME|PATH|LANG|USER|TERM|SHELL|PWD|OLDPWD|CITY|COUNTRY|QUERY|DATE|TEXT|FILE|DIR|NAME|TYPE|FORMAT|OUTPUT|INPUT|MODEL|LANGUAGE)$ ]] && continue
    if ! echo "$front_vars" | grep -q "^${var}$" 2>/dev/null; then
      # Check if it's actually in env_vars line
      if ! head -20 "$file" | grep "env_vars:" | grep -q "$var"; then
        issues+="  WARN: \$$var used in body but not in env_vars\n"
        [ "$severity" = "PASS" ] && severity="WARN"
      fi
    fi
  done

  # 6. Duplicate name check (handled at repo level)

  # 7. Hardcoded secrets check
  if grep -qE '(sk-[a-zA-Z0-9]{20,}|Bearer [a-zA-Z0-9]{20,}|password["\s]*[:=]["\s]*["\x27][^"\x27]{8,})' "$file" 2>/dev/null; then
    issues+="  FAIL: possible hardcoded secret detected\n"
    severity="FAIL"
  fi

  # 8. Tags check
  if ! head -20 "$file" | grep -q "tags:"; then
    issues+="  WARN: missing tags\n"
    [ "$severity" = "PASS" ] && severity="WARN"
  fi

  # Report
  case "$severity" in
    PASS) PASS=$((PASS+1)); echo -e "${GRN}PASS${NC} $name ${DIM}($words words)${NC}" ;;
    WARN) WARN=$((WARN+1)); echo -e "${YEL}WARN${NC} $name ${DIM}($words words)${NC}"; echo -e "$issues" ;;
    FAIL) FAIL=$((FAIL+1)); echo -e "${RED}FAIL${NC} $name ${DIM}($words words)${NC}"; echo -e "$issues"; ERRORS+="$name " ;;
  esac
}

echo "Hurmoz Skill Linter"
echo "==================="
echo ""

# Check all skill directories
for dir in */; do
  dir="${dir%/}"
  [ "$dir" = "TEMPLATE.md" ] && continue
  [ "$dir" = "DESCRIPTION.md" ] && continue
  [ ! -d "$dir" ] && continue
  check_skill "$dir"
done

echo ""
echo "==================="
echo -e "Results: ${GRN}$PASS PASS${NC} / ${YEL}$WARN WARN${NC} / ${RED}$FAIL FAIL${NC}"
echo "Total: $((PASS + WARN + FAIL)) skills"

if [ -n "$ERRORS" ]; then
  echo ""
  echo -e "${RED}Failing skills: $ERRORS${NC}"
fi

[ "$FAIL" -gt 0 ] && exit 1
exit 0

# Accepted exceptions (documented, not bugs)
# saudi-address: 182 words — concise API reference, intentionally short
# saudi-identity: $YOUR_NAFATH_BASE_URL / $YOUR_YAKEEN_BASE_URL — intentional
#   placeholders for licensed-access APIs, not env vars to declare
