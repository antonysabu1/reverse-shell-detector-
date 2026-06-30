import math
from config import ENTROPY_THRESHOLD, CONFIDENCE_MEDIUM

def calculate_entropy(data):
    """
    Computes Shannon Entropy of a byte string.
    Returns value between 0.0 (no variance) and 8.0 (completely random/maximum entropy).
    """
    if not data:
        return 0.0
    
    length = len(data)
    counts = {}
    for b in data:
        counts[b] = counts.get(b, 0) + 1
        
    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
        
    return entropy

def analyze(payload, dst_port):
    """
    Analyzes payload size and entropy for statistical anomalies.
    """
    matches = []
    
    # We only compute entropy for sufficiently large payloads to avoid noise
    if len(payload) >= 32:
        entropy = calculate_entropy(payload)
        if entropy >= ENTROPY_THRESHOLD:
            matches.append({
                "type": "Statistical High Entropy",
                "confidence": CONFIDENCE_MEDIUM,
                "reason": f"High Shannon entropy ({entropy:.2f} >= {ENTROPY_THRESHOLD}) indicating encryption or encoding"
            })
            
    return matches
