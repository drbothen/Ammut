import asyncio
import httpx
from typing import Dict, Any, List

from .base import AbstractRateLimitDetector
from core.logging import logger

class RateLimitDetector(AbstractRateLimitDetector):
    """Detects rate limiting on a target URL."""

    async def check_rate_limit(self, url: str, request_count: int = 20) -> Dict[str, Any]:
        """Sends a burst of requests to a URL to check for rate limiting."""
        logger.info(f"Checking for rate limiting on {url} with {request_count} requests.")
        status_codes: List[int] = []
        errors = 0

        async with httpx.AsyncClient() as client:
            tasks = [client.get(url, timeout=10) for _ in range(request_count)]
            responses = await asyncio.gather(*tasks, return_exceptions=True)

        for response in responses:
            if isinstance(response, httpx.Response):
                status_codes.append(response.status_code)
            else:
                errors += 1
                logger.warning(f"Request failed during rate limit check: {response}")

        rate_limit_detected = any(code == 429 for code in status_codes)
        status_code_distribution = {str(code): status_codes.count(code) for code in set(status_codes)}

        result = {
            "rate_limit_detected": rate_limit_detected,
            "status_codes": status_code_distribution,
            "total_requests": request_count,
            "successful_requests": len(status_codes),
            "failed_requests": errors
        }

        if rate_limit_detected:
            logger.warning(f"Rate limiting detected on {url}. Status codes: {status_code_distribution}")
        else:
            logger.info(f"No rate limiting detected on {url}.")

        return result

rate_limit_detector = RateLimitDetector()
