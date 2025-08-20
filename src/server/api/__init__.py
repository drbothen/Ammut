from fastapi import APIRouter

from . import (health, command, files, payloads, cache, telemetry, processes, bug_bounty, error_handling, technology_detection, rate_limit_detection, failure_recovery, intelligent_decision, visual_engine, tool_manager, challenge_automator, error_recovery)

# A list of all routers to be included in the main FastAPI app
routers: list[APIRouter] = [
    health.router,
    command.router,
    files.router,
    payloads.router,
    cache.router,
    telemetry.router,
    processes.router,
    bug_bounty.router,
    error_handling.router,
    technology_detection.router,
    rate_limit_detection.router,
    failure_recovery.router,
    intelligent_decision.router,
    visual_engine.router,
    tool_manager.router,
    challenge_automator.router,
    error_recovery.router,
]
