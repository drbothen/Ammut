from fastapi import Depends
from src.server.services.base import (
    ErrorHandlerServiceBase,
    AbstractCommandService,
    AbstractFileSystem,
    AbstractPayloadGenerator,
    AbstractBugBountyManager,
    FailureRecoveryServiceBase,
    AbstractProcessManager,
    RateLimitDetectionServiceBase,
    TechnologyDetectionServiceBase,
    AbstractTelemetry,
    VisualEngineServiceBase,
    IntelligentDecisionServiceBase,
    ToolManagerServiceBase,
    CTFChallengeAutomatorServiceBase
)
from src.server.services.error_handler_service import ErrorHandlerService
from src.server.services.command_service import CommandService
from src.server.services.file_system import FileSystem
from src.server.services.payload_generator import PayloadGenerator
from src.server.services.bug_bounty_manager import BugBountyManager
from src.server.services.failure_recovery_service import FailureRecoveryService
from src.server.services.process_manager import ProcessManager
from src.server.services.rate_limit_detection_service import RateLimitDetectionService
from src.server.services.technology_detection_service import TechnologyDetectionService
from src.server.services.telemetry import Telemetry
from src.server.services.visual_engine_service import VisualEngineService
from src.server.services.intelligent_decision_service import IntelligentDecisionService
from src.server.services.tool_manager_service import ToolManagerService
from src.server.services.challenge_automator_service import CTFChallengeAutomatorService


def get_intelligent_decision_service() -> IntelligentDecisionServiceBase:
    """Provides a singleton instance of the IntelligentDecisionService."""
    return IntelligentDecisionService()




def get_command_service() -> AbstractCommandService:
    """Provides a singleton instance of the CommandService."""
    return CommandService()


def get_file_system_service() -> AbstractFileSystem:
    """Provides a singleton instance of the FileSystem service."""
    return FileSystem()


def get_payload_generator_service() -> AbstractPayloadGenerator:
    """Provides a singleton instance of the PayloadGenerator service."""
    return PayloadGenerator()


def get_bug_bounty_manager(
    command_service: AbstractCommandService = Depends(get_command_service),
) -> AbstractBugBountyManager:
    """Provides a singleton instance of the BugBountyManager."""
    return BugBountyManager(command_service=command_service)


def get_failure_recovery_service() -> FailureRecoveryServiceBase:
    """Provides a singleton instance of the FailureRecoveryService."""
    return FailureRecoveryService()


def get_error_handler_service(
    failure_recovery_service: FailureRecoveryServiceBase = Depends(
        get_failure_recovery_service
    ),
) -> ErrorHandlerServiceBase:
    """Get an instance of the Error Handler service."""
    return ErrorHandlerService(failure_recovery_service=failure_recovery_service)


def get_process_manager_service() -> AbstractProcessManager:
    """Provides a singleton instance of the ProcessManager service."""
    return ProcessManager()


def get_rate_limit_detection_service() -> RateLimitDetectionServiceBase:
    """Provides a singleton instance of the RateLimitDetectionService."""
    return RateLimitDetectionService()


def get_technology_detection_service() -> TechnologyDetectionServiceBase:
    """Provides a singleton instance of the TechnologyDetectionService."""
    return TechnologyDetectionService()


def get_telemetry_service() -> AbstractTelemetry:
    """Provides a singleton instance of the Telemetry service."""
    return Telemetry()


def get_visual_engine_service() -> VisualEngineServiceBase:
    """Provides a singleton instance of the VisualEngineService."""
    return VisualEngineService()


def get_tool_manager_service() -> ToolManagerServiceBase:
    """Get an instance of the tool manager service."""
    return ToolManagerService()


def get_challenge_automator_service(
    tool_manager: ToolManagerServiceBase = Depends(get_tool_manager_service),
) -> CTFChallengeAutomatorServiceBase:
    """Get an instance of the CTF Challenge Automator service."""
    return CTFChallengeAutomatorService(tool_manager_service=get_tool_manager_service())
