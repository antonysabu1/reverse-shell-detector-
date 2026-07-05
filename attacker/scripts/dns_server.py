#!/usr/bin/env python3
"""Simple DNS C2 server for Phase 3.
It listens on UDP port 53 and responds with a TXT record containing a static payload.
In a real implementation it would decode the encoded command from the query name
and forward it to the victim container, but for our demo it just returns a fixed
string to confirm the tunnel is reachable.
"""
import socket
import threading

LISTEN_IP = "0.0.0.0"
PORT = 53

def handle_query(data, addr, sock):
    # Very minimal parsing – just send a TXT response.
    # Build DNS response: transaction ID, flags, QDCOUNT=1, ANCOUNT=1, ...
    txid = data[:2]
    flags = b"\x81\x80"  # Standard response, No error
    qdcount = b"\x00\x01"
    ancount = b"\x00\x01"
    nscount = b"\x00\x00"
    arcount = b"\x00\x00"
    dns_header = txid + flags + qdcount + ancount + nscount + arcount
    # Echo the query name from the request (skip the header and QTYPE/QCLASS)
    query = data[12:]
    # Construct answer section: name pointer (0xc00c), type TXT, class IN, ttl, rdlength, txt length, txt data
    name_ptr = b"\xc0\x0c"
    typ = b"\x00\x10"  # TXT
    cls = b"\x00\x01"  # IN
    ttl = b"\x00\x00\x00\x3c"  # 60 seconds
    txt = b"Hello-from-DNS-C2"
    rdlength = bytes([len(txt) + 1])
    rdata = bytes([len(txt)]) + txt
    answer = name_ptr + typ + cls + ttl + rdlength + rdata
    response = dns_header + query + answer
    sock.sendto(response, addr)

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, PORT))
    print(f"[*] DNS C2 server listening on {LISTEN_IP}:{PORT}")
    while True:
        data, addr = sock.recvfrom(512)
        threading.Thread(target=handle_query, args=(data, addr, sock), daemon=True).start()

if __name__ == "__main__":
    server()
