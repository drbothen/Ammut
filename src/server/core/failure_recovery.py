TOOL_ALTERNATIVES = {
    "nmap": ["rustscan", "masscan", "zmap"],
    "gobuster": ["dirsearch", "feroxbuster", "dirb"],
    "sqlmap": ["sqlninja", "bbqsql", "jsql-injection"],
    "nuclei": ["nikto", "w3af", "skipfish"],
    "hydra": ["medusa", "ncrack", "patator"],
    "hashcat": ["john", "ophcrack", "rainbowcrack"],
    "amass": ["subfinder", "sublist3r", "assetfinder"],
    "ffuf": ["wfuzz", "gobuster", "dirb"]
}

FAILURE_PATTERNS = {
    "timeout": ["timeout", "timed out", "connection timeout"],
    "permission_denied": ["permission denied", "access denied", "forbidden"],
    "not_found": ["not found", "command not found", "no such file"],
    "network_error": ["network unreachable", "connection refused", "host unreachable"],
    "rate_limited": ["rate limit", "too many requests", "throttled"],
    "authentication_required": ["authentication required", "unauthorized", "login required"]
}
