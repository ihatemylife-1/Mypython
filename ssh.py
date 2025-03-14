import os
import socket
import ipaddress
import threading
import paramiko

DEFAULT_CREDENTIALS = [
    ("root", "toor"),
    ("admin", "admin"),
    ("user", "user"),
    ("pi", "raspberry"),
    ("ubuntu", "ubuntu"),
    ("test", "test123"),
]

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def get_subnet():
    ip = input("Enter IP address: ")
    subnet_mask = input("Enter subnet mask: ")
    return ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)

def scan_ip(ip, open_hosts):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex((ip, 22)) == 0:
            print(f"[+] SSH Open: {ip}")
            open_hosts.append(ip)

def scan_network():
    clear_console()
    network = get_subnet()
    print(f"\nScanning {network}...\n")

    open_hosts = []
    threads = [threading.Thread(target=scan_ip, args=(str(ip), open_hosts)) for ip in network.hosts()]
    
    for t in threads: t.start()
    for t in threads: t.join()

    return open_hosts

def ssh_login(ip):
    print(f"\nAttempting SSH login on {ip}...\n")

    for username, password in DEFAULT_CREDENTIALS:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password, timeout=2)
            print(f"\n[+] SUCCESS: {username}:{password} on {ip}")
            ssh.close()
            return
        except paramiko.AuthenticationException:
            print(f"[-] Failed: {username}:{password}")
        except Exception as e:
            print(f"[!] Error: {e}")
            return

    print("\n[-] No valid credentials found.")

def main():
    open_hosts = scan_network()

    if not open_hosts:
        print("\nNo SSH hosts found.")
        return

    print("\nAvailable SSH hosts:")
    for idx, ip in enumerate(open_hosts, start=1):
        print(f"{idx}. {ip}")

    try:
        choice = int(input("\nSelect a target (number): ")) - 1
        if 0 <= choice < len(open_hosts):
            ssh_login(open_hosts[choice])
        else:
            print("\nInvalid choice.")
    except ValueError:
        print("\nInvalid input.")

if __name__ == "__main__":
    main()