#!/usr/bin/env bash
# Pulls the rest of the ad-scorer project (src/, .claude/, tests/, scripts/,
# data/, docs/, creatives/benchmarks/) from doggychip/ad-scorer @ main.
#
# This branch (claude/ad-scorer-setup-wyMBz) inlines the root config + docs.
# Everything else is fetched here to keep the scaffold commit small. Re-run
# any time you want to resync; existing files are overwritten.
#
# Usage: bash scripts/sync-from-upstream.sh [ref]
#   ref defaults to main; pass a commit SHA or tag to pin a specific version.

set -euo pipefail

REF="${1:-main}"
UPSTREAM="https://github.com/doggychip/ad-scorer.git"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "==> Cloning $UPSTREAM @ $REF into $TMP"
git clone --depth 1 --branch "$REF" "$UPSTREAM" "$TMP/src" 2>/dev/null \
  || git clone "$UPSTREAM" "$TMP/src" && git -C "$TMP/src" checkout "$REF"

ROOT="$(git rev-parse --show-toplevel)"
echo "==> Target: $ROOT"

# Copy everything except .git and items already inlined at root.
for item in src tests scripts data docs creatives .claude; do
  if [[ -e "$TMP/src/$item" ]]; then
    echo "==> Copying $item/"
    rm -rf "$ROOT/$item"
    cp -r "$TMP/src/$item" "$ROOT/$item"
  fi
done

# Don't overwrite the scaffold's own copy of this script.
if [[ -f "$ROOT/scripts/sync-from-upstream.sh" ]]; then
  chmod +x "$ROOT/scripts/sync-from-upstream.sh"
fi

# Refresh package-lock.json if missing (recommended) but don't force.
if [[ ! -f "$ROOT/package-lock.json" && -f "$TMP/src/package-lock.json" ]]; then
  echo "==> Copying package-lock.json"
  cp "$TMP/src/package-lock.json" "$ROOT/package-lock.json"
fi

echo "==> Done. Next steps:"
echo "    npm install"
echo "    cp .env.example .env  # set ANTHROPIC_API_KEY"
echo "    npm run score ./path/to/creatives/"
