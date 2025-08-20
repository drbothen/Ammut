from typing import Dict, Any

from fastapi import APIRouter, Depends

from src.server.dependencies import get_command_service
from src.server.models.schemas import CommandRequest
from src.server.services.base import AbstractCommandService

router = APIRouter()


@router.post("/command", tags=["Command"])
async def execute_command(
    request: CommandRequest,
    service: AbstractCommandService = Depends(get_command_service),
) -> Dict[str, Any]:
    """Executes a shell command and returns the output."""
    return await service.execute(request.command)
