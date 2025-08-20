from typing import Dict, List, Optional

from src.server.services.base import TechnologyDetectionServiceBase
from src.server.core.technology_detection import DETECTION_PATTERNS, PORT_SERVICES

class TechnologyDetectionService(TechnologyDetectionServiceBase):
    """Service for detecting technologies based on various signatures."""

    async def detect_technologies(
        self,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        ports: Optional[List[int]] = None
    ) -> Dict[str, List[str]]:
        """Comprehensive technology detection based on headers, content, and ports."""
        detected = {
            "web_servers": [],
            "frameworks": [],
            "cms": [],
            "databases": [],
            "languages": [],
            "security": [],
            "services": []
        }

        # Header-based detection
        if headers:
            for category, tech_patterns in DETECTION_PATTERNS.items():
                for tech, patterns in tech_patterns.items():
                    for header_name, header_value in headers.items():
                        for pattern in patterns:
                            if pattern.lower() in header_value.lower() or pattern.lower() in header_name.lower():
                                if tech not in detected[category]:
                                    detected[category].append(tech)

        # Content-based detection
        if content:
            content_lower = content.lower()
            for category, tech_patterns in DETECTION_PATTERNS.items():
                for tech, patterns in tech_patterns.items():
                    for pattern in patterns:
                        if pattern.lower() in content_lower:
                            if tech not in detected[category]:
                                detected[category].append(tech)

        # Port-based service detection
        if ports:
            for port in ports:
                if port in PORT_SERVICES:
                    service = PORT_SERVICES[port]
                    if service not in detected["services"]:
                        detected["services"].append(service)

        return detected
