from dataclasses import dataclass


@dataclass(frozen=True)
class Weapon:
    name: str
    damage: float
    fire_cooldown: float
    reload_time: float
    mag_size: int
    projectile_speed: float
    spread: float
    pellets: int = 1
    infinite_ammo: bool = False


WEAPONS: dict[str, Weapon] = {
    "pistol": Weapon(
        name="pistol",
        damage=18,
        fire_cooldown=0.28,
        reload_time=1.1,
        mag_size=12,
        projectile_speed=900,
        spread=0.02,
        infinite_ammo=True,
    ),
    "rifle": Weapon(
        name="rifle",
        damage=14,
        fire_cooldown=0.09,
        reload_time=2.0,
        mag_size=30,
        projectile_speed=1100,
        spread=0.04,
    ),
    "sniper": Weapon(
        name="sniper",
        damage=85,
        fire_cooldown=1.2,
        reload_time=2.6,
        mag_size=5,
        projectile_speed=1600,
        spread=0.005,
    ),
    "shotgun": Weapon(
        name="shotgun",
        damage=11,
        fire_cooldown=0.85,
        reload_time=2.4,
        mag_size=6,
        projectile_speed=850,
        spread=0.18,
        pellets=7,
    ),
}

DEFAULT_LOADOUT = ["pistol", "rifle", "sniper", "shotgun"]
