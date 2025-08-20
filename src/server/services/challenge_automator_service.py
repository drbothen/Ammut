import re
import time
from typing import Any, Dict, List

from src.server.models.schemas import (
    CTFChallenge, ChallengeSolution, ChallengeStep, ManualGuidance
)
from src.server.services.base import (
    CTFChallengeAutomatorServiceBase, ToolManagerServiceBase
)


class CTFChallengeAutomatorService(CTFChallengeAutomatorServiceBase):
    """Concrete implementation of the CTF Challenge Automator service."""

    def __init__(self, tool_manager_service: ToolManagerServiceBase):
        self.tool_manager = tool_manager_service
        self.solution_cache: Dict[str, ChallengeSolution] = {}

    def auto_solve_challenge(self, challenge: CTFChallenge) -> ChallengeSolution:
        """Attempt to automatically solve a CTF challenge."""
        # This is a placeholder for a more complex workflow creation logic
        # that would likely be its own service in a full refactor.
        workflow = self._create_dummy_workflow(challenge)

        solution = ChallengeSolution(
            challenge_id=challenge.name,
            status="in_progress",
            automated_steps=[],
            manual_steps=[],
            confidence=0.0,
            estimated_completion=0,
            artifacts=[],
            flag_candidates=[],
            next_actions=[]
        )

        try:
            for i, step_config in enumerate(workflow):
                step_result = self._execute_step(i, step_config, challenge)
                solution.automated_steps.append(step_result)

                if step_result.output:
                    flags = self._extract_flag_candidates(step_result.output)
                    solution.flag_candidates.extend(flags)

                if step_result.success:
                    solution.confidence += 0.1

                if solution.flag_candidates and self._validate_flag_format(solution.flag_candidates[0]):
                    solution.status = "solved"
                    solution.flag = solution.flag_candidates[0]
                    break

            if solution.status != "solved":
                solution.manual_steps = self._generate_manual_guidance(challenge, solution)
                solution.status = "needs_manual_intervention"

            solution.confidence = min(1.0, solution.confidence)

        except Exception as e:
            solution.status = "error"
            solution.error = str(e)

        return solution

    def _execute_step(self, step_index: int, step_config: Dict[str, Any], challenge: CTFChallenge) -> ChallengeStep:
        """Execute a single workflow step."""
        start_time = time.time()
        output = ""
        success = False
        tools_used = []

        for tool in step_config.get("tools", []):
            try:
                command = self.tool_manager.get_tool_command(tool, challenge.target or challenge.name)
                output += f"[{tool}] Executed successfully (simulation): {command}\n"
                tools_used.append(tool)
                success = True
            except Exception as e:
                output += f"[{tool}] Error: {str(e)}\n"

        return ChallengeStep(
            step=step_index + 1,
            action=step_config["action"],
            success=success,
            output=output,
            tools_used=tools_used,
            execution_time=time.time() - start_time,
            artifacts=[]
        )

    def _extract_flag_candidates(self, output: str) -> List[str]:
        """Extract potential flags from tool output."""
        patterns = [
            r'flag\{[^}]+\}', r'ctf\{[^}]+\}', r'[a-zA-Z0-9_]+\{[^}]+\}',
            r'[0-9a-f]{32}', r'[0-9a-f]{40}', r'[0-9a-f]{64}'
        ]
        candidates = []
        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            candidates.extend(matches)
        return list(set(candidates))

    def _validate_flag_format(self, flag: str) -> bool:
        """Validate if a string matches common flag formats."""
        patterns = [
            r'^flag\{.+\}$', r'^ctf\{.+\}$', r'^[a-zA-Z0-9_]+\{.+\}$'
        ]
        for pattern in patterns:
            if re.match(pattern, flag, re.IGNORECASE):
                return True
        return False

    def _generate_manual_guidance(self, challenge: CTFChallenge, solution: ChallengeSolution) -> List[ManualGuidance]:
        """Generate manual guidance when automation fails."""
        guidance = []
        attempted_tools = {tool for step in solution.automated_steps for tool in step.tools_used}
        
        try:
            category_tools = self.tool_manager.get_category_tools(challenge.category)
            unused_tools = [t for t in category_tools if t not in attempted_tools]
            if unused_tools:
                guidance.append(ManualGuidance(
                    action="try_alternative_tools",
                    description=f"Try these alternative tools: {', '.join(unused_tools[:3])}"
                ))
        except KeyError:
            # Category might not exist in tool manager
            pass

        if challenge.category == "web":
            guidance.append(ManualGuidance(action="manual_source_review", description="Manually review HTML/JS source code."))
        
        return guidance

    def _create_dummy_workflow(self, challenge: CTFChallenge) -> List[Dict[str, Any]]:
        """Creates a simple, dummy workflow based on challenge category."""
        if challenge.category == "web":
            return [
                {"action": "Web Reconnaissance", "tools": ["nmap", "gobuster"]},
                {"action": "Vulnerability Scanning", "tools": ["nikto", "sqlmap"]}
            ]
        elif challenge.category == "crypto":
            return [
                {"action": "Cipher Analysis", "tools": ["ciphey"]},
                {"action": "Key Cracking", "tools": ["john", "hashcat"]}
            ]
        return []
