from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from src.server.dependencies import get_technology_detection_service
from src.server.models.schemas import TechnologyDetectionRequest
from src.server.services.base import TechnologyDetectionServiceBase

router = APIRouter()


@router.post("/detect-technologies", response_model=Dict[str, List[str]])
async def detect_technologies(
    request: TechnologyDetectionRequest,
    service: TechnologyDetectionServiceBase = Depends(get_technology_detection_service),
):
    """Detects technologies based on HTTP headers, content, and open ports."""
    try:
        return await service.detect_technologies(
            headers=request.headers, content=request.content, ports=request.ports
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
