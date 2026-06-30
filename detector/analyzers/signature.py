from config import CONFIDENCE_HIGH

SIGNATURES = {
    "Bash TCP": b"bash -i",
    "Bash TCP (Dev)": b"/dev/tcp/",
    "Netcat Execute": b"nc -e",
    "Python Socket": b"import socket",
    "PHP Socket": b"fsockopen"
}

def analyze(payload, dst_port):
    """
    Checks the raw payload against known reverse shell command signatures.
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
