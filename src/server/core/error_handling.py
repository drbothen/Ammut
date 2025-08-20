from models.enums import ErrorType, RecoveryAction
from typing import Dict, Any, List

ERROR_PATTERNS: Dict[str, ErrorType] = {
    # Timeout patterns
    r"timeout|timed out|connection timeout|read timeout": ErrorType.TIMEOUT,
    r"operation timed out|command timeout": ErrorType.TIMEOUT,
    # Permission patterns
    r"permission denied|access denied|forbidden|not authorized": ErrorType.PERMISSION_DENIED,
    r"sudo required|root required|insufficient privileges": ErrorType.PERMISSION_DENIED,
    # Network patterns
    r"network unreachable|host unreachable|no route to host": ErrorType.NETWORK_UNREACHABLE,
    r"connection refused|connection reset|network error": ErrorType.NETWORK_UNREACHABLE,
    # Rate limiting patterns
    r"rate limit|too many requests|throttled|429": ErrorType.RATE_LIMITED,
    r"request limit exceeded|quota exceeded": ErrorType.RATE_LIMITED,
    # Tool not found patterns
    r"command not found|no such file or directory|not found": ErrorType.TOOL_NOT_FOUND,
    r"executable not found|binary not found": ErrorType.TOOL_NOT_FOUND,
    # Parameter patterns
    r"invalid argument|invalid option|unknown option": ErrorType.INVALID_PARAMETERS,
    r"bad parameter|invalid parameter|syntax error": ErrorType.INVALID_PARAMETERS,
    # Resource patterns
    r"out of memory|memory error|disk full|no space left": ErrorType.RESOURCE_EXHAUSTED,
    r"resource temporarily unavailable|too many open files": ErrorType.RESOURCE_EXHAUSTED,
    # Authentication patterns
    r"authentication failed|login failed|invalid credentials": ErrorType.AUTHENTICATION_FAILED,
    r"unauthorized|invalid token|expired token": ErrorType.AUTHENTICATION_FAILED,
    # Target patterns
    r"target unreachable|target not responding|target down": ErrorType.TARGET_UNREACHABLE,
    r"host not found|dns resolution failed": ErrorType.TARGET_UNREACHABLE,
    # Parsing patterns
    r"parse error|parsing failed|invalid format|malformed": ErrorType.PARSING_ERROR,
    r"json decode error|xml parse error|invalid json": ErrorType.PARSING_ERROR
}

RECOVERY_STRATEGIES: Dict[ErrorType, List[Dict[str, Any]]] = {
    ErrorType.TIMEOUT: [
        {"action": RecoveryAction.RETRY_WITH_BACKOFF, "parameters": {"initial_delay": 5, "max_delay": 60}, "max_attempts": 3, "backoff_multiplier": 2.0, "success_probability": 0.7, "estimated_time": 30},
        {"action": RecoveryAction.RETRY_WITH_REDUCED_SCOPE, "parameters": {"reduce_threads": True, "reduce_timeout": True}, "max_attempts": 2, "backoff_multiplier": 1.0, "success_probability": 0.8, "estimated_time": 45},
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"prefer_faster_tools": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.6, "estimated_time": 60}
    ],
    ErrorType.PERMISSION_DENIED: [
        {"action": RecoveryAction.ESCALATE_TO_HUMAN, "parameters": {"message": "Privilege escalation required", "urgency": "medium"}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.9, "estimated_time": 300},
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"require_no_privileges": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.5, "estimated_time": 30}
    ],
    ErrorType.NETWORK_UNREACHABLE: [
        {"action": RecoveryAction.RETRY_WITH_BACKOFF, "parameters": {"initial_delay": 10, "max_delay": 120}, "max_attempts": 3, "backoff_multiplier": 2.0, "success_probability": 0.6, "estimated_time": 60},
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"prefer_offline_tools": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.4, "estimated_time": 30}
    ],
    ErrorType.RATE_LIMITED: [
        {"action": RecoveryAction.RETRY_WITH_BACKOFF, "parameters": {"initial_delay": 30, "max_delay": 300}, "max_attempts": 5, "backoff_multiplier": 1.5, "success_probability": 0.9, "estimated_time": 180},
        {"action": RecoveryAction.ADJUST_PARAMETERS, "parameters": {"reduce_rate": True, "increase_delays": True}, "max_attempts": 2, "backoff_multiplier": 1.0, "success_probability": 0.8, "estimated_time": 120}
    ],
    ErrorType.TOOL_NOT_FOUND: [
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"find_equivalent": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.7, "estimated_time": 15},
        {"action": RecoveryAction.ESCALATE_TO_HUMAN, "parameters": {"message": "Tool installation required", "urgency": "low"}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.9, "estimated_time": 600}
    ],
    ErrorType.INVALID_PARAMETERS: [
        {"action": RecoveryAction.ADJUST_PARAMETERS, "parameters": {"use_defaults": True, "remove_invalid": True}, "max_attempts": 3, "backoff_multiplier": 1.0, "success_probability": 0.8, "estimated_time": 10},
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"simpler_interface": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.6, "estimated_time": 30}
    ],
    ErrorType.RESOURCE_EXHAUSTED: [
        {"action": RecoveryAction.RETRY_WITH_REDUCED_SCOPE, "parameters": {"reduce_memory": True, "reduce_threads": True}, "max_attempts": 2, "backoff_multiplier": 1.0, "success_probability": 0.7, "estimated_time": 60},
        {"action": RecoveryAction.RETRY_WITH_BACKOFF, "parameters": {"initial_delay": 60, "max_delay": 300}, "max_attempts": 2, "backoff_multiplier": 2.0, "success_probability": 0.5, "estimated_time": 180}
    ],
    ErrorType.AUTHENTICATION_FAILED: [
        {"action": RecoveryAction.ESCALATE_TO_HUMAN, "parameters": {"message": "Authentication credentials required", "urgency": "high"}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.9, "estimated_time": 300},
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"no_auth_required": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.4, "estimated_time": 30}
    ],
    ErrorType.TARGET_UNREACHABLE: [
        {"action": RecoveryAction.RETRY_WITH_BACKOFF, "parameters": {"initial_delay": 15, "max_delay": 180}, "max_attempts": 3, "backoff_multiplier": 2.0, "success_probability": 0.6, "estimated_time": 90},
        {"action": RecoveryAction.GRACEFUL_DEGRADATION, "parameters": {"skip_target": True, "continue_with_others": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 1.0, "estimated_time": 5}
    ],
    ErrorType.PARSING_ERROR: [
        {"action": RecoveryAction.ADJUST_PARAMETERS, "parameters": {"change_output_format": True, "add_parsing_flags": True}, "max_attempts": 2, "backoff_multiplier": 1.0, "success_probability": 0.7, "estimated_time": 20},
        {"action": RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, "parameters": {"better_output_format": True}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.6, "estimated_time": 30}
    ],
    ErrorType.UNKNOWN: [
        {"action": RecoveryAction.RETRY_WITH_BACKOFF, "parameters": {"initial_delay": 5, "max_delay": 30}, "max_attempts": 2, "backoff_multiplier": 2.0, "success_probability": 0.3, "estimated_time": 45},
        {"action": RecoveryAction.ESCALATE_TO_HUMAN, "parameters": {"message": "Unknown error encountered", "urgency": "medium"}, "max_attempts": 1, "backoff_multiplier": 1.0, "success_probability": 0.9, "estimated_time": 300}
    ]
}

TOOL_ALTERNATIVES: Dict[str, List[str]] = {
    "nmap": ["rustscan", "masscan", "zmap"],
    "rustscan": ["nmap", "masscan"],
    "masscan": ["nmap", "rustscan", "zmap"],
    "gobuster": ["feroxbuster", "dirsearch", "ffuf", "dirb"],
    "feroxbuster": ["gobuster", "dirsearch", "ffuf"],
    "dirsearch": ["gobuster", "feroxbuster", "ffuf"],
    "ffuf": ["gobuster", "feroxbuster", "dirsearch"],
    "nuclei": ["jaeles", "nikto", "w3af"],
    "jaeles": ["nuclei", "nikto"],
    "nikto": ["nuclei", "jaeles", "w3af"],
    "katana": ["gau", "waybackurls", "hakrawler"],
    "gau": ["katana", "waybackurls", "hakrawler"],
    "waybackurls": ["gau", "katana", "hakrawler"],
    "arjun": ["paramspider", "x8", "ffuf"],
    "paramspider": ["arjun", "x8"],
    "x8": ["arjun", "paramspider"],
    "sqlmap": ["sqlninja", "jsql-injection"],
    "dalfox": ["xsser", "xsstrike"],
    "subfinder": ["amass", "assetfinder", "findomain"],
    "amass": ["subfinder", "assetfinder", "findomain"],
    "assetfinder": ["subfinder", "amass", "findomain"],
    "prowler": ["scout-suite", "cloudmapper"],
    "scout-suite": ["prowler", "cloudmapper"],
    "trivy": ["clair", "docker-bench-security"],
    "clair": ["trivy", "docker-bench-security"],
    "ghidra": ["radare2", "ida", "binary-ninja"],
    "radare2": ["ghidra", "objdump", "gdb"],
    "gdb": ["radare2", "lldb"],
    "pwntools": ["ropper", "ropgadget"],
    "ropper": ["ropgadget", "pwntools"],
    "ropgadget": ["ropper", "pwntools"]
}

PARAMETER_ADJUSTMENTS: Dict[str, Dict[ErrorType, Dict[str, Any]]] = {
    "nmap": {
        ErrorType.TIMEOUT: {"timing": "-T2", "reduce_ports": True},
        ErrorType.RATE_LIMITED: {"timing": "-T1", "delay": "1000ms"},
        ErrorType.RESOURCE_EXHAUSTED: {"max_parallelism": "10"}
    },
    "gobuster": {
        ErrorType.TIMEOUT: {"threads": "10", "timeout": "30s"},
        ErrorType.RATE_LIMITED: {"threads": "5", "delay": "1s"},
        ErrorType.RESOURCE_EXHAUSTED: {"threads": "5"}
    },
    "nuclei": {
        ErrorType.TIMEOUT: {"concurrency": "10", "timeout": "30"},
        ErrorType.RATE_LIMITED: {"rate-limit": "10", "concurrency": "5"},
        ErrorType.RESOURCE_EXHAUSTED: {"concurrency": "5"}
    },
    "feroxbuster": {
        ErrorType.TIMEOUT: {"threads": "10", "timeout": "30"},
        ErrorType.RATE_LIMITED: {"threads": "5", "rate-limit": "10"},
        ErrorType.RESOURCE_EXHAUSTED: {"threads": "5"}
    },
    "ffuf": {
        ErrorType.TIMEOUT: {"threads": "10", "timeout": "30"},
        ErrorType.RATE_LIMITED: {"threads": "5", "rate": "10"},
        ErrorType.RESOURCE_EXHAUSTED: {"threads": "5"}
    }
}
