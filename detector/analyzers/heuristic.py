import re
from config import CONFIDENCE_MEDIUM, CONFIDENCE_HIGH

# Prompts: e.g., root@victim:/# or antony@host:~$ or sh-5.1$
PROMPT_PATTERNS = [
    re.compile(br'^(?:[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+[:~].*[$#]\s*)$', re.MULTILINE),
    re.compile(br'^\s*(?:sh-[0-9\.]+[#$]\s*)$', re.MULTILINE),
    re.compile(br'^\s*(?:bash-[0-9\.]+[#$]\s*)$', re.MULTILINE),
]

ERROR_PATTERNS = [
    re.compile(br'(?:command not found|Permission denied|No such file or directory)', re.IGNORECASE)
]

COMMON_SHELL_PORTS = {4444, 4445, 1337, 5555, 6666, 7777, 8888, 9999}

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

    return matches
