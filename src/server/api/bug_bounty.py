from typing import Dict, Any

from fastapi import APIRouter, Depends, Path

from src.server.dependencies import get_bug_bounty_manager
from src.server.models.schemas import BugBountyScanRequest
from src.server.services.base import AbstractBugBountyManager

router = APIRouter()


@router.post("/bugbounty/start_scan", tags=["Bug Bounty"], status_code=202)
async def start_bug_bounty_scan(
    request: BugBountyScanRequest,
    service: AbstractBugBountyManager = Depends(get_bug_bounty_manager),
) -> Dict[str, Any]:
    """Starts a new bug bounty scan with the specified tools."""
    return await service.start_scan(request.url, request.tools)


@router.get("/bugbounty/scan_status/{scan_id}", tags=["Bug Bounty"])
async def get_bug_bounty_scan_status(
    scan_id: str = Path(..., title="Scan ID"),
    service: AbstractBugBountyManager = Depends(get_bug_bounty_manager),
) -> Dict[str, Any]:
    """Gets the status and results of a specific bug bounty scan."""
    return await service.get_scan_status(scan_id)
