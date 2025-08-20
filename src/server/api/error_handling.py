from fastapi import APIRouter, Depends, HTTPException

from src.server.dependencies import get_error_handler_service
from src.server.models.enums import ErrorType
from src.server.models.schemas import ErrorContext, RecoveryStrategy
from src.server.services.base import ErrorHandlerServiceBase

router = APIRouter()

@router.post("/classify-error", response_model=ErrorType)
async def classify_error(
    error_message: str,
    service: ErrorHandlerServiceBase = Depends(get_error_handler_service),
):
    """Classifies an error message and returns the corresponding ErrorType."""
    try:
        return await service.classify_error(error_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recovery-strategy", response_model=RecoveryStrategy)
async def get_recovery_strategy(
    context: ErrorContext,
    service: ErrorHandlerServiceBase = Depends(get_error_handler_service),
):
    """Determines the best recovery strategy based on the error context."""
    try:
        return await service.get_recovery_strategy(context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
