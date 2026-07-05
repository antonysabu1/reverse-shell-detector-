import re
from config import CONFIDENCE_LOW, CONFIDENCE_MEDIUM, CONFIDENCE_HIGH

# Prompts: e.g., root@victim:/# or antony@host:~$ or sh-5.1$
PROMPT_PATTERNS = [
    re.compile(br'^(?:[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+[:~].*[$#]\s*)$', re.MULTILINE),
    re.compile(br'^\s*(?:sh-[0-9\.]+[#$]\s*)$', re.MULTILINE),
    re.compile(br'^\s*(?:bash-[0-9\.]+[#$]\s*)$', re.MULTILINE),
]

ERROR_PATTERNS = [
    re.compile(br'(?:command not found|Permission denied|No such file or directory)', re.IGNORECASE)
]

# DNS C2 patterns — base32/hex-encoded subdomains used for data exfil
DNS_C2_PATTERNS = [
    re.compile(br'[a-zA-Z0-9]{20,}\.[a-z]{2,}\.?$'),  # Long random subdomain
]

# HTTP shell beacon headers
HTTP_SHELL_PATTERNS = [
    re.compile(br'X-Shell-Token:', re.IGNORECASE),
    re.compile(br'GET /shell\?cmd=', re.IGNORECASE),
    re.compile(br'POST /cmd ', re.IGNORECASE),
]

COMMON_SHELL_PORTS = {4444, 4445, 1337, 5555, 6666, 7777, 8888, 9001, 9999}
HTTP_PORTS = {80, 8080, 8000, 8443}
DNS_PORT = 53

def analyze(payload, dst_port):
    """
    Analyzes packet payload and destination port for heuristic indicators of a shell session.
    """
    matches = []

    # 1. Shell Prompt Heuristic
    for pattern in PROMPT_PATTERNS:
        if pattern.search(payload):
            matches.append({
                "type": "Heuristic Interactive Prompt",
                "confidence": CONFIDENCE_HIGH,
                "reason": "Detected shell interactive prompt pattern in packet stream"
            })
            break

    # 2. Command Error Heuristic
    for pattern in ERROR_PATTERNS:
        if pattern.search(payload):
            matches.append({
                "type": "Heuristic Shell Error",
                "confidence": CONFIDENCE_MEDIUM,
                "reason": "Detected shell command execution error message"
            })
            break

    # 3. Port Profiling Heuristic
    if dst_port in COMMON_SHELL_PORTS:
        matches.append({
            "type": "Heuristic Suspicious Port",
            "confidence": CONFIDENCE_MEDIUM,
            "reason": f"Outbound TCP connection to common reverse shell port: {dst_port}"
        })

    # 4. HTTP reverse shell beacon heuristic
    for pattern in HTTP_SHELL_PATTERNS:
        if pattern.search(payload):
            matches.append({
                "type": "Heuristic HTTP Shell Beacon",
                "confidence": CONFIDENCE_HIGH,
                "reason": f"Detected HTTP-based shell command/beacon header on port {dst_port}"
            })
            break

    # 5. Long payload on HTTP port (potential HTTP shell exfil)
    if dst_port in HTTP_PORTS and len(payload) > 200:
        matches.append({
            "type": "Heuristic HTTP Large Payload",
            "confidence": CONFIDENCE_LOW,
            "reason": f"Unusually large HTTP payload ({len(payload)} bytes) — possible shell output exfiltration"
        })

    return matches
