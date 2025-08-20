from typing import Dict, Any

from src.server.core.config import settings
from src.server.services.base import AbstractVisualEngine

class VisualEngine(AbstractVisualEngine):
    """Beautiful, modern output formatting with animations and colors"""

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
        'PRIMARY_BORDER': '\033[38;5;160m',
        'ACCENT_LINE': '\033[38;5;196m',
        'ACCENT_GRADIENT': '\033[38;5;124m',
        'VULN_CRITICAL': '\033[48;5;124m\033[38;5;15m\033[1m',
        'TOOL_SUCCESS': '\033[38;5;46m\033[1m',
        'TOOL_FAILED': '\033[38;5;196m\033[1m',
        'TOOL_TIMEOUT': '\033[38;5;208m\033[1m',
        'TOOL_RECOVERY': '\033[38;5;129m\033[1m',
        'TOOL_RUNNING': '\033[38;5;46m\033[5m',
        'PROGRESS_BAR': '\033[38;5;46m',
        'PROGRESS_EMPTY': '\033[38;5;240m',
    }

    def create_banner(self) -> str:
        """Create the enhanced HexStrike banner"""
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

{self.COLORS['TERMINAL_GRAY']}[INFO] Server starting on {settings.AMMUT_HOST}:{settings.AMMUT_PORT}
[INFO] 150+ integrated modules | Adaptive AI decision engine active
[INFO] Blood-red theme engaged – unified offensive operations UI{RESET}
"""
        return banner

    def create_live_dashboard(self, processes: Dict[int, Dict[str, Any]]) -> str:
        """Create a live dashboard showing all active processes"""
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
        """Format vulnerability as a beautiful card"""
        severity = vuln_data.get('severity', 'unknown').upper()
        name = vuln_data.get('name', 'Unknown Vulnerability')
        description = vuln_data.get('description', 'No description available')
        
        severity_colors = {
            'CRITICAL': self.COLORS['VULN_CRITICAL'],
            'HIGH': self.COLORS['HACKER_RED'],
            'MEDIUM': self.COLORS['ACCENT_GRADIENT'],
            'LOW': self.COLORS['CYBER_ORANGE'],
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
        """Format error information as a highlighted card with reddish tones"""
        error_colors = {
            'CRITICAL': self.COLORS['VULN_CRITICAL'],
            'ERROR': self.COLORS['TOOL_FAILED'],
            'TIMEOUT': self.COLORS['TOOL_TIMEOUT'],
            'RECOVERY': self.COLORS['TOOL_RECOVERY'],
        }
        
        color = error_colors.get(error_type.upper(), self.COLORS['TOOL_FAILED'])
        
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
        """Format tool execution status with enhanced highlighting"""
        status_colors = {
            'RUNNING': self.COLORS['TOOL_RUNNING'],
            'SUCCESS': self.COLORS['TOOL_SUCCESS'],
            'FAILED': self.COLORS['TOOL_FAILED'],
            'TIMEOUT': self.COLORS['TOOL_TIMEOUT'],
            'RECOVERY': self.COLORS['TOOL_RECOVERY']
        }
        
        color = status_colors.get(status.upper(), self.COLORS['BRIGHT_WHITE'])
        
        progress_bar = ""
        if progress > 0:
            filled = int(20 * progress)
            empty = 20 - filled
            progress_bar = f" [{self.COLORS['PROGRESS_BAR']}{'█' * filled}{self.COLORS['PROGRESS_EMPTY']}{'░' * empty}{self.COLORS['RESET']}] {progress*100:.1f}%"
        
        return f"{color}🔧 {tool_name.upper()}{self.COLORS['RESET']} | {color}{status}{self.COLORS['RESET']} | {self.COLORS['BRIGHT_WHITE']}{target}{self.COLORS['RESET']}{progress_bar}"
