# AI Battle Arena

A 2D top-down deathmatch arena with **no human input** — every character is
controlled by a programmatic agent over a WebSocket API. The browser is a
spectator. Inspired by
[kandeng/AI-Controlled-battle-game](https://github.com/kandeng/AI-Controlled-battle-game).

- Server-authoritative game loop at 20 Hz (FastAPI + asyncio).
- Identical command protocol for built-in bots and external agents.
- Grid A* pathfinding, weapon switching, line-of-sight checks, projectile physics.
- Sample agents in Python and JS.

## Quick start

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 2. Frontend (separate terminal)
cd frontend
npm install
npm run dev    # open http://localhost:5173

# 3. (Optional) attach an external agent
pip install websockets
python test/python/chase_agent.py --name chaser
```

## Command protocol

Agents connect to `ws://localhost:8000/ws/agent/<name>` and exchange JSON.

| Direction      | Message                                 |
|----------------|-----------------------------------------|
| server → agent | `init`, `joined`, `state`, `error`      |
| agent → server | `MOVE`, `LOOK`, `SHOOT`, `RELOAD`, `SWITCH_WEAPON`, `AIM` |

Each command looks like `{"cmd": "MOVE", "args": {"dx": 1, "dy": 0}}`.
See [`backend/app/commands.py`](backend/app/commands.py) for the full schema and
[`test/python/chase_agent.py`](test/python/chase_agent.py) for a worked example.

## Why

The Unity reference repo is a 3D FPS testbed for AI control. This is a
browser-friendly port: same control philosophy, but reachable from any language
that speaks WebSocket + JSON, and easy to fork into RL/LLM agent experiments.

## Docker

```bash
docker compose up --build
# Frontend on http://localhost:3000, backend on :8000
```
