import socket
import threading
import time

# Sample array of outputs
outputs = {
    "output_1": 100,
    "output_2": 100,
    "output_3": 100,
    "output_4": 100,
    "output_5": 100,
    "output_6": 100,
    "output_7": 100,
    "output_8": 100,
    "output_9": 100
}

def send_output(output_index, ip_address, port):
    output_name = f"output_{output_index + 1}"
    if output_name in outputs:
        output = f"{output_name}:{outputs[output_name]}%"
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

def degrade_outputs():
    while True:
        for output in outputs:
            outputs[output] -= 2  # Degrade by 2% every second
            if outputs[output] < 40:
                print(f"Warning: Output {output} health is below 40%!")
            time.sleep(1)

def send_output_continuously(ip_address, port):
    while True:
        index = int(input("Enter the index of the output you want to send (0-8): "))
        send_output(index, ip_address, port)

if __name__ == "__main__":
    # Define the server address and port where you want to send the output
    server_ip_address = '127.0.0.1'
    server_port = 12347

    # Create threads for continuous output sending and output degradation
    send_thread = threading.Thread(target=send_output_continuously, args=(server_ip_address, server_port))
    degrade_thread = threading.Thread(target=degrade_outputs)

    # Start the threads
    send_thread.start()
    degrade_thread.start()

    # Start the output listener on a separate thread
    start_output_listener('127.0.0.1', 12346)
