import socket
import threading
from collections import defaultdict
import argparse

# Dictionary to store connection information
connection_dict = defaultdict(list)

def handle_client(client_socket, client_address, port):
    global connection_dict
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected")
                connection_dict[port].remove(client_address)
                break
            print(f"Received {data} from {client_address}")
            client_socket.send(f"Hello, you are connected from {client_address} via port {client_address[1]}\n".encode())
            print(f"Total connections on port {port}: {len(connection_dict[port])}, Current connection index: {connection_dict[port].index(client_address)+1}")
        except Exception as e:
            print(f"Error: {e}. Closing connection with {client_address}")
            if client_address in connection_dict[port]:
                connection_dict[port].remove(client_address)
            break

    client_socket.close()

def server_program(port):
    host = '0.0.0.0'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        connection_dict[port].append(addr)
        print(f"Connection from {addr}")
        # Sending welcome message right after client connection
        welcome_message = f"Welcome! You are connected from {addr} via port {port}\n"
        client_socket.send(welcome_message.encode())
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, port))
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
