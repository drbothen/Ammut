from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from src.server.services.base import IntelligentDecisionServiceBase
from src.server.dependencies import get_intelligent_decision_service
from src.server.models.schemas import TargetProfile, AttackChain, BaseModel

router = APIRouter(prefix="/intelligent-decision", tags=["Intelligent Decision"])

class TargetRequest(BaseModel):
    target: str

class ToolSelectionRequest(BaseModel):
    profile: TargetProfile
    objective: str = "comprehensive"

class ParameterOptimizationRequest(BaseModel):
    tool_name: str
    profile: TargetProfile

class AttackChainRequest(BaseModel):
    profile: TargetProfile
    objective: str = "comprehensive"

@router.post("/analyze", response_model=TargetProfile)
async def analyze_target(
    request: TargetRequest,
    service: IntelligentDecisionServiceBase = Depends(get_intelligent_decision_service)
):
    """Analyzes a target and returns its profile."""
    try:
        profile = await service.analyze_target(request.target)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/select-tools", response_model=List[str])
async def select_tools(
    request: ToolSelectionRequest,
    service: IntelligentDecisionServiceBase = Depends(get_intelligent_decision_service)
):
    """Selects optimal tools for a given target profile and objective."""
    try:
        tools = await service.select_optimal_tools(request.profile, request.objective)
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize-parameters", response_model=Dict[str, Any])
async def optimize_parameters(
    request: ParameterOptimizationRequest,
    service: IntelligentDecisionServiceBase = Depends(get_intelligent_decision_service)
):
    """Optimizes parameters for a given tool and target profile."""
    try:
        params = await service.optimize_tool_parameters(request.tool_name, request.profile)
        return params
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-chain", response_model=AttackChain)
async def generate_chain(
    request: AttackChainRequest,
    service: IntelligentDecisionServiceBase = Depends(get_intelligent_decision_service)
):
    """Generates a full attack chain for a given target profile and objective."""
    try:
        chain = await service.generate_attack_chain(request.profile, request.objective)
        return chain
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
