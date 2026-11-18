#!/usr/bin/env bash
set -euo pipefail

script="$(cd "$(dirname "$0")" && pwd)/review_diff.sh"
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
cd "$tmp"
git init -q
printf '%s\n' 'print("total")' > example
git add example
bash "$script"
printf '%s\n' '<<<<<<< HEAD' > example
git add example
if bash "$script"; then
  echo "Expected a staged conflict marker to fail" >&2
  exit 1
fi
git -c user.name=Test -c user.email=test@example.invalid commit -qm fixture
echo 'fixed' > example
git add example
bash "$script"
