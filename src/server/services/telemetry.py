import psutil
import time
from typing import Dict, Any

from .base import AbstractTelemetry

class Telemetry(AbstractTelemetry):
    """Provides system and application telemetry data."""
    def __init__(self):
        self.start_time = time.time()

    async def get_stats(self) -> Dict[str, Any]:
        """Gathers and returns telemetry statistics."""
        return {
            "cpu_usage_percent": psutil.cpu_percent(),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "uptime_seconds": time.time() - self.start_time
        }
