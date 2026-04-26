from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .weapons import DEFAULT_LOADOUT, WEAPONS

PLAYER_RADIUS = 14.0
PLAYER_MAX_HP = 100.0
MOVE_SPEED = 220.0
AIM_SPEED_PENALTY = 0.45
RESPAWN_DELAY = 3.0


@dataclass
class Player:
    id: int
    name: str
    x: float
    y: float
    angle: float = 0.0
    hp: float = PLAYER_MAX_HP
    alive: bool = True
    respawn_at: float = 0.0
    move_dx: float = 0.0
    move_dy: float = 0.0
    aiming: bool = False
    wants_shoot: bool = False
    wants_reload: bool = False
    loadout: list[str] = field(default_factory=lambda: list(DEFAULT_LOADOUT))
    weapon_idx: int = 0
    ammo: dict[str, int] = field(default_factory=dict)
    last_fire_at: float = 0.0
    reload_done_at: float = 0.0
    reloading: bool = False
    kills: int = 0
    deaths: int = 0
    last_damager: Optional[int] = None
    is_bot: bool = False

    def __post_init__(self) -> None:
        if not self.ammo:
            self.ammo = {w: WEAPONS[w].mag_size for w in self.loadout}

    @property
    def weapon_name(self) -> str:
        return self.loadout[self.weapon_idx]

    @property
    def weapon(self):
        return WEAPONS[self.weapon_name]

    def to_state(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "angle": round(self.angle, 3),
            "hp": round(self.hp, 1),
            "alive": self.alive,
            "weapon": self.weapon_name,
            "ammo": self.ammo[self.weapon_name],
            "mag": self.weapon.mag_size,
            "aiming": self.aiming,
            "reloading": self.reloading,
            "kills": self.kills,
            "deaths": self.deaths,
            "is_bot": self.is_bot,
        }


_proj_id_counter = 0


def _next_proj_id() -> int:
    global _proj_id_counter
    _proj_id_counter += 1
    return _proj_id_counter


@dataclass
class Projectile:
    id: int
    owner_id: int
    x: float
    y: float
    vx: float
    vy: float
    damage: float
    ttl: float = 1.5

    @classmethod
    def create(cls, owner_id: int, x: float, y: float, vx: float, vy: float, damage: float) -> "Projectile":
        return cls(id=_next_proj_id(), owner_id=owner_id, x=x, y=y, vx=vx, vy=vy, damage=damage)

    def to_state(self) -> dict:
        return {
            "id": self.id,
            "owner": self.owner_id,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "vx": round(self.vx, 1),
            "vy": round(self.vy, 1),
        }
