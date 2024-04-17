import socket
import threading
import time
import random

# Sample array of outputs
outputs = {
    "Sprinkler": 100,
    "door": 100,
    "lights": 100,
    "access pass": 100,
    "alarm1": 100,
    "alarm2": 100,
    "alarm3": 100,
    "alarm4": 100,  # Corrected typo here
    "lifts": 100
}

# Define a lock to synchronize access to the 'outputs' dictionary
outputs_lock = threading.Lock()

def send_output(output_key, output_value, ip_address, port):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = (ip_address, port)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the output to the server
        output_message = f"{output_key}: {output_value}"
        client_socket.sendall(output_message.encode())  

        print("Output sent successfully:", output_message)
    except ConnectionRefusedError:
        print(f"Connection refused on port {port}.")
    except Exception as e:
        print(f"An error occurred while sending output to port {port}: {str(e)}")
    finally:
        # Close the socket
        client_socket.close()

def handle_output_data(output_data):
    print("Received output data:", output_data)

def start_output_listener(ip_address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)  # Listen for incoming connections

    print("Output listener listening on", ip_address + ":" + str(port))

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)

        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()

            if data:
                # Handle the output data
                handle_output_data(data)
        except Exception as e:
            print("An error occurred while receiving data:", str(e))
        finally:
            # Close the client socket
            client_socket.close()

def degrade_outputs(server_ip_address, server_port):
    # Delay thread start by 20 seconds
    time.sleep(50)
    
    while True:
        with outputs_lock:
            for output_name, percentage in outputs.items():
                outputs[output_name] -= 1  # Decrease percentage by 1 every second
                if outputs[output_name] < 40:
                    send_warning(server_ip_address, server_port, f"Warning: Output {output_name} health is below 40%!")
        time.sleep(1)

def send_warning(ip_address, port, message):
    if message:  # Check if message is not empty
        # Create a client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = (ip_address, port)

        try:
            # Connect to the server
            client_socket.connect(server_address)

            # Send the message to the server
            client_socket.sendall(message.encode())

            print("Warning sent successfully:", message)
        except ConnectionRefusedError:
            print(f"Connection refused on port {port}.")
        except Exception as e:
            print(f"An error occurred while sending warning to port {port}: {str(e)}")
        finally:
            # Close the socket
            client_socket.close()

def send_output_continuously(ip_address, port):
    # Delay thread start by 20 seconds
    time.sleep(20)
    
    while True:
        try:
            # Generate a random output key and value
            output_key, output_value = random.choice(list(outputs.items()))
            
            # Send the output corresponding to the random key
            send_output(output_key, output_value, ip_address, port)
            
            # Sleep for a fixed interval before sending the next output
            time.sleep(10)  # Adjust the interval as needed (e.g., 10 seconds)
        except Exception as e:
            print("An error occurred while sending output:", str(e))


if __name__ == "__main__":
    # Define the server address and port
    server_ip_address = '0.0.0.0'  # Change this to your server's IP address
    original_port_sender = 12347
    original_port_listener = 12346

    # Create a thread for continuous output sending
    send_thread = threading.Thread(target=send_output_continuously, args=(server_ip_address, original_port_sender))
    send_thread.start()

    # Start the output listener on a separate thread
    listener_thread = threading.Thread(target=start_output_listener, args=(server_ip_address, original_port_listener))
    listener_thread.start()

    # Start the thread for degrading output percentages
    degrade_thread = threading.Thread(target=degrade_outputs, args=(server_ip_address, original_port_sender))
    degrade_thread.start()
