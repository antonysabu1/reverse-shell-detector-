import os
import sys
from scapy.all import sniff, IP, TCP, Raw
import models
import ips
from analyzers import signature, heuristic, statistical

def analyze_packet(packet):
    # Only inspect TCP packets with a raw payload
    if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        dst_port = packet[TCP].dport
        
        # Run all analyzers
        sig_matches = signature.analyze(payload, dst_port)
        heu_matches = heuristic.analyze(payload, dst_port)
        stat_matches = statistical.analyze(payload, dst_port)
        
        all_matches = sig_matches + heu_matches + stat_matches
        
        if all_matches:
            # Aggregate matches: sort by confidence descending
            all_matches.sort(key=lambda x: x["confidence"], reverse=True)
            best_match = all_matches[0]
            
            shell_type = best_match["type"]
            confidence = best_match["confidence"]
            reason = "; ".join(list(set(m["reason"] for m in all_matches)))
            
            action_taken = "Detected"
            
            # IPS Action: If confidence is high, inject RST packets
            if confidence >= 0.85:
                if ips.inject_rst(packet):
                    action_taken = "Blocked (TCP RST)"
            
            print(f"=====================================================")
            print(f"🚨 ALERT: Reverse Shell Activity Detected!")
            print(f"🛡️  Type: {shell_type} (Confidence: {confidence:.2f})")
            print(f"📡 Connection: {src_ip} -> {dst_ip}:{dst_port}")
            print(f"📝 Reason: {reason}")
            print(f"🛑 Action: {action_taken}")
            print(f"📦 Payload snippet: {payload[:50]}...")
            print(f"=====================================================")
            
            # Save to database
            models.save_alert(shell_type, src_ip, dst_ip, dst_port, payload, confidence, reason, action_taken)

def main():
    print("[*] Starting ShellSnare Detection Engine (IDS/IPS)...")
    models.init_db()
    print("[*] Sniffing for reverse shell traffic...")
    
    # Sniff TCP traffic, don't store in memory, pass to analyze_packet
    sniff(filter="tcp", prn=analyze_packet, store=False)

if __name__ == "__main__":
    main()

