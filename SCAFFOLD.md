# Ad-scorer scaffold notes

This branch (`claude/ad-scorer-setup-wyMBz`) scaffolds the
[doggychip/ad-scorer](https://github.com/doggychip/ad-scorer) project
alongside the existing chinastack `backend/` and `frontend/` directories.

## What's inlined directly

These files are committed verbatim on this branch:

- `package.json`, `tsconfig.json`, `vitest.config.ts`
- `.env.example`, `.gitignore` (merged with chinastack's Python/IDE patterns)
- `brand-dna.json` — locked visual identity spec
- `README.md`, `CLAUDE.md`, `CLAUDE-CODE-USAGE.md` — project docs
- `CHINASTACK.md` — the original chinastack project context, preserved
- `scripts/sync-from-upstream.sh` — fetches the rest

## What's fetched on demand

The TypeScript source (`src/`, ~3800 lines across 18 files), tests, Claude
Code config (`.claude/`), docs, data, and creatives folders are pulled
from the upstream repo via:

```bash
bash scripts/sync-from-upstream.sh
```

This avoids bloating the scaffold commit with code that's faithfully
mirrored upstream. The script supports pinning to a specific ref:

```bash
bash scripts/sync-from-upstream.sh 2933d46    # pin to a commit
bash scripts/sync-from-upstream.sh v0.1.0      # pin to a tag
```

## End-to-end setup

```bash
# 1. Sync the rest of the project from upstream
bash scripts/sync-from-upstream.sh

# 2. Install deps
npm install

# 3. Configure
cp .env.example .env
# edit .env — set ANTHROPIC_API_KEY

# 4. Try it
npm run score ./creatives/benchmarks/
npm run report
```

## Why a sync script instead of full inline?

The scaffold-here branch was generated through a session where pushing
large binary content (sample creative JPGs) and ~50KB of TypeScript via
the available tooling would have ballooned the commit. The sync script
is idempotent and gets you to the same end state.

If you want a fully self-contained branch with every file inlined, the
simplest path is to run the sync script locally, then `git add -A &&
git commit -m 'inline full ad-scorer source'` and push.
