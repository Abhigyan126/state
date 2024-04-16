import socket

def handle_output_data(output_data):
    print("Received output data:", output_data)

def start_output_listener(ip_address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)  # Listen for incoming connections

    print("Output listener listening on", ip_address + ":" + str(port))

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)

        # Receive data from the client
        data = client_socket.recv(1024).decode()

        if data:
            # Handle the output data
            handle_output_data(data)

        client_socket.close()

if __name__ == "__main__":
    start_output_listener('127.0.0.1', 12346)  
