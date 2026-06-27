import os
import sys
from scapy.all import sniff, IP, TCP, Raw
import models

# Common reverse shell payload signatures
SIGNATURES = {
    "Bash TCP": b"bash -i",
    "Bash TCP (Dev)": b"/dev/tcp/",
    "Netcat Execute": b"nc -e",
    "Python Socket": b"import socket",
    "PHP Socket": b"fsockopen"
}

def analyze_packet(packet):
    # Only inspect TCP packets with a raw payload
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        
        # Check against known signatures
        for shell_type, sig in SIGNATURES.items():
            if sig in payload:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                dst_port = packet[TCP].dport
                
                print(f"=====================================================")
                print(f"🚨 ALERT: Reverse Shell Detected!")
                print(f"🛡️  Type: {shell_type}")
                print(f"📡 Connection: {src_ip} -> {dst_ip}:{dst_port}")
                print(f"📦 Payload snippet: {payload[:50]}...")
                print(f"=====================================================")
                
                # Save to database
                models.save_alert(shell_type, src_ip, dst_ip, dst_port, payload)

def main():
    print("[*] Starting ShellSnare Detection Engine...")
    models.init_db()
    print("[*] Sniffing for reverse shell traffic...")
    
    # Sniff TCP traffic, don't store in memory, pass to analyze_packet
    sniff(filter="tcp", prn=analyze_packet, store=False)

if __name__ == "__main__":
    main()
