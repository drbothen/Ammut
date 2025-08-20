from typing import Dict, Any, List

from src.server.models.enums import TargetType, TechnologyStack
from src.server.models.schemas import TargetProfile, AttackChain, AttackStep
from src.server.services.base import (
    AbstractIntelligenceService, 
    AbstractParameterOptimizerService, 
    AbstractTechnologyDetector
)
from src.server.core.logging import logger
from core.attack_patterns import ATTACK_PATTERNS


class IntelligenceService(AbstractIntelligenceService):
    """AI-powered tool selection and parameter optimization engine."""

    def __init__(
        self, 
        parameter_optimizer: AbstractParameterOptimizerService, 
        technology_detector: AbstractTechnologyDetector
    ):
        self.tool_effectiveness = self._initialize_tool_effectiveness()
        self.technology_signatures = self._initialize_technology_signatures()
        self.attack_patterns = ATTACK_PATTERNS
        self.parameter_optimizer = parameter_optimizer
        self.technology_detector = technology_detector

    async def analyze_target(self, target: str) -> TargetProfile:
        """Analyzes a target to build a comprehensive profile."""
        profile = TargetProfile(target=target, target_type=TargetType.WEB_APPLICATION)

        # Perform technology detection
        detection_results = await self.technology_detector.detect(target)

        if "technologies" in detection_results and detection_results["technologies"]:
            detected_techs = []
            for tech_name in detection_results["technologies"].keys():
                try:
                    # Normalize tech name to match enum members (e.g., "node.js" -> "NODEJS")
                    normalized_name = tech_name.upper().replace('.', '').replace('-', '_')
                    tech_enum = TechnologyStack[normalized_name]
                    detected_techs.append(tech_enum)
                except KeyError:
                    logger.warning(f"Detected technology '{tech_name}' not in TechnologyStack enum.")
            profile.technologies = detected_techs

        return profile

    async def generate_attack_chain(self, target_profile: TargetProfile) -> AttackChain:
        """Generates a sequence of attack steps based on the target profile. Mock implementation."""
        chain = AttackChain(target_profile=target_profile)
        if target_profile.target_type == TargetType.WEB_APPLICATION:
            # This is a simplified example. A real implementation would use self.attack_patterns
            chain.steps.append(
                AttackStep(
                    tool="nmap",
                    parameters={"-sV -p- --open": target_profile.target},
                    expected_outcome="Open ports and service versions",
                    success_probability=0.9,
                    execution_time_estimate=300,
                )
            )
            chain.steps.append(
                AttackStep(
                    tool="nuclei",
                    parameters={"-u": target_profile.target},
                    expected_outcome="Known vulnerabilities identified",
                    success_probability=0.85,
                    execution_time_estimate=600,
                    dependencies=["nmap"],
                )
            )
        return chain

    async def optimize_parameters(self, tool_name: str, target_profile: TargetProfile) -> Dict[str, Any]:
        """Delegates parameter optimization to the specialized service."""
        return await self.parameter_optimizer.optimize_parameters(tool_name, target_profile)

    def _initialize_tool_effectiveness(self) -> Dict[str, Dict[str, float]]:
        """Initialize tool effectiveness ratings for different target types"""
        return {
            TargetType.WEB_APPLICATION.value: {
                "nmap": 0.8,
                "gobuster": 0.9,
                "nuclei": 0.95,
                "nikto": 0.85,
                "sqlmap": 0.9,
                "ffuf": 0.9,
                "feroxbuster": 0.85,
                "katana": 0.88,
                "httpx": 0.85,
                "wpscan": 0.95,  # High for WordPress sites
                "burpsuite": 0.9,
                "dirsearch": 0.87,
                "gau": 0.82,
                "waybackurls": 0.8,
                "arjun": 0.9,
                "paramspider": 0.85,
                "x8": 0.88,
                "jaeles": 0.92,
                "dalfox": 0.93,  # High for XSS detection
                "anew": 0.7,  # Utility tool
                "qsreplace": 0.75,  # Utility tool
                "uro": 0.7  # Utility tool
            },
            TargetType.NETWORK_HOST.value: {
                "nmap": 0.95,
                "masscan": 0.92,
                "rustscan": 0.9,
                "autorecon": 0.95,
                "enum4linux-ng": 0.88,
                "smbmap": 0.85,
                "rpcclient": 0.82,
                "nbtscan": 0.75,
                "responder": 0.88,
                "hydra": 0.8,
                "netexec": 0.85,
                "amass": 0.7
            },
            TargetType.API_ENDPOINT.value: {
                "nuclei": 0.9,
                "ffuf": 0.85,
                "arjun": 0.95,
                "paramspider": 0.88,
                "httpx": 0.9,
                "x8": 0.92,
                "katana": 0.85,
                "jaeles": 0.88,
                "postman": 0.8
            },
            TargetType.CLOUD_SERVICE.value: {
                "prowler": 0.95,
                "scout-suite": 0.92,
                "cloudmapper": 0.88,
                "pacu": 0.85,
                "trivy": 0.9,
                "clair": 0.85,
                "kube-hunter": 0.9,
                "kube-bench": 0.88,
                "checkov": 0.9,
                "terrascan": 0.88
            },
            TargetType.BINARY_FILE.value: {
                "ghidra": 0.95,
                "radare2": 0.9,
                "gdb-peda": 0.92,
                "angr": 0.88,
                "pwntools": 0.9,
                "ropgadget": 0.85,
                "ropper": 0.88,
                "one-gadget": 0.82
            }
        }

    def _initialize_technology_signatures(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize technology detection signatures"""
        return {
            "headers": {
                TechnologyStack.APACHE.value: ["Apache", "apache"],
                TechnologyStack.NGINX.value: ["nginx", "Nginx"],
                TechnologyStack.IIS.value: ["Microsoft-IIS", "IIS"],
                TechnologyStack.PHP.value: ["PHP", "X-Powered-By: PHP"],
                TechnologyStack.NODEJS.value: ["Express", "X-Powered-By: Express"],
                TechnologyStack.PYTHON.value: ["Django", "Flask", "Werkzeug"],
                TechnologyStack.JAVA.value: ["Tomcat", "JBoss", "WebLogic"],
                TechnologyStack.DOTNET.value: ["ASP.NET", "X-AspNet-Version"]
            },
            "content": {
                TechnologyStack.WORDPRESS.value: ["wp-content", "wp-includes", "WordPress"],
                TechnologyStack.DRUPAL.value: ["Drupal", "drupal", "/sites/default"],
                TechnologyStack.JOOMLA.value: ["Joomla", "joomla", "/administrator"],
                TechnologyStack.REACT.value: ["React", "react", "__REACT_DEVTOOLS"],
                TechnologyStack.ANGULAR.value: ["Angular", "angular", "ng-version"],
                TechnologyStack.VUE.value: ["Vue", "vue", "__VUE__"]
            },
        }

