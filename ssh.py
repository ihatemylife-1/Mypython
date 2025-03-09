import socket
import ipaddress
import threading

def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_subnet():
    ip = get_local_ip()
    print(f"Detected IP: {ip}")
    subnet_mask = input("Enter your subnet mask: ")
    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
    return network

def scan_ip(ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((ip, 22))
        if result == 0:
            print(f"[+] SSH Open: {ip}")

def scan_network():
    network = get_subnet()
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