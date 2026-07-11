import logging
from scapy.all import IP, TCP, send

logging.basicConfig(level=logging.INFO, format='[*] %(message)s')

def inject_rst(packet):
    """
    Injects forged TCP RST packets into the network to sever an active connection.
    Sends one RST to the destination (attacker) and one to the source (victim).
    """
    if not (packet.haslayer(IP) and packet.haslayer(TCP)):
        return False
        
    ip_src = packet[IP].src
    ip_dst = packet[IP].dst
    tcp_sport = packet[TCP].sport
    tcp_dport = packet[TCP].dport
    tcp_seq = packet[TCP].seq
    tcp_ack = packet[TCP].ack
    
    logging.info(f"🛑 IPS: Injecting TCP RST for {ip_src}:{tcp_sport} <-> {ip_dst}:{tcp_dport}")
    
    try:
        # Forge RST packet to the destination (Attacker) pretending to be the source (Victim)
        rst_to_dst = IP(src=ip_src, dst=ip_dst) / \
                     TCP(sport=tcp_sport, dport=tcp_dport, flags="R", seq=tcp_seq)
                     
        # Forge RST packet to the source (Victim) pretending to be the destination (Attacker)
        rst_to_src = IP(src=ip_dst, dst=ip_src) / \
                     TCP(sport=tcp_dport, dport=tcp_sport, flags="R", seq=tcp_ack)
                     
        # Send both packets silently on the network layer
        send(rst_to_dst, verbose=0)
        send(rst_to_src, verbose=0)
        return True
    except Exception as e:
        logging.error(f"Failed to inject RST: {e}")
        return False
