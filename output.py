import socket
import threading
import time
# Sample array of outputs
outputs = ["sprinkler", "door", "lights", "access pass", "alarm1", "alarm2", "alarm3", "alearm4", "lifts"]

def send_output(output_index, ip_address, port, alternative_port_sender = 14346):
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
            print(f"An error occurred while sending output to port {port}: {str(e)}")
            # Try connecting to the alternative port
            try:
                print(f"Trying alternative port {alternative_port_sender}...")
                client_socket.connect((ip_address, alternative_port_sender))
                client_socket.sendall(output.encode())
                print("Output sent successfully to alternative port:", output)
            except Exception as e:
                print(f"Failed to send output to alternative port {alternative_port_sender}: {str(e)}")
        finally:
            # Close the socket
            client_socket.close()

def handle_output_data(output_data):
    print("Received output data:", output_data)

def start_output_listener(ip_address, port, alternative_port_listener):
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

def send_output_continuously(ip_address, port, alternative_port_sender):
    while True:
        user_input = input("Enter the index of the output you want to send (0-8): ")
        if user_input.strip():  # Check if the input is not empty
            try:
                index = int(user_input)
                send_output(index, ip_address, port, alternative_port_sender)
            except ValueError:
                print("Invalid input. Please enter a valid index (0-8).")
        else:
            print("Please enter a valid index (0-8).")

if __name__ == "__main__":
    # Define the server address and ports
    server_ip_address = '0.0.0.0'
    original_port_sender = 12347
    alternative_port_sender = 14347
    original_port_listener = 12346
    alternative_port_listener = 14346

    # Create a thread for continuous output sending
    send_thread = threading.Thread(target=send_output_continuously, args=(server_ip_address, original_port_sender, alternative_port_sender))
    send_thread.start()

    # Start the output listener on a separate thread using the specified alternative port
    start_output_listener(server_ip_address, original_port_listener, alternative_port_listener)
