from fastapi import FastAPI

from core.config import settings
from core.logging import logger
from src.server.dependencies import get_visual_engine_service
from api import routers

app = FastAPI(
    title="Ammut FastAPI Server",
    description="A modular and extensible security testing framework.",
    version="0.1.0"
)

# Include API routers from the api module
for router in routers:
    app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    visual_engine = get_visual_engine_service()
    print(visual_engine.create_banner())
    logger.info("Ammut server startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Ammut server...")
