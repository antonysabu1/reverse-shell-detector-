#!/bin/bash

# Simple script to start a netcat listener
PORT=${1:-4444}
echo "[*] Attacker listening on port $PORT..."
echo "[*] Waiting for reverse shell connections..."
nc -lvnp $PORT
