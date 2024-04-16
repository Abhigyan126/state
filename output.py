import socket
import threading

# Sample array of outputs
outputs = ["output_1", "output_2", "output_3", "output_4", "output_5", "output_6", "output_7", "output_8", "output_9"]

def send_output(output_index, ip_address, port):
    if output_index < len(outputs):
        output = outputs[output_index]
        # Create a client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = (ip_address, port)

        try:
            # Connect to the server
            client_socket.connect(server_address)

            # Send the output to the server
            client_socket.sendall(output.encode())

            print("Output sent successfully:", output)
        except Exception as e:
            print("An error occurred while sending output:", str(e))
        finally:
            # Close the socket
            client_socket.close()
    else:
        print("Invalid output index:", output_index)

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

def send_output_continuously(ip_address, port):
    while True:
        index = int(input("Enter the index of the output you want to send (0-8): "))
        send_output(index, ip_address, port)

if __name__ == "__main__":
    # Define the server address and port where you want to send the output
    server_ip_address = '127.0.0.1'
    server_port = 12347

    # Create a thread for continuous output sending
    send_thread = threading.Thread(target=send_output_continuously, args=(server_ip_address, server_port))
    send_thread.start()

    # Start the output listener on a separate thread
    start_output_listener('127.0.0.1', 12346)
