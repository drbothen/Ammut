from fastapi import APIRouter, Depends, HTTPException

from src.server.dependencies import get_failure_recovery_service
from src.server.models.schemas import (
    FailureAnalysisRequest,
    FailureAnalysisResponse,
)
from src.server.services.base import FailureRecoveryServiceBase

router = APIRouter(
    prefix="/failure-recovery",
    tags=["Failure Recovery"],
)


@router.post("/analyze-failure", response_model=FailureAnalysisResponse)
async def analyze_failure(
    request: FailureAnalysisRequest,
    service: FailureRecoveryServiceBase = Depends(get_failure_recovery_service),
):
    """Analyzes a failure and suggests recovery strategies."""
    try:
        return await service.analyze_failure(
            error_output=request.error_output,
            exit_code=request.exit_code,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
