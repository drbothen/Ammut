from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Path

from src.server.dependencies import get_process_manager_service
from src.server.services.base import AbstractProcessManager

router = APIRouter()


@router.get("/processes/list", tags=["Process Management"])
async def list_all_processes(
    service: AbstractProcessManager = Depends(get_process_manager_service),
) -> List[Dict[str, Any]]:
    """Lists all active processes."""
    return await service.list_processes()


@router.get("/processes/status/{pid}", tags=["Process Management"])
async def get_process_status(
    pid: int = Path(..., title="Process ID"),
    service: AbstractProcessManager = Depends(get_process_manager_service),
) -> Dict[str, Any]:
    """Gets the status of a specific process."""
    return await service.get_process_status(pid)


@router.post("/processes/terminate/{pid}", tags=["Process Management"])
async def terminate_a_process(
    pid: int = Path(..., title="Process ID"),
    service: AbstractProcessManager = Depends(get_process_manager_service),
) -> Dict[str, Any]:
    """Terminates a specific process."""
    return await service.terminate_process(pid)


@router.post("/processes/pause/{pid}", tags=["Process Management"])
async def pause_a_process(
    pid: int = Path(..., title="Process ID"),
    service: AbstractProcessManager = Depends(get_process_manager_service),
) -> Dict[str, Any]:
    """Pauses a specific process."""
    return await service.pause_process(pid)


@router.post("/processes/resume/{pid}", tags=["Process Management"])
async def resume_a_process(
    pid: int = Path(..., title="Process ID"),
    service: AbstractProcessManager = Depends(get_process_manager_service),
) -> Dict[str, Any]:
    """Resumes a paused process."""
    return await service.resume_process(pid)
