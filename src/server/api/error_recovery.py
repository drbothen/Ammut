from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.server.models.schemas import ErrorContext, RecoveryStrategy
from src.server.services.base import ErrorHandlerServiceBase
from src.server.dependencies import get_error_handler_service

router = APIRouter(
    prefix="/error-recovery",
    tags=["Error Recovery"],
)

@router.post("/get-recovery-strategies", response_model=List[RecoveryStrategy])
async def get_recovery_strategies(
    context: ErrorContext,
    error_handler_service: ErrorHandlerServiceBase = Depends(get_error_handler_service),
):
    """
    Get a list of recovery strategies for a given error context.
    """
    try:
        return await error_handler_service.get_recovery_strategies(context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
