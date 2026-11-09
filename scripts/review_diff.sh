#!/usr/bin/env bash
# Diff hygiene scan for a staged or explicit diff.
#
# Usage:
#   bash scripts/review_diff.sh            # staged changes
#   bash scripts/review_diff.sh --working  # unstaged changes
#   bash scripts/review_diff.sh main...HEAD
#
# Exit code 1 when a blocker-level pattern is found.

set -euo pipefail

if [[ "${1:-}" == "--working" ]]; then
  DIFF=$(git diff)
  LABEL="working tree"
elif [[ -n "${1:-}" ]]; then
  DIFF=$(git diff "$1")
  LABEL="$1"
else
  DIFF=$(git diff --cached)
  LABEL="staged"
fi

if [[ -z "$DIFF" ]]; then
  echo "No diff in $LABEL."
  exit 0
fi

status=0
report() {
  local level="$1" label="$2" pattern="$3"
  local hits
  hits=$(printf '%s\n' "$DIFF" | grep -nE "$pattern" || true)
  if [[ -n "$hits" ]]; then
    echo ""
    echo "[$level] $label"
    printf '%s\n' "$hits" | head -20
    if [[ "$level" == "BLOCKER" ]]; then status=1; fi
  fi
}

echo "Diff hygiene: $LABEL"

report BLOCKER "possible private key" "BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY"
report BLOCKER "possible cloud key" "AKIA[0-9A-Z]{16}"
report BLOCKER "possible generic secret assignment" "(api[_-]?key|secret|password|token)[[:space:]]*[:=][[:space:]]*['\"][^'\"]{8,}"
report BLOCKER "merge conflict marker" "^(<<<<<<<|=======|>>>>>>>)"
report BLOCKER "debug statement" "(console\.log\(|fmt\.Println\(|print\(|debugger;|binding\.pry)"
report MAJOR "TODO or FIXME added" "^\+.*(TODO|FIXME|XXX)"
report MAJOR "commented-out code" "^\+[[:space:]]*//[[:space:]]*(func|const|let|var|return|if|for)"
report MINOR "trailing whitespace" "^\+.*[[:space:]]+$"

echo ""
if [[ "$status" -eq 0 ]]; then
  echo "PASS: no blocker patterns found."
else
  echo "FAIL: blocker patterns found. Review the output above."
fi
exit "$status"
