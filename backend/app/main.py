from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .game import game

DEFAULT_BOTS = int(os.environ.get("BATTLE_BOTS", "3"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    game.ensure_bots(DEFAULT_BOTS)
    await game.start()
    try:
        yield
    finally:
        await game.stop()


app = FastAPI(title="AI Battle Game", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {
        "ok": True,
        "tick": game.tick,
        "players": len(game.players),
        "bots": len(game.bots),
    }


@app.get("/api/init")
async def api_init() -> dict:
    return game.init_payload()


@app.websocket("/ws/spectator")
async def ws_spectator(ws: WebSocket) -> None:
    await ws.accept()

    async def sink(msg: dict) -> None:
        await ws.send_text(json.dumps(msg))

    await sink(game.init_payload())
    game.add_spectator(sink)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        game.remove_spectator(sink)


@app.websocket("/ws/agent/{name}")
async def ws_agent(ws: WebSocket, name: str) -> None:
    await ws.accept()

    async def sink(msg: dict) -> None:
        await ws.send_text(json.dumps(msg))

    player = game.add_player(name=name[:24] or "anon", sink=sink)
    await sink(game.init_payload())
    await sink({"type": "joined", "id": player.id, "name": player.name})

    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await sink({"type": "error", "message": "invalid JSON"})
                continue
            err = game.apply_command(player.id, msg)
            if err is not None:
                await sink(err)
    except WebSocketDisconnect:
        pass
    finally:
        game.remove_player(player.id)
