from fastapi import APIRouter, Depends

from src.server.dependencies import get_challenge_automator_service
from src.server.models.schemas import CTFChallenge, ChallengeSolution
from src.server.services.base import CTFChallengeAutomatorServiceBase

router = APIRouter(
    prefix="/challenge-automator",
    tags=["challenge-automator"],
)


@router.post("/solve", response_model=ChallengeSolution)
def solve_challenge(
    challenge: CTFChallenge,
    automator_service: CTFChallengeAutomatorServiceBase = Depends(
        get_challenge_automator_service
    ),
) -> ChallengeSolution:
    """Endpoint to automatically solve a CTF challenge."""
    return automator_service.auto_solve_challenge(challenge)
