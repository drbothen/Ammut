from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException

from src.server.dependencies import get_rate_limit_detection_service
from src.server.models.schemas import (
    RateLimitDetectionRequest,
    RateLimitDetectionResponse,
    TimingAdjustmentRequest,
)
from src.server.services.base import RateLimitDetectionServiceBase

router = APIRouter()


@router.post("/detect-rate-limiting", response_model=RateLimitDetectionResponse)
async def detect_rate_limiting(
    request: RateLimitDetectionRequest,
    service: RateLimitDetectionServiceBase = Depends(get_rate_limit_detection_service),
):
    """Detects rate limiting from a response."""
    try:
        return await service.detect_rate_limiting(
            response_text=request.response_text,
            status_code=request.status_code,
            headers=request.headers,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adjust-timing", response_model=Dict[str, Any])
async def adjust_timing(
    request: TimingAdjustmentRequest,
    service: RateLimitDetectionServiceBase = Depends(get_rate_limit_detection_service),
):
    """Adjusts timing parameters based on a recommended profile."""
    try:
        return await service.adjust_timing(
            current_params=request.current_params,
            profile=request.profile,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
