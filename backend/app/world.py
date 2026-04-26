from dataclasses import dataclass


@dataclass(frozen=True)
class Wall:
    x: float
    y: float
    w: float
    h: float

    def contains(self, px: float, py: float, radius: float = 0.0) -> bool:
        return (
            self.x - radius <= px <= self.x + self.w + radius
            and self.y - radius <= py <= self.y + self.h + radius
        )


@dataclass(frozen=True)
class Spawn:
    x: float
    y: float


WORLD_WIDTH = 1280
WORLD_HEIGHT = 960
GRID_CELL = 32

WALLS: list[Wall] = [
    Wall(0, 0, WORLD_WIDTH, 16),
    Wall(0, WORLD_HEIGHT - 16, WORLD_WIDTH, 16),
    Wall(0, 0, 16, WORLD_HEIGHT),
    Wall(WORLD_WIDTH - 16, 0, 16, WORLD_HEIGHT),
    Wall(200, 200, 200, 32),
    Wall(880, 200, 200, 32),
    Wall(200, 728, 200, 32),
    Wall(880, 728, 200, 32),
    Wall(560, 320, 32, 320),
    Wall(688, 320, 32, 320),
    Wall(400, 480, 160, 32),
    Wall(720, 480, 160, 32),
    Wall(304, 416, 32, 128),
    Wall(944, 416, 32, 128),
]

SPAWNS: list[Spawn] = [
    Spawn(96, 96),
    Spawn(WORLD_WIDTH - 96, 96),
    Spawn(96, WORLD_HEIGHT - 96),
    Spawn(WORLD_WIDTH - 96, WORLD_HEIGHT - 96),
    Spawn(WORLD_WIDTH / 2, 96),
    Spawn(WORLD_WIDTH / 2, WORLD_HEIGHT - 96),
    Spawn(96, WORLD_HEIGHT / 2),
    Spawn(WORLD_WIDTH - 96, WORLD_HEIGHT / 2),
]


def point_in_walls(x: float, y: float, radius: float = 0.0) -> bool:
    return any(w.contains(x, y, radius) for w in WALLS)


def segment_blocked(x1: float, y1: float, x2: float, y2: float, steps: int = 24) -> bool:
    for i in range(1, steps + 1):
        t = i / steps
        if point_in_walls(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t):
            return True
    return False
