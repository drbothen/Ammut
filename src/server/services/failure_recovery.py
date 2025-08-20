from typing import Dict, Any

from .base import AbstractFailureRecoverySystem
from models.schemas import AttackStep
from core.logging import logger

class FailureRecoverySystem(AbstractFailureRecoverySystem):
    """Analyzes failed attack steps and suggests recovery actions."""

    def analyze_failure(self, step: AttackStep) -> str:
        """Analyzes the error message of a failed step and provides a recovery suggestion."""
        logger.info(f"Analyzing failure for step {step.step_id} (Tool: {step.tool})")

        error_message = "".join(step.logs).lower() if step.logs else ""

        if "timeout" in error_message:
            return "The command timed out. Consider increasing the timeout or checking the target's responsiveness."
        
        if "not found" in error_message or "no such file" in error_message:
            return f"The tool '{step.tool}' or a required file was not found. Ensure the tool is installed and in the system's PATH."

        if "connection refused" in error_message:
            return "The connection was refused by the target. The target may be down or a firewall might be blocking the connection."

        if "authentication failed" in error_message or "401 unauthorized" in error_message:
            return "Authentication failed. Check the credentials or tokens being used."

        # Default suggestion
        return "The tool failed for an unknown reason. Review the logs and consider trying a different tool or parameters."

failure_recovery_system = FailureRecoverySystem()
