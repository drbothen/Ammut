import asyncio
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from src.server.services.base import AbstractCommandService
from src.server.core.logging import logger, ModernVisualEngine

class CommandService(AbstractCommandService):
    """Service for executing shell commands with caching."""

    def __init__(self, cache_dir: str = "/tmp/ammut_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, command: str) -> Path:
        """Generate a cache file path for a command."""
        command_hash = hashlib.sha256(command.encode()).hexdigest()
        return self.cache_dir / f"{command_hash}.json"

    def _read_from_cache(self, command: str) -> Optional[Dict[str, Any]]:
        """Read command output from cache if available and not expired."""
        cache_file = self._get_cache_path(command)
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cached_data["timestamp"])
            if datetime.now() - cached_time < timedelta(hours=24):
                logger.info(f"{ModernVisualEngine.format_highlighted_text('CACHE HIT', 'GREEN')} for command: {command}")
                return cached_data
        return None

    def _write_to_cache(self, command: str, result: Dict[str, Any]):
        """Write command output to a cache file."""
        cache_file = self._get_cache_path(command)
        result_with_ts = result.copy()
        result_with_ts["timestamp"] = datetime.now().isoformat()
        with open(cache_file, 'w') as f:
            json.dump(result_with_ts, f, indent=4)

    async def get_stats(self) -> Dict[str, Any]:
        """Returns statistics about the command cache."""
        try:
            num_files = len(list(self.cache_dir.glob('*.json')))
            total_size = sum(f.stat().st_size for f in self.cache_dir.glob('*.json'))
            return {
                "success": True,
                "cache_dir": str(self.cache_dir),
                "num_files": num_files,
                "total_size_bytes": total_size,
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"success": False, "error": str(e)}

    async def clear_cache(self) -> Dict[str, Any]:
        """Clears the command cache."""
        try:
            for item in self.cache_dir.iterdir():
                item.unlink()
            logger.info("Command cache cleared.")
            return {"success": True, "message": "Cache cleared successfully."}
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return {"success": False, "error": str(e)}

    async def execute(self, command: str, use_cache: bool = True) -> Dict[str, Any]:
        """Execute a shell command asynchronously with logging, error handling, and caching."""
        logger.info(ModernVisualEngine.format_command_execution(command, 'STARTING'))

        if use_cache:
            cached_result = self._read_from_cache(command)
            if cached_result:
                return cached_result

        start_time = datetime.now()
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=300)
            end_time = datetime.now()

            result = {
                "command": command,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "return_code": process.returncode,
                "success": process.returncode == 0,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": (end_time - start_time).total_seconds()
            }

            if use_cache and result['success']:
                self._write_to_cache(command, result)

        except asyncio.TimeoutError:
            end_time = datetime.now()
            result = {
                "command": command,
                "error": "Command timed out after 5 minutes.",
                "return_code": -1,
                "success": False,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            }
            logger.error(ModernVisualEngine.format_error_card('TIMEOUT', 'CommandService', command))
        except Exception as e:
            end_time = datetime.now()
            result = {
                "command": command,
                "error": str(e),
                "return_code": -1,
                "success": False,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            }
            logger.error(ModernVisualEngine.format_error_card('EXECUTION FAILED', 'CommandService', str(e)))

        return result
