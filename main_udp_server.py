import socket
import threading
from collections import defaultdict
import argparse

# Dictionary to store connection information
connection_dict = defaultdict(int)

def handle_client(client_socket, client_address, port):
    global connection_dict
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            if not data:
                break
            print(f"Received {data} from {addr}")
            client_socket.sendto(f"Hello, you are connected from {addr} via port {port}\n".encode(), addr)
            connection_dict[port] += 1
            print(f"Total connections on port {port}: {connection_dict[port]}")
        except Exception as e:
            print(f"Error: {e}. Closing connection with {addr}")
            break

def server_program(port):
    host = '0.0.0.0'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Connection from {addr}")
        welcome_message = f"Welcome! You are connected from {addr} via port {port}\n"
        server_socket.sendto(welcome_message.encode(), addr)
        client_thread = threading.Thread(target=handle_client, args=(server_socket, addr, port))
        client_thread.start()

def main():
    parser = argparse.ArgumentParser(description='Start a server that listens to given ports.')
    parser.add_argument('--ports', metavar='P', type=int, nargs='+', help='an integer for the ports to bind')
    args = parser.parse_args()
    
    ports = args.ports if args.ports else [80, 443]

    print(f'listen 0.0.0.0:[{ports}]')
    for port in ports:
        server_thread = threading.Thread(target=server_program, args=(port,))
        server_thread.start()

if __name__ == "__main__":
    main()
