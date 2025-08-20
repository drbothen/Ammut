from typing import Dict, Any

from src.server.services.base import VisualEngineServiceBase


class VisualEngineService(VisualEngineServiceBase):
    """A service for creating beautiful, modern output formatting with animations and colors."""

    COLORS = {
        'MATRIX_GREEN': '\033[38;5;46m',
        'NEON_BLUE': '\033[38;5;51m',
        'ELECTRIC_PURPLE': '\033[38;5;129m',
        'CYBER_ORANGE': '\033[38;5;208m',
        'HACKER_RED': '\033[38;5;196m',
        'TERMINAL_GRAY': '\033[38;5;240m',
        'BRIGHT_WHITE': '\033[97m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
        'BLOOD_RED': '\033[38;5;124m',
        'CRIMSON': '\033[38;5;160m',
        'DARK_RED': '\033[38;5;88m',
        'FIRE_RED': '\033[38;5;202m',
        'ROSE_RED': '\033[38;5;167m',
        'BURGUNDY': '\033[38;5;52m',
        'SCARLET': '\033[38;5;197m',
        'RUBY': '\033[38;5;161m',
        'PRIMARY_BORDER': '\033[38;5;160m',
        'ACCENT_LINE': '\033[38;5;196m',
        'ACCENT_GRADIENT': '\033[38;5;124m',
        'HIGHLIGHT_RED': '\033[48;5;196m\033[38;5;15m',
        'HIGHLIGHT_YELLOW': '\033[48;5;226m\033[38;5;16m',
        'HIGHLIGHT_GREEN': '\033[48;5;46m\033[38;5;16m',
        'HIGHLIGHT_BLUE': '\033[48;5;51m\033[38;5;16m',
        'HIGHLIGHT_PURPLE': '\033[48;5;129m\033[38;5;15m',
        'SUCCESS': '\033[38;5;46m',
        'WARNING': '\033[38;5;208m',
        'ERROR': '\033[38;5;196m',
        'CRITICAL': '\033[48;5;196m\033[38;5;15m\033[1m',
        'INFO': '\033[38;5;51m',
        'DEBUG': '\033[38;5;240m',
        'VULN_CRITICAL': '\033[48;5;124m\033[38;5;15m\033[1m',
        'VULN_HIGH': '\033[38;5;196m\033[1m',
        'VULN_MEDIUM': '\033[38;5;208m\033[1m',
        'VULN_LOW': '\033[38;5;226m',
        'VULN_INFO': '\033[38;5;51m',
        'TOOL_RUNNING': '\033[38;5;46m\033[5m',
        'TOOL_SUCCESS': '\033[38;5;46m\033[1m',
        'TOOL_FAILED': '\033[38;5;196m\033[1m',
        'TOOL_TIMEOUT': '\033[38;5;208m\033[1m',
        'TOOL_RECOVERY': '\033[38;5;129m\033[1m',
        'PROGRESS_BAR': '\033[38;5;46m',
        'PROGRESS_EMPTY': '\033[38;5;240m',
        'SPINNER': '\033[38;5;51m',
        'PULSE': '\033[38;5;196m\033[5m'
    }

    PROGRESS_STYLES = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'bars': [' ', '▂', '▃', '▄', '▅', '▆', '▇', '█'],
        'arrows': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'pulse': ['●', '◐', '◑', '◒', '◓', '◔', '◕', '◖', '◗', '◘']
    }

    def create_banner(self) -> str:
        border_color = self.COLORS['PRIMARY_BORDER']
        accent = self.COLORS['ACCENT_LINE']
        gradient = self.COLORS['ACCENT_GRADIENT']
        RESET = self.COLORS['RESET']
        BOLD = self.COLORS['BOLD']
        title_block = f"{accent}{BOLD}"
        banner = f"""
{title_block}
██╗  ██╗███████╗██╗  ██╗███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
██║  ██║██╔════╝╚██╗██╔╝██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
███████║█████╗   ╚███╔╝ ███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  
██╔══██║██╔══╝   ██╔██╗ ╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  
██║  ██║███████╗██╔╝ ██╗███████║   ██║   ██║  ██║██║██║  ██╗███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
{RESET}
{border_color}┌─────────────────────────────────────────────────────────────────────┐
│  {self.COLORS['BRIGHT_WHITE']}🚀 HexStrike AI - Blood-Red Offensive Intelligence Core{border_color}        │
│  {accent}⚡ AI-Automated Recon | Exploitation | Analysis Pipeline{border_color}          │
│  {gradient}🎯 Bug Bounty | CTF | Red Team | Zero-Day Research{border_color}              │
└─────────────────────────────────────────────────────────────────────┘{RESET}
"""
        return banner

    def create_progress_bar(self, current: int, total: int, width: int = 50, tool: str = "") -> str:
        percentage = min(100, (current / total) * 100) if total > 0 else 0
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        border = self.COLORS['PRIMARY_BORDER']
        fill_col = self.COLORS['ACCENT_LINE']
        return f"""
{border}┌─ {tool} ─{'─' * (width - len(tool) - 4)}┐
│ {fill_col}{bar}{border} │ {percentage:6.1f}%
└─{'─' * (width + 10)}┘{self.COLORS['RESET']}"""

    def render_progress_bar(self, progress: float, width: int = 40, style: str = 'cyber', label: str = "", eta: float = 0, speed: str = "") -> str:
        progress = max(0.0, min(1.0, progress))
        filled_width = int(width * progress)
        empty_width = width - filled_width
        if style == 'cyber':
            filled_char, empty_char, bar_color, progress_color = '█', '░', self.COLORS['ACCENT_LINE'], self.COLORS['PRIMARY_BORDER']
        elif style == 'matrix':
            filled_char, empty_char, bar_color, progress_color = '▓', '▒', self.COLORS['ACCENT_LINE'], self.COLORS['ACCENT_GRADIENT']
        elif style == 'neon':
            filled_char, empty_char, bar_color, progress_color = '━', '─', self.COLORS['PRIMARY_BORDER'], self.COLORS['CYBER_ORANGE']
        else:
            filled_char, empty_char, bar_color, progress_color = '█', '░', self.COLORS['ACCENT_LINE'], self.COLORS['PRIMARY_BORDER']
        filled_part = bar_color + filled_char * filled_width
        empty_part = self.COLORS['TERMINAL_GRAY'] + empty_char * empty_width
        percentage = f"{progress * 100:.1f}%"
        extra_info = ""
        if eta > 0:
            extra_info += f" ETA: {eta:.1f}s"
        if speed:
            extra_info += f" Speed: {speed}"
        bar_display = f"[{filled_part}{empty_part}{self.COLORS['RESET']}] {progress_color}{percentage}{self.COLORS['RESET']}"
        return f"{label}: {bar_display}{extra_info}" if label else f"{bar_display}{extra_info}"

    def create_live_dashboard(self, processes: Dict[int, Dict[str, Any]]) -> str:
        if not processes:
            return f"""
{self.COLORS['PRIMARY_BORDER']}╭─────────────────────────────────────────────────────────────────────────────╮
│ {self.COLORS['ACCENT_LINE']}📊 HEXSTRIKE LIVE DASHBOARD{self.COLORS['PRIMARY_BORDER']}                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ {self.COLORS['TERMINAL_GRAY']}No active processes currently running{self.COLORS['PRIMARY_BORDER']}                                    │
╰─────────────────────────────────────────────────────────────────────────────╯{self.COLORS['RESET']}
"""
        dashboard_lines = [
            f"{self.COLORS['PRIMARY_BORDER']}╭─────────────────────────────────────────────────────────────────────────────╮",
            f"│ {self.COLORS['ACCENT_LINE']}📊 HEXSTRIKE LIVE DASHBOARD{self.COLORS['PRIMARY_BORDER']}                                           │",
            f"├─────────────────────────────────────────────────────────────────────────────┤"
        ]
        for pid, proc_info in processes.items():
            status = proc_info.get('status', 'unknown')
            command = proc_info.get('command', 'unknown')[:50] + "..." if len(proc_info.get('command', '')) > 50 else proc_info.get('command', 'unknown')
            status_color = self.COLORS['ACCENT_LINE'] if status == 'running' else self.COLORS['HACKER_RED']
            dashboard_lines.append(
                f"│ {self.COLORS['CYBER_ORANGE']}PID {pid}{self.COLORS['PRIMARY_BORDER']} | {status_color}{status}{self.COLORS['PRIMARY_BORDER']} | {self.COLORS['BRIGHT_WHITE']}{command}{self.COLORS['PRIMARY_BORDER']} │"
            )
        dashboard_lines.append(f"╰─────────────────────────────────────────────────────────────────────────────╯{self.COLORS['RESET']}")
        return "\n".join(dashboard_lines)

    def format_vulnerability_card(self, vuln_data: Dict[str, Any]) -> str:
        severity = vuln_data.get('severity', 'unknown').upper()
        name = vuln_data.get('name', 'Unknown Vulnerability')
        description = vuln_data.get('description', 'No description available')
        severity_colors = {
            'CRITICAL': self.COLORS['VULN_CRITICAL'], 'HIGH': self.COLORS['HACKER_RED'],
            'MEDIUM': self.COLORS['ACCENT_GRADIENT'], 'LOW': self.COLORS['CYBER_ORANGE'],
            'INFO': self.COLORS['TERMINAL_GRAY']
        }
        color = severity_colors.get(severity, self.COLORS['TERMINAL_GRAY'])
        return f"""
{color}┌─ 🚨 VULNERABILITY DETECTED ─────────────────────────────────────┐
│ {self.COLORS['BRIGHT_WHITE']}{name:<60}{color} │
│ {self.COLORS['TERMINAL_GRAY']}Severity: {color}{severity:<52}{color} │
│ {self.COLORS['TERMINAL_GRAY']}{description[:58]:<58}{color} │
└─────────────────────────────────────────────────────────────────┘{self.COLORS['RESET']}"""

    def format_error_card(self, error_type: str, tool_name: str, error_message: str, recovery_action: str = "") -> str:
        error_colors = {
            'CRITICAL': self.COLORS['VULN_CRITICAL'], 'ERROR': self.COLORS['TOOL_FAILED'],
            'TIMEOUT': self.COLORS['TOOL_TIMEOUT'], 'RECOVERY': self.COLORS['TOOL_RECOVERY'],
            'WARNING': self.COLORS['WARNING']
        }
        color = error_colors.get(error_type.upper(), self.COLORS['ERROR'])
        card = f"""
{color}┌─ 🔥 ERROR DETECTED ─────────────────────────────────────────────┐{self.COLORS['RESET']}
{color}│ {self.COLORS['BRIGHT_WHITE']}Tool: {tool_name:<55}{color} │{self.COLORS['RESET']}
{color}│ {self.COLORS['BRIGHT_WHITE']}Type: {error_type:<55}{color} │{self.COLORS['RESET']}
{color}│ {self.COLORS['BRIGHT_WHITE']}Error: {error_message[:53]:<53}{color} │{self.COLORS['RESET']}"""
        if recovery_action:
            card += f"""
{color}│ {self.COLORS['TOOL_RECOVERY']}Recovery: {recovery_action[:50]:<50}{color} │{self.COLORS['RESET']}"""
        card += f"""
{color}└─────────────────────────────────────────────────────────────────┘{self.COLORS['RESET']}"""
        return card

    def format_tool_status(self, tool_name: str, status: str, target: str = "", progress: float = 0.0) -> str:
        status_colors = {
            'RUNNING': self.COLORS['TOOL_RUNNING'], 'SUCCESS': self.COLORS['TOOL_SUCCESS'],
            'FAILED': self.COLORS['TOOL_FAILED'], 'TIMEOUT': self.COLORS['TOOL_TIMEOUT'],
            'RECOVERY': self.COLORS['TOOL_RECOVERY']
        }
        color = status_colors.get(status.upper(), self.COLORS['INFO'])
        progress_bar = ""
        if progress > 0:
            filled = int(20 * progress)
            empty = 20 - filled
            progress_bar = f" [{self.COLORS['PROGRESS_BAR']}{'█' * filled}{self.COLORS['PROGRESS_EMPTY']}{'░' * empty}{self.COLORS['RESET']}] {progress*100:.1f}%"
        return f"{color}🔧 {tool_name.upper()}{self.COLORS['RESET']} | {color}{status}{self.COLORS['RESET']} | {self.COLORS['BRIGHT_WHITE']}{target}{self.COLORS['RESET']}{progress_bar}"

    def format_highlighted_text(self, text: str, highlight_type: str = "RED") -> str:
        highlight_colors = {
            'RED': self.COLORS['HIGHLIGHT_RED'], 'YELLOW': self.COLORS['HIGHLIGHT_YELLOW'],
            'GREEN': self.COLORS['HIGHLIGHT_GREEN'], 'BLUE': self.COLORS['HIGHLIGHT_BLUE'],
            'PURPLE': self.COLORS['HIGHLIGHT_PURPLE']
        }
        color = highlight_colors.get(highlight_type.upper(), self.COLORS['HIGHLIGHT_RED'])
        return f"{color} {text} {self.COLORS['RESET']}"

    def format_vulnerability_severity(self, severity: str, count: int = 0) -> str:
        severity_colors = {
            'CRITICAL': self.COLORS['VULN_CRITICAL'], 'HIGH': self.COLORS['VULN_HIGH'],
            'MEDIUM': self.COLORS['VULN_MEDIUM'], 'LOW': self.COLORS['VULN_LOW'],
            'INFO': self.COLORS['VULN_INFO']
        }
        color = severity_colors.get(severity.upper(), self.COLORS['INFO'])
        count_text = f" ({count})" if count > 0 else ""
        return f"{color}{severity.upper()}{count_text}{self.COLORS['RESET']}"

    def create_section_header(self, title: str, icon: str = "🔥", color: str = "FIRE_RED") -> str:
        header_color = self.COLORS.get(color, self.COLORS['FIRE_RED'])
        return f"""
{header_color}{'═' * 70}{self.COLORS['RESET']}
{header_color}{icon} {title.upper()}{self.COLORS['RESET']}
{header_color}{'═' * 70}{self.COLORS['RESET']}"""

    def format_command_execution(self, command: str, status: str, duration: float = 0.0) -> str:
        status_colors = {
            'STARTING': self.COLORS['INFO'], 'RUNNING': self.COLORS['TOOL_RUNNING'],
            'SUCCESS': self.COLORS['TOOL_SUCCESS'], 'FAILED': self.COLORS['TOOL_FAILED'],
            'TIMEOUT': self.COLORS['TOOL_TIMEOUT']
        }
        color = status_colors.get(status.upper(), self.COLORS['INFO'])
        duration_text = f" ({duration:.2f}s)" if duration > 0 else ""
        return f"{color}▶ {command[:60]}{'...' if len(command) > 60 else ''} | {status.upper()}{duration_text}{self.COLORS['RESET']}"
