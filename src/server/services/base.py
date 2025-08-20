from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from src.server.models.schemas import (
    TargetProfile, AttackStep, ToolEffectiveness, AttackPattern, AttackChain, 
    TechnologyStack, CTFChallenge, ChallengeSolution, ErrorContext, RecoveryStrategy
)

class IntelligentDecisionServiceBase(ABC):
    """Abstract base class for the intelligent decision engine."""

    @abstractmethod
    async def analyze_target(self, target: str) -> TargetProfile:
        """Analyze a target to build a comprehensive profile."""
        pass

    @abstractmethod
    async def select_optimal_tools(self, profile: TargetProfile, objective: str) -> List[str]:
        """Selects the best tools for a given target and objective."""
        pass

    @abstractmethod
    async def optimize_tool_parameters(self, tool_name: str, profile: TargetProfile) -> Dict[str, Any]:
        """Optimize tool parameters based on the target's characteristics."""
        pass

    @abstractmethod
    async def generate_attack_chain(self, profile: TargetProfile, objective: str) -> AttackChain:
        """Generate a sequence of attack steps based on the target profile."""
        pass

class AbstractTechnologyDetector(ABC):
    @abstractmethod
    async def detect(self, target: str) -> Dict[str, Any]:
        pass

class AbstractRateLimitDetector(ABC):
    @abstractmethod
    async def check_rate_limit(self, url: str) -> Dict[str, Any]:
        pass

class AbstractFailureRecoverySystem(ABC):
    @abstractmethod
    def analyze_failure(self, step: AttackStep) -> str:
        pass

class AbstractParameterOptimizer(ABC):
    @abstractmethod
    def optimize_parameters(self, tool_name: str, target_info: Dict[str, Any]) -> Dict[str, Any]:
        pass

class AbstractHTTPFramework(ABC):
    @abstractmethod
    async def intercept_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None, headers: Optional[Dict] = None, cookies: Optional[Dict] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def spider_website(self, base_url: str, max_depth: int = 2, max_pages: int = 50) -> Dict[str, Any]:
        pass

class AbstractBrowserAgent(ABC):
    @abstractmethod
    def setup_browser(self, headless: bool = True, proxy_port: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def navigate_and_inspect(self, url: str, wait_time: int = 5) -> Dict[str, Any]:
        pass

    @abstractmethod
    def close_browser(self):
        pass

class AbstractAIPayloadGenerator(ABC):
    @abstractmethod
    def generate_contextual_payload(self, target_info: Dict[str, Any]) -> Dict[str, Any]:
        pass

class AbstractFileSystem(ABC):
    @abstractmethod
    async def create_file(self, path: str, content: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def modify_file(self, path: str, content: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def delete_path(self, path: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def list_files(self, path: str) -> Dict[str, Any]:
        pass

class AbstractPayloadGenerator(ABC):
    @abstractmethod
    async def generate(self, payload_type: str, size_kb: int, custom_char: Optional[str] = None) -> str:
        pass

class AbstractTelemetry(ABC):
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        pass

class AbstractProcessManager(ABC):
    @abstractmethod
    async def list_processes(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_process_status(self, pid: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def terminate_process(self, pid: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def pause_process(self, pid: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def resume_process(self, pid: int) -> Dict[str, Any]:
        pass


class AbstractBugBountyManager(ABC):
    @abstractmethod
    async def start_scan(self, url: str, tools: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        pass

class AbstractParameterOptimizerService(ABC):
    @abstractmethod
    async def optimize_parameters(
        self, tool: str, profile: "TargetProfile", context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Optimizes parameters for a given tool and target profile."""
        pass


class VisualEngineServiceBase(ABC):
    """Abstract base class for the visual engine service."""

    @abstractmethod
    def create_banner(self) -> str:
        pass

    @abstractmethod
    def create_progress_bar(self, current: int, total: int, width: int = 50, tool: str = "") -> str:
        pass

    @abstractmethod
    def render_progress_bar(self, progress: float, width: int = 40, style: str = 'cyber', label: str = "", eta: float = 0, speed: str = "") -> str:
        pass

    @abstractmethod
    def create_live_dashboard(self, processes: Dict[int, Dict[str, Any]]) -> str:
        pass

    @abstractmethod
    def format_vulnerability_card(self, vuln_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def format_error_card(self, error_type: str, tool_name: str, error_message: str, recovery_action: str = "") -> str:
        pass

    @abstractmethod
    def format_tool_status(self, tool_name: str, status: str, target: str = "", progress: float = 0.0) -> str:
        pass

    @abstractmethod
    def format_highlighted_text(self, text: str, highlight_type: str = "RED") -> str:
        pass

    @abstractmethod
    def format_vulnerability_severity(self, severity: str, count: int = 0) -> str:
        pass

    @abstractmethod
    def create_section_header(self, title: str, icon: str = "🔥", color: str = "FIRE_RED") -> str:
        pass

    @abstractmethod
    def format_command_execution(self, command: str, status: str, duration: float = 0.0) -> str:
        pass


class ToolManagerServiceBase(ABC):
    """Abstract base class for the tool manager service."""

    @abstractmethod
    def get_tool_command(self, tool: str, target: str, additional_args: str = "") -> str:
        """Get the full command for a given tool and target."""
        pass

    @abstractmethod
    def get_category_tools(self, category: str) -> List[str]:
        """Get a list of tools for a given category."""
        pass

    @abstractmethod
    def suggest_tools_for_challenge(self, challenge_description: str, category: str) -> List[str]:
        """Suggest tools for a given challenge description and category."""
        pass


class ErrorHandlerServiceBase(ABC):
    """Abstract base class for the error handler service."""

    @abstractmethod
    def get_recovery_strategies(self, context: ErrorContext) -> List[RecoveryStrategy]:
        """Get a list of recovery strategies for a given error context."""
        pass


class CTFChallengeAutomatorServiceBase(ABC):
    """Abstract base class for the CTF Challenge Automator service."""

    @abstractmethod
    def auto_solve_challenge(self, challenge: CTFChallenge) -> ChallengeSolution:
        """Attempt to automatically solve a CTF challenge."""
        pass


class AbstractCommandService(ABC):
    """Abstract base class for a command execution service."""

    @abstractmethod
    async def execute(self, command: str, use_cache: bool = True) -> Dict[str, Any]:
        """Executes a shell command and returns the output."""
        pass

    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Returns statistics about the command cache."""
        pass

    @abstractmethod
    async def clear_cache(self) -> Dict[str, Any]:
        """Clears the command cache."""
        pass




class FailureRecoveryServiceBase(ABC):
    """Abstract base class for the failure recovery service."""

    @abstractmethod
    async def analyze_failure(self, error_output: str, exit_code: int) -> Dict[str, Any]:
        """Analyzes a failure and suggests recovery strategies."""
        pass


class RateLimitDetectionServiceBase(ABC):
    """Abstract base class for the rate limit detection service."""

    @abstractmethod
    async def detect_rate_limiting(
        self,
        response_text: str,
        status_code: int,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Detects rate limiting from a response."""
        pass

    @abstractmethod
    async def adjust_timing(
        self,
        current_params: Dict[str, Any],
        profile: str
    ) -> Dict[str, Any]:
        """Adjusts timing parameters based on a recommended profile."""
        pass


class TechnologyDetectionServiceBase(ABC):
    """Abstract base class for the technology detection service."""

    @abstractmethod
    async def detect_technologies(
        self,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        ports: Optional[List[int]] = None
    ) -> Dict[str, List[str]]:
        """
        Detects technologies based on HTTP headers, page content, and open ports.
        """
        pass

