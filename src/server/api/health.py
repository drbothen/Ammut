from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """Check the health of the application."""
    return {"status": "ok"}
