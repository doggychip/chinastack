"""Minimal random-walk agent. Connects, picks the nearest opponent, faces them,
and fires whenever it has line-of-sight (approximated as "anyone alive").

Usage:
    pip install websockets
    python test/python/single_agent.py [--name WALKER] [--server ws://localhost:8000]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import random

import websockets


async def run(name: str, server: str) -> None:
    url = f"{server}/ws/agent/{name}"
    async with websockets.connect(url) as ws:
        me_id: int | None = None
        next_dir_change = 0.0
        dx = dy = 0.0

        async def send(cmd: str, args: dict | None = None) -> None:
            await ws.send(json.dumps({"cmd": cmd, "args": args or {}}))

        async for raw in ws:
            msg = json.loads(raw)
            t = msg.get("type")
            if t == "joined":
                me_id = msg["id"]
                print(f"[{name}] joined as id={me_id}")
                continue
            if t != "state":
                continue

            me = next((p for p in msg["players"] if p["id"] == me_id), None)
            if me is None or not me["alive"]:
                continue

            opponents = [p for p in msg["players"] if p["id"] != me_id and p["alive"]]
            if opponents:
                target = min(opponents, key=lambda p: (p["x"] - me["x"]) ** 2 + (p["y"] - me["y"]) ** 2)
                angle = math.atan2(target["y"] - me["y"], target["x"] - me["x"])
                await send("LOOK", {"angle": angle})
                await send("SHOOT", {"hold": True})

            now = msg["now"]
            if now >= next_dir_change:
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)
                next_dir_change = now + random.uniform(0.6, 1.6)
                await send("MOVE", {"dx": dx, "dy": dy})

            if me["ammo"] == 0 and not me["reloading"]:
                await send("RELOAD")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=f"walker-{random.randint(100,999)}")
    ap.add_argument("--server", default="ws://localhost:8000")
    args = ap.parse_args()
    asyncio.run(run(args.name, args.server))


if __name__ == "__main__":
    main()
