from typing import Dict, Any

from fastapi import APIRouter, Depends

from src.server.dependencies import get_command_service
from src.server.services.base import AbstractCommandService

router = APIRouter()


@router.get("/cache/stats", tags=["Cache"])
async def get_cache_stats(
    service: AbstractCommandService = Depends(get_command_service),
) -> Dict[str, Any]:
    """Returns statistics about the command cache."""
    return await service.get_stats()


@router.post("/cache/clear", tags=["Cache"])
async def clear_command_cache(
    service: AbstractCommandService = Depends(get_command_service),
) -> Dict[str, Any]:
    """Clears the command cache."""
    return await service.clear_cache()
