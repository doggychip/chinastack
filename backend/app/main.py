import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.seed import seed_technologies, seed_sites
from app.routers import lookup, sites, technologies, stats, export

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger("chinastack")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB and seed technologies
    await init_db()
    await seed_technologies()
    logger.info("Database initialized, technologies loaded")

    # Run seed scan in background (don't block startup)
    task = asyncio.create_task(seed_sites())

    yield

    # Shutdown
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="ChinaStack",
    description="Technology profiler for Chinese websites — 建站雷达",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lookup.router)
app.include_router(sites.router)
app.include_router(technologies.router)
app.include_router(stats.router)
app.include_router(export.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "chinastack"}
