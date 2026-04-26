"""Smarter agent: picks weapon by distance, aims when sniping, strafes while
shooting, retreats and reloads when low. Useful as a baseline opponent."""

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
        strafe_dir = 1
        next_strafe_flip = 0.0

        async def send(cmd: str, args: dict | None = None) -> None:
            await ws.send(json.dumps({"cmd": cmd, "args": args or {}}))

        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("type") == "joined":
                me_id = msg["id"]
                print(f"[{name}] id={me_id}")
                continue
            if msg.get("type") != "state":
                continue

            me = next((p for p in msg["players"] if p["id"] == me_id), None)
            if me is None or not me["alive"]:
                continue
            opponents = [p for p in msg["players"] if p["id"] != me_id and p["alive"]]
            if not opponents:
                await send("MOVE", {"dx": 0, "dy": 0})
                continue

            target = min(opponents, key=lambda p: (p["x"] - me["x"]) ** 2 + (p["y"] - me["y"]) ** 2)
            dist = math.hypot(target["x"] - me["x"], target["y"] - me["y"])

            desired = "rifle"
            if dist < 180:
                desired = "shotgun"
            elif dist > 480:
                desired = "sniper"
            if me["weapon"] != desired:
                await send("SWITCH_WEAPON", {"name": desired})

            await send("AIM", {"state": desired == "sniper" and dist > 350})

            angle = math.atan2(target["y"] - me["y"], target["x"] - me["x"])
            await send("LOOK", {"angle": angle})

            if me["hp"] < 30 and me["ammo"] > 0:
                back = angle + math.pi
                await send("MOVE", {"dx": math.cos(back), "dy": math.sin(back)})
                await send("SHOOT", {"hold": True})
                continue

            if me["ammo"] == 0 and not me["reloading"]:
                await send("RELOAD")
                await send("MOVE", {"dx": 0, "dy": 0})
                continue

            if msg["now"] >= next_strafe_flip:
                strafe_dir *= -1
                next_strafe_flip = msg["now"] + random.uniform(0.4, 0.9)
            perp = angle + math.pi / 2
            forward = 0.4 if dist > 220 else (-0.3 if dist < 120 else 0.0)
            mx = math.cos(perp) * strafe_dir + math.cos(angle) * forward
            my = math.sin(perp) * strafe_dir + math.sin(angle) * forward
            mag = math.hypot(mx, my) or 1.0
            await send("MOVE", {"dx": mx / mag, "dy": my / mag})
            await send("SHOOT", {"hold": True})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default=f"chaser-{random.randint(100,999)}")
    ap.add_argument("--server", default="ws://localhost:8000")
    args = ap.parse_args()
    asyncio.run(run(args.name, args.server))


if __name__ == "__main__":
    main()
