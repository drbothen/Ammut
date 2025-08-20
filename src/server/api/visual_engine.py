from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List

from src.server.services.base import VisualEngineServiceBase
from src.server.dependencies import get_visual_engine_service

router = APIRouter(prefix="/visual-engine", tags=["Visual Engine"])

class ProgressBarRequest(BaseModel):
    current: int
    total: int
    width: int = 50
    tool: str = ""

class RenderProgressBarRequest(BaseModel):
    progress: float
    width: int = 40
    style: str = 'cyber'
    label: str = ""
    eta: float = 0
    speed: str = ""

class LiveDashboardRequest(BaseModel):
    processes: Dict[int, Dict[str, Any]]

class VulnerabilityCardRequest(BaseModel):
    vuln_data: Dict[str, Any]

class ErrorCardRequest(BaseModel):
    error_type: str
    tool_name: str
    error_message: str
    recovery_action: str = ""

class ToolStatusRequest(BaseModel):
    tool_name: str
    status: str
    target: str = ""
    progress: float = 0.0

class HighlightedTextRequest(BaseModel):
    text: str
    highlight_type: str = "RED"

class VulnerabilitySeverityRequest(BaseModel):
    severity: str
    count: int = 0

class SectionHeaderRequest(BaseModel):
    title: str
    icon: str = "🔥"
    color: str = "FIRE_RED"

class CommandExecutionRequest(BaseModel):
    command: str
    status: str
    duration: float = 0.0

@router.post("/banner", response_class=PlainTextResponse)
def create_banner(service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.create_banner()

@router.post("/progress-bar", response_class=PlainTextResponse)
def create_progress_bar(request: ProgressBarRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.create_progress_bar(**request.model_dump())

@router.post("/render-progress-bar", response_class=PlainTextResponse)
def render_progress_bar(request: RenderProgressBarRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.render_progress_bar(**request.model_dump())

@router.post("/live-dashboard", response_class=PlainTextResponse)
def create_live_dashboard(request: LiveDashboardRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.create_live_dashboard(**request.model_dump())

@router.post("/vulnerability-card", response_class=PlainTextResponse)
def format_vulnerability_card(request: VulnerabilityCardRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.format_vulnerability_card(**request.model_dump())

@router.post("/error-card", response_class=PlainTextResponse)
def format_error_card(request: ErrorCardRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.format_error_card(**request.model_dump())

@router.post("/tool-status", response_class=PlainTextResponse)
def format_tool_status(request: ToolStatusRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.format_tool_status(**request.model_dump())

@router.post("/highlighted-text", response_class=PlainTextResponse)
def format_highlighted_text(request: HighlightedTextRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.format_highlighted_text(**request.model_dump())

@router.post("/vulnerability-severity", response_class=PlainTextResponse)
def format_vulnerability_severity(request: VulnerabilitySeverityRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.format_vulnerability_severity(**request.model_dump())

@router.post("/section-header", response_class=PlainTextResponse)
def create_section_header(request: SectionHeaderRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.create_section_header(**request.model_dump())

@router.post("/command-execution", response_class=PlainTextResponse)
def format_command_execution(request: CommandExecutionRequest, service: VisualEngineServiceBase = Depends(get_visual_engine_service)):
    return service.format_command_execution(**request.model_dump())
