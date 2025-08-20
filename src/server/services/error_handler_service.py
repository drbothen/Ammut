import re
from typing import Dict, Any, List
from datetime import datetime

from src.server.models.enums import ErrorType, RecoveryAction
from src.server.models.schemas import ErrorContext, RecoveryStrategy
from src.server.services.base import ErrorHandlerServiceBase, FailureRecoveryServiceBase
from src.server.core.error_handling import (
    ERROR_PATTERNS,
    RECOVERY_STRATEGIES,
    TOOL_ALTERNATIVES,
    PARAMETER_ADJUSTMENTS,
)

class ErrorHandlerService(ErrorHandlerServiceBase):
    """Service for intelligent error handling and recovery."""

    def __init__(self, failure_recovery_service: FailureRecoveryServiceBase):
        self.failure_recovery_service = failure_recovery_service

    async def get_recovery_strategies(self, context: ErrorContext) -> List[RecoveryStrategy]:
        """Determines the best recovery strategies based on the error context."""
        error_type = self._classify_error(context.error_message)
        context.error_type = error_type

        strategy_configs = RECOVERY_STRATEGIES.get(error_type, [])

        # If exit_code is available, use the FailureRecoveryService
        if hasattr(context, 'exit_code') and context.exit_code is not None:
            failure_analysis = await self.failure_recovery_service.analyze_failure(
                error_output=context.error_message,
                exit_code=context.exit_code
            )
            # This is a simplified integration. A real implementation would have a more
            # sophisticated way of merging strategies from both services.
            if failure_analysis["recovery_strategies"]:
                # For now, we'll just create a single strategy for demonstration
                return [
                    RecoveryStrategy(
                        action=RecoveryAction.ADJUST_PARAMETERS,
                        parameters={"suggestions": failure_analysis["recovery_strategies"]},
                        max_attempts=1,
                        backoff_multiplier=1.0,
                        success_probability=0.5,
                        estimated_time=60
                    )
                ]

        if error_type == ErrorType.UNKNOWN or not strategy_configs:
            return [
                RecoveryStrategy(
                    action=RecoveryAction.ESCALATE_TO_HUMAN,
                    parameters={"message": "Unknown error, manual intervention required."},
                    max_attempts=1,
                    backoff_multiplier=1.0,
                    success_probability=0.9,
                    estimated_time=300
                )
            ]

        recovery_strategies = []
        for config in strategy_configs:
            params = config.get("parameters", {}).copy()
            action = config["action"]

            if action == RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL:
                alternatives = TOOL_ALTERNATIVES.get(context.tool_name)
                if alternatives:
                    params["alternative_tools"] = alternatives
                else:
                    continue  # Skip this strategy if no alternatives are found

            if action == RecoveryAction.ADJUST_PARAMETERS:
                adjustments = PARAMETER_ADJUSTMENTS.get(context.tool_name, {}).get(error_type)
                if adjustments:
                    params.update(adjustments)

            recovery_strategies.append(
                RecoveryStrategy(
                    action=action,
                    parameters=params,
                    max_attempts=config.get("max_attempts", 1),
                    backoff_multiplier=config.get("backoff_multiplier", 1.5),
                    success_probability=config.get("success_probability", 0.5),
                    estimated_time=config.get("estimated_time", 60),
                )
            )
        
        return recovery_strategies

    def _classify_error(self, error_message: str) -> ErrorType:
        """Classifies an error message into a specific error type using regex patterns."""
        for pattern, error_type in ERROR_PATTERNS.items():
            if re.search(pattern, error_message, re.IGNORECASE):
                return error_type
        return ErrorType.UNKNOWN
