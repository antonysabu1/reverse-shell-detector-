from config import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM

SIGNATURES = {
    # Classic reverse shells
    "Bash TCP":          b"bash -i",
    "Bash TCP (Dev)":    b"/dev/tcp/",
    "Netcat Execute":    b"nc -e",
    "Netcat -c flag":    b"nc -c",
    "Python Socket":     b"import socket",
    "PHP Socket":        b"fsockopen",
    "Perl Socket":       b"use Socket",
    "Ruby Socket":       b"TCPSocket",
    "PowerShell":        b"powershell -nop",
    # SSL / Socat shells
    "Socat SSL":         b"socat openssl",
    "Socat EXEC":        b"EXEC:/bin/bash",
    # DNS C2
    "DNS C2 Payload":    b"Hello-from-DNS-C2",
    "DNS TXT Query":     b"cmd.c2.",
    # HTTP reverse shell beacon
    "HTTP Shell Beacon": b"X-Shell-Token",
    # Encoded payloads
    "Base64 Encoded":    b"bash -i >& /dev/tcp",
}

# Port-based confidence boost table
SUSPICIOUS_PORTS = {
    4444: ("Common Metasploit port", CONFIDENCE_HIGH),
    1337: ("Common leet shell port", CONFIDENCE_MEDIUM),
    5555: ("Common reverse shell port", CONFIDENCE_MEDIUM),
    6666: ("Common reverse shell port", CONFIDENCE_MEDIUM),
    7777: ("Common reverse shell port", CONFIDENCE_MEDIUM),
    8888: ("Common reverse shell port", CONFIDENCE_MEDIUM),
    9001: ("Common reverse shell port", CONFIDENCE_MEDIUM),
    9999: ("Common reverse shell port", CONFIDENCE_MEDIUM),
    443:  ("HTTPS camouflage shell", CONFIDENCE_MEDIUM),
    80:   ("HTTP camouflage shell", CONFIDENCE_MEDIUM),
}

def analyze(payload, dst_port):
    """
    Checks the raw payload against known reverse shell command signatures
    and port-based threat intelligence.
    """
    matches = []
    for shell_type, sig in SIGNATURES.items():
        if sig in payload:
            matches.append({
                "type": f"{shell_type} Signature Match",
                "confidence": CONFIDENCE_HIGH,
                "reason": f"Matched signature '{sig.decode(errors='ignore')}'"
            })
    return matches
