from typing import Dict, List, Any

ATTACK_PATTERNS: Dict[str, List[Dict[str, Any]]] = {
    "web_reconnaissance": [
        {"tool": "nmap", "priority": 1, "params": {"scan_type": "-sV -sC", "ports": "80,443,8080,8443"}},
        {"tool": "httpx", "priority": 2, "params": {"probe": True, "tech_detect": True}},
        {"tool": "katana", "priority": 3, "params": {"depth": 3, "js_crawl": True}},
        {"tool": "gau", "priority": 4, "params": {"include_subs": True}},
        {"tool": "waybackurls", "priority": 5, "params": {"get_versions": False}},
        {"tool": "nuclei", "priority": 6, "params": {"severity": "critical,high", "tags": "tech"}},
        {"tool": "dirsearch", "priority": 7, "params": {"extensions": "php,html,js,txt", "threads": 30}},
        {"tool": "gobuster", "priority": 8, "params": {"mode": "dir", "extensions": "php,html,js,txt"}}
    ],
    "api_testing": [
        {"tool": "httpx", "priority": 1, "params": {"probe": True, "tech_detect": True}},
        {"tool": "arjun", "priority": 2, "params": {"method": "GET,POST", "stable": True}},
        {"tool": "x8", "priority": 3, "params": {"method": "GET", "wordlist": "/usr/share/wordlists/x8/params.txt"}},
        {"tool": "paramspider", "priority": 4, "params": {"level": 2}},
        {"tool": "nuclei", "priority": 5, "params": {"tags": "api,graphql,jwt", "severity": "high,critical"}},
        {"tool": "ffuf", "priority": 6, "params": {"mode": "parameter", "method": "POST"}}
    ],
    "network_discovery": [
        {"tool": "arp-scan", "priority": 1, "params": {"local_network": True}},
        {"tool": "rustscan", "priority": 2, "params": {"ulimit": 5000, "scripts": True}},
        {"tool": "nmap-advanced", "priority": 3, "params": {"scan_type": "-sS", "os_detection": True, "version_detection": True}},
        {"tool": "masscan", "priority": 4, "params": {"rate": 1000, "ports": "1-65535", "banners": True}},
        {"tool": "enum4linux-ng", "priority": 5, "params": {"shares": True, "users": True, "groups": True}},
        {"tool": "nbtscan", "priority": 6, "params": {"verbose": True}},
        {"tool": "smbmap", "priority": 7, "params": {"recursive": True}},
        {"tool": "rpcclient", "priority": 8, "params": {"commands": "enumdomusers;enumdomgroups;querydominfo"}}
    ],
    "vulnerability_assessment": [
        {"tool": "nuclei", "priority": 1, "params": {"severity": "critical,high,medium", "update": True}},
        {"tool": "jaeles", "priority": 2, "params": {"threads": 20, "timeout": 20}},
        {"tool": "dalfox", "priority": 3, "params": {"mining_dom": True, "mining_dict": True}},
        {"tool": "nikto", "priority": 4, "params": {"comprehensive": True}},
        {"tool": "sqlmap", "priority": 5, "params": {"crawl": 2, "batch": True}}
    ],
    "comprehensive_network_pentest": [
        {"tool": "autorecon", "priority": 1, "params": {"port_scans": "top-1000-ports", "service_scans": "default"}},
        {"tool": "rustscan", "priority": 2, "params": {"ulimit": 5000, "scripts": True}},
        {"tool": "nmap-advanced", "priority": 3, "params": {"aggressive": True, "nse_scripts": "vuln,exploit"}},
        {"tool": "enum4linux-ng", "priority": 4, "params": {"shares": True, "users": True, "groups": True, "policy": True}},
        {"tool": "responder", "priority": 5, "params": {"wpad": True, "duration": 180}}
    ],
    "binary_exploitation": [
        {"tool": "checksec", "priority": 1, "params": {}},
        {"tool": "ghidra", "priority": 2, "params": {"analysis_timeout": 300, "output_format": "xml"}},
        {"tool": "ropper", "priority": 3, "params": {"gadget_type": "rop", "quality": 2}},
        {"tool": "one-gadget", "priority": 4, "params": {"level": 1}},
        {"tool": "pwntools", "priority": 5, "params": {"exploit_type": "local"}},
        {"tool": "gdb-peda", "priority": 6, "params": {"commands": "checksec\ninfo functions\nquit"}}
    ],
    "ctf_pwn_challenge": [
        {"tool": "pwninit", "priority": 1, "params": {"template_type": "python"}},
        {"tool": "checksec", "priority": 2, "params": {}},
        {"tool": "ghidra", "priority": 3, "params": {"analysis_timeout": 180}},
        {"tool": "ropper", "priority": 4, "params": {"gadget_type": "all", "quality": 3}},
        {"tool": "angr", "priority": 5, "params": {"analysis_type": "symbolic"}},
        {"tool": "one-gadget", "priority": 6, "params": {"level": 2}}
    ],
    "aws_security_assessment": [
        {"tool": "prowler", "priority": 1, "params": {"provider": "aws", "output_format": "json"}},
        {"tool": "scout-suite", "priority": 2, "params": {"provider": "aws"}},
        {"tool": "cloudmapper", "priority": 3, "params": {"action": "collect"}},
        {"tool": "pacu", "priority": 4, "params": {"modules": "iam__enum_users_roles_policies_groups"}}
    ],
    "kubernetes_security_assessment": [
        {"tool": "kube-bench", "priority": 1, "params": {"output_format": "json"}},
        {"tool": "kube-hunter", "priority": 2, "params": {"report": "json"}},
        {"tool": "falco", "priority": 3, "params": {"duration": 120, "output_format": "json"}}
    ],
    "container_security_assessment": [
        {"tool": "trivy", "priority": 1, "params": {"scan_type": "image", "severity": "HIGH,CRITICAL"}},
        {"tool": "clair", "priority": 2, "params": {"output_format": "json"}},
        {"tool": "docker-bench-security", "priority": 3, "params": {}}
    ],
    "iac_security_assessment": [
        {"tool": "checkov", "priority": 1, "params": {"output_format": "json"}},
        {"tool": "terrascan", "priority": 2, "params": {"scan_type": "all", "output_format": "json"}},
        {"tool": "trivy", "priority": 3, "params": {"scan_type": "config", "severity": "HIGH,CRITICAL"}}
    ],
    "multi_cloud_assessment": [
        {"tool": "scout-suite", "priority": 1, "params": {"provider": "aws"}},
        {"tool": "prowler", "priority": 2, "params": {"provider": "aws"}},
        {"tool": "checkov", "priority": 3, "params": {"framework": "terraform"}},
        {"tool": "terrascan", "priority": 4, "params": {"scan_type": "all"}}
    ],
    "bug_bounty_reconnaissance": [
        {"tool": "amass", "priority": 1, "params": {"mode": "enum", "passive": False}},
        {"tool": "subfinder", "priority": 2, "params": {"silent": True, "all_sources": True}},
        {"tool": "httpx", "priority": 3, "params": {"probe": True, "tech_detect": True, "status_code": True}},
        {"tool": "katana", "priority": 4, "params": {"depth": 3, "js_crawl": True, "form_extraction": True}},
        {"tool": "gau", "priority": 5, "params": {"include_subs": True}},
        {"tool": "waybackurls", "priority": 6, "params": {"get_versions": False}},
        {"tool": "paramspider", "priority": 7, "params": {"level": 2}},
        {"tool": "arjun", "priority": 8, "params": {"method": "GET,POST", "stable": True}}
    ],
    "bug_bounty_vulnerability_hunting": [
        {"tool": "nuclei", "priority": 1, "params": {"severity": "critical,high", "tags": "rce,sqli,xss,ssrf"}},
        {"tool": "dalfox", "priority": 2, "params": {"mining_dom": True, "mining_dict": True}},
        {"tool": "sqlmap", "priority": 3, "params": {"batch": True, "level": 2, "risk": 2}},
        {"tool": "jaeles", "priority": 4, "params": {"threads": 20, "timeout": 20}},
        {"tool": "ffuf", "priority": 5, "params": {"match_codes": "200,204,301,302,307,401,403", "threads": 40}}
    ],
    "bug_bounty_high_impact": [
        {"tool": "nuclei", "priority": 1, "params": {"severity": "critical", "tags": "rce,sqli,ssrf,lfi,xxe"}},
        {"tool": "sqlmap", "priority": 2, "params": {"batch": True, "level": 3, "risk": 3, "tamper": "space2comment"}},
        {"tool": "jaeles", "priority": 3, "params": {"signatures": "rce,sqli,ssrf", "threads": 30}},
        {"tool": "dalfox", "priority": 4, "params": {"blind": True, "mining_dom": True, "custom_payload": "alert(document.domain)"}}
    ]
}
