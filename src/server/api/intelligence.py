from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from src.server.models.schemas import TargetProfile, AttackChain, OptimizeParametersRequest, UrlRequest
from src.server.services.base import AbstractIntelligenceService
from src.server.dependencies import get_intelligence_service

router = APIRouter()

@router.post("/intelligence/analyze-target", response_model=TargetProfile, tags=["Intelligence"])
async def analyze_target(
    request: UrlRequest,
    service: AbstractIntelligenceService = Depends(get_intelligence_service)
):
    """Analyzes a target URL to build a comprehensive profile."""
    try:
        return await service.analyze_target(request.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/intelligence/generate-attack-chain", response_model=AttackChain, tags=["Intelligence"])
async def generate_attack_chain(
    target_profile: TargetProfile,
    service: AbstractIntelligenceService = Depends(get_intelligence_service)
):
    """Generates a sequence of attack steps based on the target profile."""
    return await service.generate_attack_chain(target_profile)

@router.post("/intelligence/optimize-parameters", tags=["Intelligence"])
async def optimize_parameters(
    request: OptimizeParametersRequest,
    service: AbstractIntelligenceService = Depends(get_intelligence_service)
) -> Dict[str, Any]:
    """Suggests optimized parameters for a given tool and target profile."""
    return await service.optimize_parameters(request.tool_name, request.target_profile)
