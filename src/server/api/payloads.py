from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from src.server.dependencies import get_payload_generator_service
from src.server.models.schemas import PayloadRequest
from src.server.services.base import AbstractPayloadGenerator

router = APIRouter()


@router.post("/payloads/generate", tags=["Payloads"], response_class=PlainTextResponse)
async def generate_payload(
    request: PayloadRequest,
    service: AbstractPayloadGenerator = Depends(get_payload_generator_service),
) -> str:
    """Generates a large payload for testing purposes."""
    return await service.generate(
        payload_type=request.payload_type,
        size_kb=request.size_kb,
        custom_char=request.custom_char,
    )
