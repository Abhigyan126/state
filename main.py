import socket



def handle_sensor_data(sensor_data):
    for sensor, state in sensor_data.items():
        if state == 'true':
            print(sensor, "triggered")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)  # Listen for incoming connections

    print("Server listening on port", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)

        # Receive data from the client
        data = client_socket.recv(1024).decode()

        if data:
            print("Received sensor data:", data)
            # Parse the received data into sensor states dictionary
            sensor_data = {}
            sensor_states = data.split(",")
            for state in sensor_states:
                sensor, state = state.split("-")
                sensor_data[sensor] = state

            # Handle the sensor data
            handle_sensor_data(sensor_data)

        client_socket.close()

if __name__ == "__main__":
    start_server(12345)  # Start the server on port 12345
