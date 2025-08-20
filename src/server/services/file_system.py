import os
import shutil
from pathlib import Path
from typing import Dict, Any, List

from .base import AbstractFileSystem
from core.logging import logger

class FileSystem(AbstractFileSystem):
    """Provides functionalities for file system operations."""

    async def create_file(self, path: str, content: str) -> Dict[str, Any]:
        """Creates a new file with the given content."""
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            logger.info(f"File created at {path}")
            return {"success": True, "path": path}
        except Exception as e:
            logger.error(f"Error creating file at {path}: {e}")
            return {"success": False, "error": str(e)}

    async def modify_file(self, path: str, content: str) -> Dict[str, Any]:
        """Modifies an existing file with the given content."""
        try:
            p = Path(path)
            if not p.exists():
                return {"success": False, "error": "File not found"}
            p.write_text(content)
            logger.info(f"File modified at {path}")
            return {"success": True, "path": path}
        except Exception as e:
            logger.error(f"Error modifying file at {path}: {e}")
            return {"success": False, "error": str(e)}

    async def delete_path(self, path: str) -> Dict[str, Any]:
        """Deletes a file or directory."""
        try:
            p = Path(path)
            if not p.exists():
                return {"success": False, "error": "Path not found"}
            if p.is_dir():
                shutil.rmtree(p)
                logger.info(f"Directory deleted: {path}")
            else:
                p.unlink()
                logger.info(f"File deleted: {path}")
            return {"success": True, "path": path}
        except Exception as e:
            logger.error(f"Error deleting path {path}: {e}")
            return {"success": False, "error": str(e)}

    async def list_files(self, path: str) -> Dict[str, Any]:
        """Lists files and directories at the given path."""
        try:
            p = Path(path)
            if not p.exists() or not p.is_dir():
                return {"success": False, "error": "Directory not found"}
            
            files = [str(item) for item in p.iterdir()]
            logger.info(f"Listed files in {path}")
            return {"success": True, "path": path, "files": files}
        except Exception as e:
            logger.error(f"Error listing files in {path}: {e}")
            return {"success": False, "error": str(e)}
