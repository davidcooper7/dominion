import socket
import threading
import time

HOST = 'localhost'

class Server():
    def __init__(self, PORT, n_connections, timeout=120):
        self.n_connections = n_connections
        self.connections = {}
        self.lock = threading.Lock()  # Lock to manage shared resources
        self.timeout = timeout  # Timeout for recv

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.bind((HOST, PORT))
            self.s.listen()
            print(f'Server listening on {HOST}:{PORT}')

            while len(self.connections) < self.n_connections:
                conn, addr = self.s.accept()
                name = conn.recv(1024).decode()
                print(f"Client {name} connected from {addr}")
                self.connections[name] = conn

                client_thread = threading.Thread(target=self.handle_client, args=(conn, name), daemon=True)
                client_thread.start()

    def get_clients(self):
        return list(self.connections.items())

    def handle_client(self, conn, name):
        pass
        # try:
        #     conn.settimeout(self.timeout)  # Set a timeout for recv calls
        #     with conn:
        #         while True:
        #             try:
        #                 data = conn.recv(1024)
        #                 if not data:
        #                     print(f"Client {name} disconnected")
        #                     break
        #                 print(f"Received from {name}: {data.decode()}")
        #             except socket.timeout:
        #                 print(f"Client {name} timed out.")
        #             except Exception as e:
        #                 print(f"Error with client {name}: {e}")
        #                 break
        # finally:
        #     with self.lock:
        #         del self.connections[name]
        #     print(f"Connection with {name} closed")

    def close(self):
        # Close all client connections
        for conn in self.connections.values():
            conn.sendall(b'exit')
            conn.close()
        print("Server is closing...")

