from typing import List, Dict, Any

from src.server.services.base import ToolManagerServiceBase


class ToolManagerService(ToolManagerServiceBase):
    """Concrete implementation of the tool manager service."""

    def __init__(self):
        self.tool_commands: Dict[str, str] = {
            # Web Reconnaissance & Analysis
            "nmap": "nmap -sV -sC -T4",
            "gobuster": "gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "nikto": "nikto -h {target}",
            "whatweb": "whatweb -v",
            "wpscan": "wpscan --url {target} --enumerate p,t,u --api-token YOUR_API_TOKEN",
            "sublist3r": "sublist3r -d {target}",
            "amass": "amass enum -d {target}",
            "feroxbuster": "feroxbuster -u {target} -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt",
            "dirsearch": "dirsearch -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "katana": "katana -u {target}",

            # Web Vulnerability Scanning
            "sqlmap": "sqlmap -u {target} --batch --level=5 --risk=3",
            "dalfox": "dalfox url {target}",
            "arjun": "arjun -u {target}",
            "paramspider": "paramspider -d {target}",
            "jwt-tool": "jwt-tool {target}",
            "graphql-voyager": "graphql-voyager {target}",

            # Cryptography & Hashing
            "hashcat": "hashcat -m 0 -a 0 {target}",
            "john": "john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt {target}",
            "hash-identifier": "hash-identifier {target}",
            "rsatool": "rsatool -f {target}",
            "factordb": "factordb {target}",
            "yafu": "yafu-x64 {target}",
            "cipher-identifier": "cipher-identifier -t '{target}'",
            "frequency-analysis": "freq.py {target}",
            "vigenere-solver": "vigenere-solver -i {target}",
            "gpg": "gpg --decrypt {target}",

            # Binary Exploitation (Pwn)
            "gdb-peda": "gdb -q {target}",
            "gdb-gef": "gdb -q {target}",
            "pwntools": "python -c 'from pwn import *; ...'",
            "ropper": "ropper --file {target}",
            "ropgadget": "ROPgadget --binary {target}",
            "checksec": "checksec --file={target}",
            "one-gadget": "one-gadget {target}",

            # Forensics
            "exiftool": "exiftool {target}",
            "steghide": "steghide extract -sf {target}",
            "stegsolve": "stegsolve.jar {target}",
            "zsteg": "zsteg {target}",
            "binwalk": "binwalk -e {target}",
            "foremost": "foremost -i {target}",
            "photorec": "photorec /d {target}",
            "volatility": "volatility -f {target} imageinfo",
            "volatility3": "python3 vol.py -f {target} windows.info.Info",
            "wireshark": "wireshark -r {target}",
            "tcpdump": "tcpdump -r {target}",
            "testdisk": "testdisk {target}",
            "sleuthkit": "fls {target}",
            "audacity": "audacity {target}",
            "sonic-visualizer": "sonic-visualizer {target}",

            # Reverse Engineering
            "ghidra": "ghidraRun {target}",
            "ida": "idaq64 {target}",
            "radare2": "r2 -d {target}",
            "strings": "strings -a {target}",
            "ltrace": "ltrace ./{target}",
            "strace": "strace ./{target}",
            "upx": "upx -d {target}",
            "peid": "peid {target}",
            "detect-it-easy": "die {target}",
            "apktool": "apktool d {target}",
            "jadx": "jadx-gui {target}",
            "dex2jar": "d2j-dex2jar.sh {target}",
            "dnspy": "dnSpy.exe {target}",
            "ilspy": "ILSpy.exe {target}",
            "jd-gui": "jd-gui {target}",
            "x64dbg": "x64dbg.exe {target}",
            "objdump": "objdump -d {target}",

            # OSINT
            "sherlock": "sherlock {target}",
            "social-analyzer": "social-analyzer --username {target}",
            "theHarvester": "theHarvester -d {target} -b all",
            "whois": "whois {target}",
            "dig": "dig {target}",

            # Misc
            "base64": "base64 -d",
            "base32": "base32 -d",
            "hex": "xxd -r -p",
            "rot13": "tr 'A-Za-z' 'N-ZA-Mn-za-m'",
            "zip": "unzip {target}",
            "7zip": "7z x {target}",
            "rar": "unrar x {target}",
            "tar": "tar -xf {target}",
            "brainfuck": "bf {target}",
            "whitespace": "wsrun {target}",
            "piet": "npiet {target}",
            "malbolge": "malbolge {target}",
            "qr-decoder": "zbarimg {target}"
        }

        self.tool_categories: Dict[str, List[str]] = {
            "web_recon": ["nmap", "gobuster", "nikto", "whatweb", "wpscan", "sublist3r", "amass", "feroxbuster", "dirsearch", "katana"],
            "web_vuln": ["sqlmap", "dalfox", "arjun", "paramspider", "jwt-tool", "graphql-voyager"],
            "crypto_hash": ["hashcat", "john", "hash-identifier"],
            "crypto_asymmetric": ["rsatool", "factordb", "yafu"],
            "crypto_cipher": ["cipher-identifier", "frequency-analysis", "vigenere-solver"],
            "crypto_stego": ["exiftool", "steghide", "stegsolve", "zsteg"],
            "pwn_analysis": ["checksec", "file", "strings", "gdb-peda", "gdb-gef"],
            "pwn_exploit": ["pwntools", "ropper", "ropgadget", "one-gadget"],
            "forensics_disk": ["testdisk", "sleuthkit", "photorec", "foremost"],
            "forensics_memory": ["volatility", "volatility3"],
            "forensics_network": ["wireshark", "tcpdump"],
            "forensics_file": ["exiftool", "binwalk", "strings"],
            "rev_static": ["ghidra", "ida", "radare2", "strings"],
            "rev_dynamic": ["gdb-peda", "ltrace", "strace"],
            "rev_unpack": ["upx", "peid", "detect-it-easy"],
            "osint_social": ["sherlock", "social-analyzer", "theHarvester"],
            "osint_domain": ["whois", "dig", "sublist3r", "amass"],
            "osint_search": ["shodan", "censys", "recon-ng"],
            "misc_encoding": ["base64", "base32", "hex", "rot13"],
            "misc_compression": ["zip", "7zip", "rar", "tar"],
            "misc_esoteric": ["brainfuck", "whitespace", "piet", "malbolge"]
        }

    def get_tool_command(self, tool: str, target: str, additional_args: str = "") -> str:
        """Get optimized command for CTF tool with intelligent parameter selection"""
        base_command = self.tool_commands.get(tool, tool)

        if tool in ["hashcat", "john"]:
            if "wordlist" not in base_command:
                base_command += " --wordlist=/usr/share/wordlists/rockyou.txt"
            if tool == "hashcat" and "--rules" not in base_command:
                base_command += " --rules-file=/usr/share/hashcat/rules/best64.rule"

        elif tool in ["sqlmap"]:
            if "--tamper" not in base_command:
                base_command += " --tamper=space2comment,charencode,randomcase"
            if "--threads" not in base_command:
                base_command += " --threads=5"

        elif tool in ["gobuster", "dirsearch", "feroxbuster"]:
            if tool == "gobuster" and "-t" not in base_command:
                base_command += " -t 50"
            elif tool == "dirsearch" and "-t" not in base_command:
                base_command += " -t 50"
            elif tool == "feroxbuster" and "-t" not in base_command:
                base_command += " -t 50"

        if additional_args:
            return f"{base_command} {additional_args} {target}"
        else:
            return f"{base_command} {target}"

    def get_category_tools(self, category: str) -> List[str]:
        """Get all tools for a specific category"""
        return self.tool_categories.get(category, [])

    def suggest_tools_for_challenge(self, challenge_description: str, category: str) -> List[str]:
        """Suggest optimal tools based on challenge description and category"""
        suggested_tools = []
        description_lower = challenge_description.lower()

        if category == "web":
            suggested_tools.extend(self.tool_categories["web_recon"][:2])
            if any(keyword in description_lower for keyword in ["sql", "injection", "database", "mysql", "postgres"]):
                suggested_tools.extend(["sqlmap", "hash-identifier"])
            if any(keyword in description_lower for keyword in ["xss", "script", "javascript", "dom"]):
                suggested_tools.extend(["dalfox", "katana"])
            if any(keyword in description_lower for keyword in ["wordpress", "wp", "cms"]):
                suggested_tools.append("wpscan")
            if any(keyword in description_lower for keyword in ["directory", "hidden", "files", "admin"]):
                suggested_tools.extend(["gobuster", "dirsearch"])
            if any(keyword in description_lower for keyword in ["parameter", "param", "get", "post"]):
                suggested_tools.extend(["arjun", "paramspider"])
            if any(keyword in description_lower for keyword in ["jwt", "token", "session"]):
                suggested_tools.append("jwt-tool")
            if any(keyword in description_lower for keyword in ["graphql", "api"]):
                suggested_tools.append("graphql-voyager")

        elif category == "crypto":
            if any(keyword in description_lower for keyword in ["hash", "md5", "sha", "password"]):
                suggested_tools.extend(["hashcat", "john", "hash-identifier"])
            if any(keyword in description_lower for keyword in ["rsa", "public key", "private key", "factorization"]):
                suggested_tools.extend(["rsatool", "factordb", "yafu"])
            if any(keyword in description_lower for keyword in ["cipher", "encrypt", "decrypt", "substitution"]):
                suggested_tools.extend(["cipher-identifier", "frequency-analysis"])
            if any(keyword in description_lower for keyword in ["vigenere", "polyalphabetic"]):
                suggested_tools.append("vigenere-solver")
            if any(keyword in description_lower for keyword in ["base64", "base32", "encoding"]):
                suggested_tools.extend(["base64", "base32"])
            if any(keyword in description_lower for keyword in ["rot", "caesar", "shift"]):
                suggested_tools.append("rot13")
            if any(keyword in description_lower for keyword in ["pgp", "gpg", "signature"]):
                suggested_tools.append("gpg")

        elif category == "pwn":
            suggested_tools.extend(["checksec", "file", "strings"])
            if any(keyword in description_lower for keyword in ["buffer", "overflow", "bof"]):
                suggested_tools.extend(["pwntools", "gdb-peda", "ropper"])
            if any(keyword in description_lower for keyword in ["format", "printf", "string"]):
                suggested_tools.extend(["pwntools", "gdb-peda"])
            if any(keyword in description_lower for keyword in ["heap", "malloc", "free"]):
                suggested_tools.extend(["pwntools", "gdb-gef"])
            if any(keyword in description_lower for keyword in ["rop", "gadget", "chain"]):
                suggested_tools.extend(["ropper", "ropgadget"])
            if any(keyword in description_lower for keyword in ["shellcode", "exploit"]):
                suggested_tools.extend(["pwntools", "one-gadget"])
            if any(keyword in description_lower for keyword in ["canary", "stack", "protection"]):
                suggested_tools.extend(["checksec", "pwntools"])

        elif category == "forensics":
            if any(keyword in description_lower for keyword in ["image", "jpg", "png", "gif", "steganography"]):
                suggested_tools.extend(["exiftool", "steghide", "stegsolve", "zsteg"])
            if any(keyword in description_lower for keyword in ["memory", "dump", "ram"]):
                suggested_tools.extend(["volatility", "volatility3"])
            if any(keyword in description_lower for keyword in ["network", "pcap", "wireshark", "traffic"]):
                suggested_tools.extend(["wireshark", "tcpdump"])
            if any(keyword in description_lower for keyword in ["file", "deleted", "recovery", "carving"]):
                suggested_tools.extend(["binwalk", "foremost", "photorec"])
            if any(keyword in description_lower for keyword in ["disk", "filesystem", "partition"]):
                suggested_tools.extend(["testdisk", "sleuthkit"])
            if any(keyword in description_lower for keyword in ["audio", "wav", "mp3", "sound"]):
                suggested_tools.extend(["audacity", "sonic-visualizer"])

        elif category == "rev":
            suggested_tools.extend(["file", "strings", "objdump"])
            if any(keyword in description_lower for keyword in ["packed", "upx", "packer"]):
                suggested_tools.extend(["upx", "peid", "detect-it-easy"])
            if any(keyword in description_lower for keyword in ["android", "apk", "mobile"]):
                suggested_tools.extend(["apktool", "jadx", "dex2jar"])
            if any(keyword in description_lower for keyword in [".net", "dotnet", "csharp"]):
                suggested_tools.extend(["dnspy", "ilspy"])
            if any(keyword in description_lower for keyword in ["java", "jar", "class"]):
                suggested_tools.extend(["jd-gui", "jadx"])
            if any(keyword in description_lower for keyword in ["windows", "exe", "dll"]):
                suggested_tools.extend(["ghidra", "ida", "x64dbg"])
            if any(keyword in description_lower for keyword in ["linux", "elf", "binary"]):
                suggested_tools.extend(["ghidra", "radare2", "gdb-peda"])

        elif category == "osint":
            if any(keyword in description_lower for keyword in ["username", "social", "media"]):
                suggested_tools.extend(["sherlock", "social-analyzer"])
            if any(keyword in description_lower for keyword in ["domain", "subdomain", "dns"]):
                suggested_tools.extend(["sublist3r", "amass", "dig"])
            if any(keyword in description_lower for keyword in ["email", "harvest", "contact"]):
                suggested_tools.append("theHarvester")
            if any(keyword in description_lower for keyword in ["ip", "port", "service"]):
                suggested_tools.extend(["shodan", "censys"])
            if any(keyword in description_lower for keyword in ["whois", "registration", "owner"]):
                suggested_tools.append("whois")

        elif category == "misc":
            if any(keyword in description_lower for keyword in ["qr", "barcode", "code"]):
                suggested_tools.append("qr-decoder")
            if any(keyword in description_lower for keyword in ["zip", "archive", "compressed"]):
                suggested_tools.extend(["zip", "7zip", "rar"])
            if any(keyword in description_lower for keyword in ["brainfuck", "bf", "esoteric"]):
                suggested_tools.append("brainfuck")
            if any(keyword in description_lower for keyword in ["whitespace", "ws"]):
                suggested_tools.append("whitespace")
            if any(keyword in description_lower for keyword in ["piet", "image", "program"]):
                suggested_tools.append("piet")

        return list(dict.fromkeys(suggested_tools))
