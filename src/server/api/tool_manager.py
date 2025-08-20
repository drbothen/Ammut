from fastapi import APIRouter, Depends, HTTPException
from typing import List

from pydantic import BaseModel

from src.server.services.base import ToolManagerServiceBase
from src.server.dependencies import get_tool_manager_service

router = APIRouter(
    prefix="/tool-manager",
    tags=["tool-manager"],
)

class ToolCommandRequest(BaseModel):
    tool: str
    target: str
    additional_args: str = ""

class SuggestToolsRequest(BaseModel):
    description: str
    category: str

@router.post("/command", response_model=str)
async def get_tool_command(
    request: ToolCommandRequest,
    service: ToolManagerServiceBase = Depends(get_tool_manager_service),
):
    """Get the command for a specific tool."""
    try:
        return service.get_tool_command(request.tool, request.target, request.additional_args)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/{category}", response_model=List[str])
async def get_category_tools(
    category: str,
    service: ToolManagerServiceBase = Depends(get_tool_manager_service),
):
    """Get all tools for a specific category."""
    try:
        return service.get_category_tools(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-tools", response_model=List[str])
async def suggest_tools(
    request: SuggestToolsRequest,
    service: ToolManagerServiceBase = Depends(get_tool_manager_service),
):
    """Suggest tools for a given challenge description and category."""
    try:
        return service.suggest_tools_for_challenge(request.description, request.category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
