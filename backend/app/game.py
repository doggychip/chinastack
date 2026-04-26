from __future__ import annotations

import asyncio
import math
import random
import time
from typing import Awaitable, Callable

from . import commands as cmdmod
from . import world
from .bot import BotController
from .entities import (
    AIM_SPEED_PENALTY,
    MOVE_SPEED,
    PLAYER_MAX_HP,
    PLAYER_RADIUS,
    RESPAWN_DELAY,
    Player,
    Projectile,
)
from .weapons import WEAPONS

TICK_RATE = 20
DT = 1.0 / TICK_RATE
PROJECTILE_RADIUS = 3.0


class Game:
    def __init__(self) -> None:
        self.players: dict[int, Player] = {}
        self.projectiles: list[Projectile] = []
        self.bots: dict[int, BotController] = {}
        self.tick: int = 0
        self.now: float = 0.0
        self._next_id: int = 1
        self._spectators: set[Callable[[dict], Awaitable[None]]] = set()
        self._agent_sinks: dict[int, Callable[[dict], Awaitable[None]]] = {}
        self._loop_task: asyncio.Task | None = None
        self._running: bool = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._loop_task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        self._running = False
        if self._loop_task:
            self._loop_task.cancel()

    def add_spectator(self, sink: Callable[[dict], Awaitable[None]]) -> None:
        self._spectators.add(sink)

    def remove_spectator(self, sink: Callable[[dict], Awaitable[None]]) -> None:
        self._spectators.discard(sink)

    def add_player(
        self,
        name: str,
        sink: Callable[[dict], Awaitable[None]] | None = None,
        is_bot: bool = False,
    ) -> Player:
        pid = self._next_id
        self._next_id += 1
        spawn = self._pick_spawn()
        player = Player(id=pid, name=name, x=spawn.x, y=spawn.y, is_bot=is_bot)
        self.players[pid] = player
        if sink is not None:
            self._agent_sinks[pid] = sink
        if is_bot:
            self.bots[pid] = BotController(player)
        return player

    def remove_player(self, pid: int) -> None:
        self.players.pop(pid, None)
        self.bots.pop(pid, None)
        self._agent_sinks.pop(pid, None)

    def ensure_bots(self, count: int) -> None:
        existing = sum(1 for p in self.players.values() if p.is_bot)
        for i in range(count - existing):
            self.add_player(f"bot-{random.randint(1000, 9999)}", is_bot=True)

    def _pick_spawn(self):
        random.shuffle(world.SPAWNS)
        for s in world.SPAWNS:
            occupied = any(
                p.alive and math.hypot(p.x - s.x, p.y - s.y) < 80
                for p in self.players.values()
            )
            if not occupied:
                return s
        return random.choice(world.SPAWNS)

    def init_payload(self) -> dict:
        return {
            "type": "init",
            "tick_rate": TICK_RATE,
            "world": {
                "width": world.WORLD_WIDTH,
                "height": world.WORLD_HEIGHT,
                "walls": [{"x": w.x, "y": w.y, "w": w.w, "h": w.h} for w in world.WALLS],
                "spawns": [{"x": s.x, "y": s.y} for s in world.SPAWNS],
            },
            "weapons": {
                k: {"damage": v.damage, "mag_size": v.mag_size, "fire_cooldown": v.fire_cooldown}
                for k, v in WEAPONS.items()
            },
        }

    def apply_command(self, pid: int, msg: dict) -> dict | None:
        try:
            cmd, args = cmdmod.parse(msg)
        except cmdmod.CommandError as e:
            return {"type": "error", "message": str(e)}
        p = self.players.get(pid)
        if p is None:
            return {"type": "error", "message": "no player"}
        if not p.alive and cmd not in ("LOOK",):
            return None
        if cmd == "MOVE":
            p.move_dx = args["dx"]
            p.move_dy = args["dy"]
        elif cmd == "LOOK":
            if "angle" in args:
                p.angle = args["angle"]
            else:
                p.angle = math.atan2(args["ty"] - p.y, args["tx"] - p.x)
        elif cmd == "SHOOT":
            p.wants_shoot = args["hold"]
        elif cmd == "RELOAD":
            p.wants_reload = True
        elif cmd == "SWITCH_WEAPON":
            self._switch(p, args)
        elif cmd == "AIM":
            p.aiming = args["state"]
        return None

    def _switch(self, p: Player, args: dict) -> None:
        if p.reloading:
            return
        if "slot" in args:
            slot = args["slot"]
            if 0 <= slot < len(p.loadout):
                p.weapon_idx = slot
        elif "name" in args:
            try:
                p.weapon_idx = p.loadout.index(args["name"])
            except ValueError:
                pass

    async def _loop(self) -> None:
        last = time.perf_counter()
        while self._running:
            target = last + DT
            now = time.perf_counter()
            if now < target:
                await asyncio.sleep(target - now)
            last = time.perf_counter()
            self.now += DT
            self.tick += 1
            try:
                self._step()
                await self._broadcast()
            except Exception as e:
                print(f"[game] tick error: {e}")

    def _step(self) -> None:
        for ctrl in list(self.bots.values()):
            ctrl.tick(self, DT)
        for p in self.players.values():
            self._update_player(p)
        self._update_projectiles()
        self._respawn_dead()

    def _update_player(self, p: Player) -> None:
        if not p.alive:
            return
        speed = MOVE_SPEED * (AIM_SPEED_PENALTY if p.aiming else 1.0)
        nx = p.x + p.move_dx * speed * DT
        ny = p.y + p.move_dy * speed * DT
        if not self._collides(nx, p.y):
            p.x = nx
        if not self._collides(p.x, ny):
            p.y = ny

        if p.reloading and self.now >= p.reload_done_at:
            p.ammo[p.weapon_name] = p.weapon.mag_size
            p.reloading = False

        if p.wants_reload and not p.reloading:
            w = p.weapon
            if p.ammo[p.weapon_name] < w.mag_size:
                p.reloading = True
                p.reload_done_at = self.now + w.reload_time
            p.wants_reload = False

        if p.wants_shoot and not p.reloading:
            self._try_fire(p)

    def _collides(self, x: float, y: float) -> bool:
        if x < PLAYER_RADIUS or x > world.WORLD_WIDTH - PLAYER_RADIUS:
            return True
        if y < PLAYER_RADIUS or y > world.WORLD_HEIGHT - PLAYER_RADIUS:
            return True
        return world.point_in_walls(x, y, PLAYER_RADIUS)

    def _try_fire(self, p: Player) -> None:
        w = p.weapon
        if self.now - p.last_fire_at < w.fire_cooldown:
            return
        if p.ammo[p.weapon_name] <= 0:
            return
        p.last_fire_at = self.now
        if not w.infinite_ammo:
            p.ammo[p.weapon_name] -= 1
        else:
            p.ammo[p.weapon_name] = max(0, p.ammo[p.weapon_name] - 1)
            if p.ammo[p.weapon_name] == 0:
                p.ammo[p.weapon_name] = w.mag_size

        spread = w.spread * (0.3 if p.aiming else 1.0)
        for _ in range(w.pellets):
            a = p.angle + (random.random() - 0.5) * spread * 2
            vx = math.cos(a) * w.projectile_speed
            vy = math.sin(a) * w.projectile_speed
            ox = p.x + math.cos(a) * (PLAYER_RADIUS + 4)
            oy = p.y + math.sin(a) * (PLAYER_RADIUS + 4)
            self.projectiles.append(
                Projectile.create(p.id, ox, oy, vx, vy, w.damage)
            )

    def _update_projectiles(self) -> None:
        survivors: list[Projectile] = []
        for proj in self.projectiles:
            steps = 4
            sub_dt = DT / steps
            hit = False
            for _ in range(steps):
                proj.x += proj.vx * sub_dt
                proj.y += proj.vy * sub_dt
                if world.point_in_walls(proj.x, proj.y, PROJECTILE_RADIUS):
                    hit = True
                    break
                if (
                    proj.x < 0 or proj.x > world.WORLD_WIDTH
                    or proj.y < 0 or proj.y > world.WORLD_HEIGHT
                ):
                    hit = True
                    break
                target = self._projectile_hit_player(proj)
                if target is not None:
                    self._apply_damage(proj.owner_id, target, proj.damage)
                    hit = True
                    break
            proj.ttl -= DT
            if not hit and proj.ttl > 0:
                survivors.append(proj)
        self.projectiles = survivors

    def _projectile_hit_player(self, proj: Projectile) -> Player | None:
        for p in self.players.values():
            if not p.alive or p.id == proj.owner_id:
                continue
            if (proj.x - p.x) ** 2 + (proj.y - p.y) ** 2 <= (PLAYER_RADIUS + PROJECTILE_RADIUS) ** 2:
                return p
        return None

    def _apply_damage(self, attacker_id: int, target: Player, dmg: float) -> None:
        target.hp -= dmg
        target.last_damager = attacker_id
        if target.hp <= 0:
            target.hp = 0
            target.alive = False
            target.deaths += 1
            target.respawn_at = self.now + RESPAWN_DELAY
            killer = self.players.get(attacker_id)
            if killer is not None and killer.id != target.id:
                killer.kills += 1

    def _respawn_dead(self) -> None:
        for p in self.players.values():
            if not p.alive and self.now >= p.respawn_at:
                spawn = self._pick_spawn()
                p.x, p.y = spawn.x, spawn.y
                p.hp = PLAYER_MAX_HP
                p.alive = True
                p.ammo = {w: WEAPONS[w].mag_size for w in p.loadout}
                p.reloading = False
                p.weapon_idx = 0
                p.move_dx = p.move_dy = 0.0
                p.wants_shoot = False

    async def _broadcast(self) -> None:
        snapshot = {
            "type": "state",
            "tick": self.tick,
            "now": round(self.now, 3),
            "players": [p.to_state() for p in self.players.values()],
            "projectiles": [pr.to_state() for pr in self.projectiles],
        }
        for sink in list(self._spectators):
            try:
                await sink(snapshot)
            except Exception:
                self._spectators.discard(sink)
        for pid, sink in list(self._agent_sinks.items()):
            payload = dict(snapshot)
            payload["you"] = pid
            try:
                await sink(payload)
            except Exception:
                self._agent_sinks.pop(pid, None)


game = Game()
