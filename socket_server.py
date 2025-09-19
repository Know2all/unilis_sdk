import socket
import requests
import threading
from decoders.heme340 import Heme340


class SocketServer:
    def __init__(self, host="0.0.0.0", port=9001, callback_url="http://127.0.0.1:5000/data"):
        self.host = host
        self.port = port
        self.callback_url = callback_url
        self.latest_data = []
        self.server_socket = None
        self.thread = None

    def process_data(self, data):
        """Decode/process incoming data"""
        heme_340 = Heme340()
        result = heme_340.process(data)
        # print("Processed Data:",result)
        payload = {
            'raw_data':data,
            'result':result
        }
        try:
            _ = requests.post(self.callback_url, json=payload)
            print("Data posted to Flask app successfully.")
        except Exception as e:
            print(f"Error posting to callback URL: {e}")

    def handle_client(self, client_socket):
        """Handle each client in a separate thread"""
        with client_socket:
            while True:
                data = client_socket.recv(50000)
                if not data:
                    break

                decoded_data = data.decode("utf-8").split("\\r")
                if decoded_data:
                    # print("Data Received From Machine:", decoded_data)
                    self.process_data(decoded_data)

    def socket_server(self):
        """Main TCP socket listener"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"Socket server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")

            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def start(self):
        """Start the server in a background thread"""
        self.thread = threading.Thread(target=self.socket_server, daemon=True)
        self.thread.start()
        print("Socket server started in background thread.")


# Example usage
if __name__ == "__main__":
    server = SocketServer(host="0.0.0.0", port=9001, callback_url="http://127.0.0.1:5000/data")
    server.start()

    # Keep main thread alive
    while True:
        pass
