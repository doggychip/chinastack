"""Grid A* pathfinder. Cells are GRID_CELL pixels wide; a cell is blocked if it
intersects any wall (with a small inflate so paths don't graze corners)."""

from __future__ import annotations

import heapq
import math

from . import world
from .world import GRID_CELL, WORLD_HEIGHT, WORLD_WIDTH

COLS = WORLD_WIDTH // GRID_CELL
ROWS = WORLD_HEIGHT // GRID_CELL
INFLATE = 6.0

_blocked: list[list[bool]] | None = None


def _build_grid() -> list[list[bool]]:
    grid = [[False] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            cx = c * GRID_CELL + GRID_CELL / 2
            cy = r * GRID_CELL + GRID_CELL / 2
            grid[r][c] = world.point_in_walls(cx, cy, INFLATE)
    return grid


def grid() -> list[list[bool]]:
    global _blocked
    if _blocked is None:
        _blocked = _build_grid()
    return _blocked


def _cell(x: float, y: float) -> tuple[int, int]:
    c = max(0, min(COLS - 1, int(x // GRID_CELL)))
    r = max(0, min(ROWS - 1, int(y // GRID_CELL)))
    return r, c


def find_path(sx: float, sy: float, tx: float, ty: float) -> list[tuple[float, float]]:
    g = grid()
    start = _cell(sx, sy)
    goal = _cell(tx, ty)
    if g[start[0]][start[1]] or g[goal[0]][goal[1]]:
        return []
    if start == goal:
        return [(tx, ty)]

    open_heap: list[tuple[float, tuple[int, int]]] = [(0.0, start)]
    came: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: dict[tuple[int, int], float] = {start: 0.0}

    neighbors = [
        (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
        (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142),
    ]

    while open_heap:
        _, cur = heapq.heappop(open_heap)
        if cur == goal:
            return _reconstruct(came, cur, tx, ty)
        cr, cc = cur
        for dr, dc, cost in neighbors:
            nr, nc = cr + dr, cc + dc
            if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                continue
            if g[nr][nc]:
                continue
            if dr != 0 and dc != 0 and (g[cr + dr][cc] or g[cr][cc + dc]):
                continue
            tentative = g_score[cur] + cost
            if tentative < g_score.get((nr, nc), float("inf")):
                came[(nr, nc)] = cur
                g_score[(nr, nc)] = tentative
                f = tentative + math.hypot(goal[0] - nr, goal[1] - nc)
                heapq.heappush(open_heap, (f, (nr, nc)))
    return []


def _reconstruct(
    came: dict[tuple[int, int], tuple[int, int]],
    end: tuple[int, int],
    tx: float,
    ty: float,
) -> list[tuple[float, float]]:
    path: list[tuple[float, float]] = []
    cur = end
    while cur in came:
        r, c = cur
        path.append((c * GRID_CELL + GRID_CELL / 2, r * GRID_CELL + GRID_CELL / 2))
        cur = came[cur]
    path.reverse()
    if path:
        path[-1] = (tx, ty)
    return path
