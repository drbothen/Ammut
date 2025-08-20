from typing import Dict, Any, List, Optional
import re
import socket
import urllib.parse

from .base import IntelligentDecisionServiceBase
from ..models.enums import TargetType, TechnologyStack
from ..models.schemas import TargetProfile, AttackChain, AttackStep


class IntelligentDecisionService(IntelligentDecisionServiceBase):
    """AI-powered tool selection and parameter optimization engine."""

    def __init__(self):
        self.tool_effectiveness = self._initialize_tool_effectiveness()
        self.technology_signatures = self._initialize_technology_signatures()
        self.attack_patterns = self._initialize_attack_patterns()

    async def analyze_target(self, target: str) -> TargetProfile:
        """Analyze target and create comprehensive profile."""
        profile = TargetProfile(target=target)
        profile.target_type = self._determine_target_type(target)

        if profile.target_type in [TargetType.WEB_APPLICATION, TargetType.API_ENDPOINT]:
            profile.ip_addresses = self._resolve_domain(target)

        if profile.target_type == TargetType.WEB_APPLICATION:
            profile.technologies = self._detect_technologies(target)
            profile.cms_type = self._detect_cms(target)

        profile.attack_surface_score = self._calculate_attack_surface(profile)
        profile.risk_level = self._determine_risk_level(profile)
        profile.confidence_score = self._calculate_confidence(profile)

        return profile

    async def select_optimal_tools(self, profile: TargetProfile, objective: str = "comprehensive") -> List[str]:
        """Selects the best tools for a given target and objective."""
        if not profile.target_type or profile.target_type == TargetType.UNKNOWN:
            return []

        target_type_value = profile.target_type.value
        if target_type_value not in self.tool_effectiveness:
            return []

        tool_scores = self.tool_effectiveness[target_type_value]
        sorted_tools = sorted(tool_scores.keys(), key=lambda tool: tool_scores[tool], reverse=True)

        # Further filter based on objective if needed (simplified for now)
        return sorted_tools[:5] # Return top 5

    async def optimize_tool_parameters(self, tool_name: str, profile: TargetProfile) -> Dict[str, Any]:
        """Optimize tool parameters based on the target's characteristics."""
        # This is a placeholder for a more sophisticated implementation.
        # In a real scenario, this would involve complex logic based on the tool and profile.
        params = {}
        if tool_name == "nmap" and profile.target_type == TargetType.NETWORK_HOST:
            params = {"scan_type": "-sV -T4", "ports": "top-1000"}
        elif tool_name == "nuclei" and profile.target_type == TargetType.WEB_APPLICATION:
            params = {"severity": "critical,high", "templates": "cves,vulnerabilities"}

        return params

    async def generate_attack_chain(self, profile: TargetProfile, objective: str) -> AttackChain:
        """Generate a sequence of attack steps based on the target profile."""
        attack_chain = AttackChain(target_profile=profile)
        selected_tools = await self.select_optimal_tools(profile, objective)

        for tool in selected_tools:
            params = await self.optimize_tool_parameters(tool, profile)
            step = AttackStep(
                tool=tool,
                parameters=params,
                expected_outcome="Gather information or find vulnerabilities.",
                success_probability=0.8,  # Placeholder value
                execution_time_estimate=300  # Placeholder value
            )
            attack_chain.steps.append(step)

        return attack_chain

    # Helper methods ported from the legacy script
    def _determine_target_type(self, target: str) -> TargetType:
        if target.startswith(('http://', 'https://')):
            parsed = urllib.parse.urlparse(target)
            if '/api/' in parsed.path or parsed.path.endswith('/api'):
                return TargetType.API_ENDPOINT
            return TargetType.WEB_APPLICATION
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', target):
            return TargetType.NETWORK_HOST
        if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            return TargetType.WEB_APPLICATION
        if target.endswith(('.exe', '.bin', '.elf', '.so', '.dll')):
            return TargetType.BINARY_FILE
        if any(cloud in target.lower() for cloud in ['amazonaws.com', 'azure', 'googleapis.com']):
            return TargetType.CLOUD_SERVICE
        return TargetType.UNKNOWN

    def _resolve_domain(self, target: str) -> List[str]:
        try:
            hostname = urllib.parse.urlparse(target).hostname or target
            return [socket.gethostbyname(hostname)]
        except (socket.gaierror, TypeError):
            return []

    def _detect_technologies(self, target: str) -> List[TechnologyStack]:
        # Simplified version for now
        technologies = []
        if 'wordpress' in target.lower() or 'wp-' in target.lower():
            technologies.append(TechnologyStack.WORDPRESS)
        if '.php' in target.lower():
            technologies.append(TechnologyStack.PHP)
        if '.asp' in target.lower():
            technologies.append(TechnologyStack.DOTNET)
        return technologies if technologies else [TechnologyStack.UNKNOWN]

    def _detect_cms(self, target: str) -> Optional[str]:
        target_lower = target.lower()
        if 'wordpress' in target_lower or 'wp-' in target_lower:
            return "WordPress"
        if 'drupal' in target_lower:
            return "Drupal"
        if 'joomla' in target_lower:
            return "Joomla"
        return None

    def _calculate_attack_surface(self, profile: TargetProfile) -> float:
        score = 0.0
        type_scores = {
            TargetType.WEB_APPLICATION: 7.0, TargetType.API_ENDPOINT: 6.0,
            TargetType.NETWORK_HOST: 8.0, TargetType.CLOUD_SERVICE: 5.0,
            TargetType.BINARY_FILE: 4.0
        }
        score += type_scores.get(profile.target_type, 3.0)
        score += len(profile.technologies) * 0.5
        score += len(profile.open_ports) * 0.3
        score += len(profile.subdomains) * 0.2
        if profile.cms_type:
            score += 1.5
        return min(score, 10.0)

    def _determine_risk_level(self, profile: TargetProfile) -> str:
        score = profile.attack_surface_score
        if score >= 8.0: return "critical"
        if score >= 6.0: return "high"
        if score >= 4.0: return "medium"
        if score >= 2.0: return "low"
        return "minimal"

    def _calculate_confidence(self, profile: TargetProfile) -> float:
        confidence = 0.5
        if profile.ip_addresses: confidence += 0.1
        if profile.technologies and profile.technologies[0] != TechnologyStack.UNKNOWN: confidence += 0.2
        if profile.cms_type: confidence += 0.1
        if profile.target_type != TargetType.UNKNOWN: confidence += 0.1
        return min(confidence, 1.0)

    def _initialize_tool_effectiveness(self) -> Dict[str, Dict[str, float]]:
        return {
            TargetType.WEB_APPLICATION.value: {
                "nmap": 0.8, "gobuster": 0.9, "nuclei": 0.95, "nikto": 0.85,
                "sqlmap": 0.9, "ffuf": 0.9, "feroxbuster": 0.85, "katana": 0.88,
                "httpx": 0.85, "wpscan": 0.95, "burpsuite": 0.9, "dirsearch": 0.87,
                "gau": 0.82, "waybackurls": 0.8, "arjun": 0.9, "paramspider": 0.85,
                "x8": 0.88, "jaeles": 0.92, "dalfox": 0.93, "anew": 0.7,
                "qsreplace": 0.75, "uro": 0.7
            },
            TargetType.NETWORK_HOST.value: {
                "nmap": 0.95, "nmap-advanced": 0.97, "masscan": 0.92, "rustscan": 0.9,
                "autorecon": 0.95, "enum4linux": 0.8, "enum4linux-ng": 0.88,
                "smbmap": 0.85, "rpcclient": 0.82, "nbtscan": 0.75, "arp-scan": 0.85,
                "responder": 0.88, "hydra": 0.8, "netexec": 0.85, "amass": 0.7
            },
            # ... (other target types from legacy file) ...
        }

    def _initialize_technology_signatures(self) -> Dict[str, Dict[str, List[str]]]:
        return {
            "headers": {
                TechnologyStack.APACHE.value: ["Apache"], TechnologyStack.NGINX.value: ["nginx"],
                TechnologyStack.IIS.value: ["Microsoft-IIS"], TechnologyStack.PHP.value: ["PHP"],
            },
            "content": {
                TechnologyStack.WORDPRESS.value: ["wp-content"], TechnologyStack.DRUPAL.value: ["Drupal"],
            }
        }

    def _initialize_attack_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "web_reconnaissance": [
                {"tool": "nmap", "priority": 1, "params": {"scan_type": "-sV"}},
                {"tool": "httpx", "priority": 2, "params": {"probe": True}},
            ]
        }
