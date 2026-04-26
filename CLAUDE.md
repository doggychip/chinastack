# AI Battle Game — Build Spec

## What This Is

A web port of [kandeng/AI-Controlled-battle-game](https://github.com/kandeng/AI-Controlled-battle-game) — a 2D top-down arena where there is **no human input**: every player is controlled programmatically through a WebSocket command API. The browser acts as a spectator only.

It's a testbed for AI agents (rule-based, RL, LLM, anything) to fight each other in a deterministic, server-authoritative environment.

## Tech Stack

- **Backend**: FastAPI + asyncio + websockets, single-process server-authoritative tick loop at 20 Hz.
- **Frontend**: React 18 + Vite + TypeScript + Tailwind, Canvas2D renderer.
- **Agents**: anything that speaks WebSocket + JSON. Sample Python and JS agents in `test/`.

## Ports

- Backend: `8000`
- Frontend dev: `5173` (proxies `/api` and `/ws` to backend)
- Frontend prod (docker): `3000`

## Command Protocol

Agents connect to `ws://<host>:8000/ws/agent/<name>` and exchange JSON.

Server → agent:
- `init` — world dimensions, walls, spawn points, weapon stats.
- `joined` — assigned `id`.
- `state` — every tick: `players[]`, `projectiles[]`, plus `you` (your id).
- `error` — bad command.

Agent → server (one of):
- `MOVE { dx, dy }` — movement vector, auto-normalized.
- `LOOK { angle }` or `LOOK { tx, ty }` — face an angle or a world-space point.
- `SHOOT { hold: bool }` — start/stop firing.
- `RELOAD {}` — reload current weapon.
- `SWITCH_WEAPON { slot }` or `{ name }`.
- `AIM { state: bool }` — scope (slower movement, tighter spread).

## Layout

```
backend/app/
  main.py          FastAPI app + WebSocket endpoints
  game.py          Game class, 20 Hz tick loop, broadcast
  world.py         Arena layout, walls, spawns
  entities.py      Player, Projectile
  weapons.py       Weapon table (pistol/rifle/sniper/shotgun)
  commands.py      Command parser/validator
  pathfinding.py   Grid A*
  bot.py           Built-in FSM bot (PATROL/CHASE/ATTACK)
frontend/src/
  App.tsx, Arena.tsx, Scoreboard.tsx, useArenaSocket.ts
test/
  python/single_agent.py      random-walker baseline
  python/chase_agent.py       weapon-switching, strafing
  javascript/agent.js         JS sample
```

## Running

```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev   # http://localhost:5173

# Spawn a couple of agents
python test/python/single_agent.py --name walker
python test/python/chase_agent.py --name chaser
```

`BATTLE_BOTS=N` env var on the backend sets how many built-in bots populate an empty arena (default 3).
