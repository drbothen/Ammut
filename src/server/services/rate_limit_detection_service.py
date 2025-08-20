import re
from typing import Dict, Any, Optional

from src.server.services.base import RateLimitDetectionServiceBase
from src.server.core.rate_limit_detection import RATE_LIMIT_INDICATORS, TIMING_PROFILES

class RateLimitDetectionService(RateLimitDetectionServiceBase):
    """Service for detecting rate limiting and adjusting timing."""

    async def detect_rate_limiting(
        self,
        response_text: str,
        status_code: int,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Detects rate limiting from a response and recommends a timing profile."""
        rate_limit_detected = False
        confidence = 0.0
        indicators_found = []

        if status_code == 429:
            rate_limit_detected = True
            confidence += 0.8
            indicators_found.append("HTTP 429 status")

        response_lower = response_text.lower()
        for indicator in RATE_LIMIT_INDICATORS:
            if indicator in response_lower:
                rate_limit_detected = True
                confidence += 0.2
                indicators_found.append(f"Text: '{indicator}'")

        if headers:
            rate_limit_headers = ["x-ratelimit", "retry-after", "x-rate-limit"]
            for header_name in headers.keys():
                for rl_header in rate_limit_headers:
                    if rl_header.lower() in header_name.lower():
                        rate_limit_detected = True
                        confidence += 0.3
                        indicators_found.append(f"Header: {header_name}")

        confidence = min(1.0, confidence)

        return {
            "detected": rate_limit_detected,
            "confidence": confidence,
            "indicators": indicators_found,
            "recommended_profile": self._recommend_timing_profile(confidence)
        }

    def _recommend_timing_profile(self, confidence: float) -> str:
        """Recommends a timing profile based on rate limit confidence."""
        if confidence >= 0.8:
            return "stealth"
        elif confidence >= 0.5:
            return "conservative"
        elif confidence >= 0.2:
            return "normal"
        else:
            return "aggressive"

    async def adjust_timing(
        self,
        current_params: Dict[str, Any],
        profile: str
    ) -> Dict[str, Any]:
        """Adjusts timing parameters based on a recommended profile."""
        timing = TIMING_PROFILES.get(profile, TIMING_PROFILES["normal"])
        adjusted_params = current_params.copy()

        if "threads" in adjusted_params:
            adjusted_params["threads"] = timing["threads"]
        if "delay" in adjusted_params:
            adjusted_params["delay"] = timing["delay"]
        if "timeout" in adjusted_params:
            adjusted_params["timeout"] = timing["timeout"]

        return adjusted_params
