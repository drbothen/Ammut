import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModernVisualEngine:
    """A class to provide modern, visually appealing terminal output."""

    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'BG_RED': '\033[41m',
        'BG_GREEN': '\033[42m',
        'BG_YELLOW': '\033[43m',
        'BG_BLUE': '\033[44m',
        'BG_MAGENTA': '\033[45m',
        'BG_CYAN': '\033[46m',
        'FIRE_RED': '\033[38;5;196m',
        'BLOOD_RED': '\033[38;5;88m',
        'CRIMSON': '\033[38;5;124m',
        'SUCCESS': '\033[38;5;46m',
    }

    @staticmethod
    def format_text(text, *styles):
        """Apply multiple styles to text."""
        style_str = ''.join(ModernVisualEngine.COLORS.get(s.upper(), '') for s in styles)
        return f"{style_str}{text}{ModernVisualEngine.COLORS['RESET']}"

    @staticmethod
    def create_section_header(title: str, icon: str = '🚀', color: str = 'CYAN') -> str:
        """Creates a visually appealing section header."""
        header = f"\n{icon} {ModernVisualEngine.format_text(title.upper(), 'BOLD', color, 'UNDERLINE')}"
        return header

    @staticmethod
    def format_tool_status(tool_name: str, status: str, message: str = '') -> str:
        """Formats the status of a tool execution."""
        status_colors = {
            'SUCCESS': 'GREEN',
            'FAILED': 'RED',
            'RUNNING': 'YELLOW',
            'INFO': 'BLUE'
        }
        color = status_colors.get(status.upper(), 'WHITE')
        return f"[{ModernVisualEngine.format_text(tool_name, 'BOLD')}] [{ModernVisualEngine.format_text(status, color)}] {message}"

    @staticmethod
    def format_command_execution(command: str, status: str) -> str:
        """Formats a command execution log."""
        return f"{ModernVisualEngine.format_text('CMD', 'MAGENTA')} [{status}]> {command}"

    @staticmethod
    def format_error_card(title: str, component: str, message: str) -> str:
        """Creates a formatted error card."""
        card = (
            f"{ModernVisualEngine.COLORS['BG_RED']}{ModernVisualEngine.COLORS['WHITE']}{ModernVisualEngine.COLORS['BOLD']}"
            f"{title:^50}\n"
            f"{'='*50}\n"
            f" Component: {component}\n"
            f" Message: {message}\n"
            f"{'='*50}"
            f"{ModernVisualEngine.COLORS['RESET']}"
        )
        return card

    @staticmethod
    def format_highlighted_text(text: str, color: str = 'YELLOW') -> str:
        """Highlights text with a specific color."""
        return ModernVisualEngine.format_text(text, color, 'BOLD')

    @staticmethod
    def format_vulnerability_severity(severity: str, count: int) -> str:
        """Formats vulnerability severity with appropriate colors."""
        severity_colors = {
            'CRITICAL': 'BG_RED',
            'HIGH': 'RED',
            'MEDIUM': 'YELLOW',
            'LOW': 'BLUE'
        }
        color = severity_colors.get(severity.upper(), 'WHITE')
        return f"- {ModernVisualEngine.format_text(severity, color)}: {count}"
