"""Built-in bot AI: a simple FSM (PATROL / CHASE / ATTACK / RELOAD) that picks
a target, paths to it via A*, and shoots when in line of sight. Provides
out-of-the-box opponents so the arena isn't empty."""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

from . import pathfinding, world
from .entities import Player

if TYPE_CHECKING:
    from .game import Game


class BotController:
    def __init__(self, player: Player) -> None:
        self.player = player
        self.state: str = "PATROL"
        self.path: list[tuple[float, float]] = []
        self.target_id: int | None = None
        self.next_repath_at: float = 0.0
        self.patrol_target: tuple[float, float] | None = None

    def _pick_target(self, game: "Game") -> Player | None:
        candidates = [
            p for p in game.players.values()
            if p.id != self.player.id and p.alive and not (p.is_bot and self.player.is_bot)
        ]
        if not candidates:
            candidates = [p for p in game.players.values() if p.id != self.player.id and p.alive]
        if not candidates:
            return None
        return min(candidates, key=lambda p: (p.x - self.player.x) ** 2 + (p.y - self.player.y) ** 2)

    def _has_los(self, target: Player) -> bool:
        return not world.segment_blocked(self.player.x, self.player.y, target.x, target.y)

    def _random_patrol(self) -> tuple[float, float]:
        for _ in range(20):
            x = random.uniform(64, world.WORLD_WIDTH - 64)
            y = random.uniform(64, world.WORLD_HEIGHT - 64)
            if not world.point_in_walls(x, y, 16):
                return x, y
        return self.player.x, self.player.y

    def tick(self, game: "Game", dt: float) -> None:
        me = self.player
        if not me.alive:
            me.move_dx = me.move_dy = 0.0
            me.wants_shoot = False
            return

        target = self._pick_target(game)
        if target is None:
            self.state = "PATROL"
        else:
            dist = math.hypot(target.x - me.x, target.y - me.y)
            los = self._has_los(target)
            if los and dist < 520:
                self.state = "ATTACK"
                self.target_id = target.id
            elif target is not None:
                self.state = "CHASE"
                self.target_id = target.id

        if me.ammo[me.weapon_name] == 0 and not me.reloading:
            me.wants_reload = True

        if self.state == "ATTACK" and target is not None:
            me.angle = math.atan2(target.y - me.y, target.x - me.x)
            jitter = (random.random() - 0.5) * 0.05
            me.angle += jitter
            me.wants_shoot = me.ammo[me.weapon_name] > 0
            strafe = math.sin(game.now * 2.0 + me.id)
            perp = me.angle + math.pi / 2
            me.move_dx = math.cos(perp) * strafe * 0.8
            me.move_dy = math.sin(perp) * strafe * 0.8
            return

        me.wants_shoot = False

        if self.state == "CHASE" and target is not None:
            if game.now >= self.next_repath_at or not self.path:
                self.path = pathfinding.find_path(me.x, me.y, target.x, target.y)
                self.next_repath_at = game.now + 0.5
        else:
            if not self.path or game.now >= self.next_repath_at:
                self.patrol_target = self._random_patrol()
                self.path = pathfinding.find_path(me.x, me.y, *self.patrol_target)
                self.next_repath_at = game.now + 3.0

        if self.path:
            wx, wy = self.path[0]
            dx = wx - me.x
            dy = wy - me.y
            d = math.hypot(dx, dy)
            if d < 12:
                self.path.pop(0)
                me.move_dx = me.move_dy = 0.0
            else:
                me.move_dx = dx / d
                me.move_dy = dy / d
                me.angle = math.atan2(dy, dx)
        else:
            me.move_dx = me.move_dy = 0.0
