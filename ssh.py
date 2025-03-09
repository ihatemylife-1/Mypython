import socket
import ipaddress
import threading
import netifaces

def get_local_subnet():
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    addr_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
    ip = addr_info['addr']
    netmask = addr_info['netmask']
    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
    return network

def scan_ip(ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((ip, 22))
        if result == 0:
            print(f"[+] SSH Open: {ip}")

def scan_network():
    network = get_local_subnet()
    print(f"Scanning network: {network}")

    threads = []
    for ip in network.hosts():
        t = threading.Thread(target=scan_ip, args=(str(ip),))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    scan_network()