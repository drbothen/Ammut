from typing import Dict, Any

from fastapi import APIRouter, Depends

from src.server.dependencies import get_file_system_service
from src.server.models.schemas import FileRequest, FileContentRequest
from src.server.services.base import AbstractFileSystem

router = APIRouter()


@router.post("/files/create", tags=["File System"])
async def create_file(
    request: FileContentRequest,
    service: AbstractFileSystem = Depends(get_file_system_service),
) -> Dict[str, Any]:
    """Creates a new file with the given content."""
    return await service.create_file(request.path, request.content)


@router.post("/files/modify", tags=["File System"])
async def modify_file(
    request: FileContentRequest,
    service: AbstractFileSystem = Depends(get_file_system_service),
) -> Dict[str, Any]:
    """Modifies an existing file with the given content."""
    return await service.modify_file(request.path, request.content)


@router.delete("/files/delete", tags=["File System"])
async def delete_file(
    request: FileRequest, service: AbstractFileSystem = Depends(get_file_system_service)
) -> Dict[str, Any]:
    """Deletes a file or directory."""
    return await service.delete_path(request.path)


@router.get("/files/list", tags=["File System"])
async def list_files(
    path: str, service: AbstractFileSystem = Depends(get_file_system_service)
) -> Dict[str, Any]:
    """Lists files in a directory."""
    return await service.list_files(path)
