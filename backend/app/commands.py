"""Agent command schema. Mirrors the protocol from the Unity reference repo:
MOVE / LOOK / SHOOT / RELOAD / SWITCH_WEAPON / AIM."""

from __future__ import annotations

import math
from typing import Any


class CommandError(ValueError):
    pass


def _f(v: Any, name: str) -> float:
    try:
        return float(v)
    except (TypeError, ValueError) as e:
        raise CommandError(f"{name} must be a number") from e


def parse(msg: dict) -> tuple[str, dict]:
    cmd = msg.get("cmd")
    if not isinstance(cmd, str):
        raise CommandError("missing 'cmd'")
    cmd = cmd.upper()
    args = msg.get("args") or {}
    if not isinstance(args, dict):
        raise CommandError("'args' must be an object")

    if cmd == "MOVE":
        dx = _f(args.get("dx", 0), "dx")
        dy = _f(args.get("dy", 0), "dy")
        mag = math.hypot(dx, dy)
        if mag > 1.0:
            dx /= mag
            dy /= mag
        return cmd, {"dx": dx, "dy": dy}

    if cmd == "LOOK":
        if "angle" in args:
            return cmd, {"angle": _f(args["angle"], "angle")}
        if "tx" in args and "ty" in args:
            return cmd, {"tx": _f(args["tx"], "tx"), "ty": _f(args["ty"], "ty")}
        raise CommandError("LOOK requires 'angle' or ('tx','ty')")

    if cmd == "SHOOT":
        return cmd, {"hold": bool(args.get("hold", True))}

    if cmd == "RELOAD":
        return cmd, {}

    if cmd == "SWITCH_WEAPON":
        if "slot" in args:
            return cmd, {"slot": int(args["slot"])}
        if "name" in args:
            return cmd, {"name": str(args["name"])}
        raise CommandError("SWITCH_WEAPON requires 'slot' or 'name'")

    if cmd == "AIM":
        return cmd, {"state": bool(args.get("state", True))}

    raise CommandError(f"unknown command '{cmd}'")
