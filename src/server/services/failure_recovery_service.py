from typing import Dict, Any

from src.server.services.base import FailureRecoveryServiceBase
from src.server.core.failure_recovery import TOOL_ALTERNATIVES, FAILURE_PATTERNS

class FailureRecoveryService(FailureRecoveryServiceBase):
    """Service for analyzing failures and providing recovery strategies."""

    async def analyze_failure(self, error_output: str, exit_code: int) -> Dict[str, Any]:
        """Analyzes a failure and suggests recovery strategies."""
        failure_type = "unknown"
        confidence = 0.0
        recovery_strategies = []
        error_lower = error_output.lower()

        for f_type, patterns in FAILURE_PATTERNS.items():
            for pattern in patterns:
                if pattern in error_lower:
                    failure_type = f_type
                    confidence += 0.3
                    break
        
        if exit_code == 124:  # timeout
            failure_type = "timeout"
            confidence += 0.5
        elif exit_code == 126:  # permission denied
            failure_type = "permission_denied"
            confidence += 0.5
        elif exit_code != 0:
            confidence += 0.1

        confidence = min(1.0, confidence)

        if failure_type == "timeout":
            recovery_strategies = [
                "Increase timeout values",
                "Reduce thread count",
                "Use alternative faster tool",
                "Split target into smaller chunks"
            ]
        elif failure_type == "permission_denied":
            recovery_strategies = [
                "Run with elevated privileges",
                "Check file permissions",
                "Use alternative tool with different approach"
            ]
        elif failure_type == "rate_limited":
            recovery_strategies = [
                "Implement delays between requests",
                "Reduce thread count",
                "Use stealth timing profile",
                "Rotate IP addresses if possible"
            ]
        elif failure_type == "network_error":
            recovery_strategies = [
                "Check network connectivity",
                "Try alternative network routes",
                "Use proxy or VPN",
                "Verify target is accessible"
            ]

        return {
            "failure_type": failure_type,
            "confidence": confidence,
            "recovery_strategies": recovery_strategies,
            "alternative_tools": TOOL_ALTERNATIVES.get(self._extract_tool_name(error_output), [])
        }

    def _extract_tool_name(self, error_output: str) -> str:
        """Extracts the tool name from the error output."""
        for tool in TOOL_ALTERNATIVES.keys():
            if tool in error_output.lower():
                return tool
        return "unknown"
