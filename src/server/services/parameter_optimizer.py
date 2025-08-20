from typing import Dict, Any

from .base import AbstractParameterOptimizer
from core.logging import logger

class ParameterOptimizer(AbstractParameterOptimizer):
    """Optimizes tool parameters based on target information."""

    def optimize_parameters(self, tool_name: str, target_info: Dict[str, Any]) -> Dict[str, Any]:
        """Suggests optimized parameters for a given tool and target."""
        logger.info(f"Optimizing parameters for {tool_name} against target with info: {target_info}")
        
        base_params = {}
        # Generic optimization: if rate limiting is detected, suggest a delay.
        if target_info.get("rate_limit_detected"):
            logger.warning("Rate limiting detected, adding a delay parameter where applicable.")
            base_params['delay'] = "--delay 500ms" # Example for a tool that supports it

        # Tool-specific optimizations
        if tool_name == 'nmap':
            if 'technologies' in target_info and 'iis' in target_info['technologies']:
                base_params['scripts'] = "--script=http-iis-webdav-vuln"
            else:
                base_params['scripts'] = "-sV -sC" # Default scripts
            base_params['timing'] = "-T4" # Aggressive timing

        elif tool_name == 'gobuster':
            base_params['wordlist'] = "-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
            if 'technologies' in target_info:
                if 'php' in target_info['technologies']:
                    base_params['extensions'] = "-x php,txt,html"
                elif 'asp.net' in target_info['technologies']:
                    base_params['extensions'] = "-x aspx,asp,html"
        
        elif tool_name == 'nuclei':
            base_params['templates'] = "-t /path/to/nuclei-templates/"
            if 'technologies' in target_info:
                tech_list = ','.join(target_info['technologies'].keys())
                if tech_list:
                    base_params['autotag'] = f"-tags {tech_list}"

        logger.info(f"Optimized parameters for {tool_name}: {base_params}")
        return base_params

parameter_optimizer = ParameterOptimizer()
