import json
from typing import Dict, Any

from .base import AbstractTechnologyDetector
from src.server.services.base import AbstractCommandService
from src.server.core.logging import logger

class TechnologyDetector(AbstractTechnologyDetector):
    """Detects technologies used by a web application."""

    def __init__(self, command_service: AbstractCommandService):
        self.command_service = command_service

    async def detect(self, target: str) -> Dict[str, Any]:
        """Uses whatweb to identify technologies."""
        logger.info(f"Starting technology detection for {target}")
        
        # Construct the whatweb command
        # The --log-json flag outputs results in a machine-readable format.
        command = f"whatweb --log-json - {target}"
        
        result = await self.command_service.execute(command)

        if not result["success"] or not result["stdout"]:
            logger.error(f"Technology detection failed for {target}. Error: {result.get('stderr', 'No output')}")
            return {"error": "Failed to detect technologies.", "details": result.get('stderr')}

        try:
            # The output is a list of JSON objects, one per target URL.
            # We are only scanning one, so we take the first element.
            detected_info = json.loads(result["stdout"])[0]
            
            # Extract key information
            technologies = {}
            if 'plugins' in detected_info:
                for name, plugin_data in detected_info['plugins'].items():
                    tech_info = {}
                    if 'version' in plugin_data:
                        tech_info['version'] = plugin_data['version']
                    if 'string' in plugin_data:
                        tech_info['string'] = plugin_data['string']
                    technologies[name] = tech_info

            logger.info(f"Successfully detected technologies for {target}")
            return {"target": detected_info.get('target'), "technologies": technologies}
        except (json.JSONDecodeError, IndexError) as e:
            logger.error(f"Failed to parse whatweb output for {target}. Error: {e}")
            return {"error": "Failed to parse detection results.", "raw_output": result["stdout"]}
