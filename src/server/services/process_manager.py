import psutil
from typing import List, Dict, Any

from .base import AbstractProcessManager
from core.logging import logger

class ProcessManager(AbstractProcessManager):
    """Manages system processes."""

    async def list_processes(self) -> List[Dict[str, Any]]:
        """Lists all running processes with their details."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    async def get_process_status(self, pid: int) -> Dict[str, Any]:
        """Gets the status of a specific process."""
        try:
            proc = psutil.Process(pid)
            return proc.as_dict()
        except psutil.NoSuchProcess:
            return {"error": "Process not found"}

    async def terminate_process(self, pid: int) -> Dict[str, Any]:
        """Terminates a specific process."""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            logger.info(f"Terminated process {pid}")
            return {"success": True, "pid": pid}
        except psutil.NoSuchProcess:
            return {"success": False, "error": "Process not found"}

    async def pause_process(self, pid: int) -> Dict[str, Any]:
        """Pauses a specific process."""
        try:
            proc = psutil.Process(pid)
            proc.suspend()
            logger.info(f"Paused process {pid}")
            return {"success": True, "pid": pid}
        except psutil.NoSuchProcess:
            return {"success": False, "error": "Process not found"}

    async def resume_process(self, pid: int) -> Dict[str, Any]:
        """Resumes a paused process."""
        try:
            proc = psutil.Process(pid)
            proc.resume()
            logger.info(f"Resumed process {pid}")
            return {"success": True, "pid": pid}
        except psutil.NoSuchProcess:
            return {"success": False, "error": "Process not found"}
