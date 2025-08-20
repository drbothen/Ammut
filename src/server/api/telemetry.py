from typing import Dict, Any

from fastapi import APIRouter, Depends

from src.server.dependencies import get_telemetry_service
from src.server.services.base import AbstractTelemetry

router = APIRouter()


@router.get("/telemetry", tags=["Telemetry"])
async def get_telemetry_stats(
    service: AbstractTelemetry = Depends(get_telemetry_service),
) -> Dict[str, Any]:
    """Returns system and application telemetry data."""
    return await service.get_stats()
