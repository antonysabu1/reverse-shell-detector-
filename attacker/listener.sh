#!/bin/bash

# Simple script to start a netcat listener
PORT=${1:-4444}
MODE=${2:-nc}

if [ "$MODE" = "ssl" ]; then
    PEM_FILE="/opt/attacker/server.pem"
    if [ ! -f "$PEM_FILE" ]; then
        echo "[*] Generating self-signed SSL certificate..."
        openssl req -newkey rsa:2048 -nodes -keyout /opt/attacker/server.key -x509 -days 365 -out /opt/attacker/server.crt -subj "/CN=shellsnare-attacker"
        cat /opt/attacker/server.key /opt/attacker/server.crt > "$PEM_FILE"
        rm /opt/attacker/server.key /opt/attacker/server.crt
    fi
    echo "[*] Attacker listening for SSL connections on port $PORT..."
    socat openssl-listen:$PORT,cert="$PEM_FILE",verify=0,reuseaddr -
else
    echo "[*] Attacker listening on port $PORT..."
    echo "[*] Waiting for reverse shell connections..."
    nc -lvnp $PORT
fi
