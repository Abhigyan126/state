import socket
import xml.etree.ElementTree as ET

def read_sensor_outputs(xml_file):
    sensor_outputs = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for sensor in root.findall('sensor'):
        name = sensor.find('name').text
        outputs = [trigger.text for trigger in sensor.find('triggers')]
        sensor_outputs[name] = outputs
    return sensor_outputs

def send_outputs(outputs):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address (192.168.1.9) and port
    server_address = ('127.0.0.1', 12346)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the outputs to the server
        client_socket.sendall(','.join(outputs).encode())

        print("Outputs sent successfully:", outputs)
    except Exception as e:
        print("An error occurred while sending outputs:", str(e))
    finally:
        # Close the socket
        client_socket.close()

def handle_sensor_data(sensor_data, sensor_outputs):
    for sensor, state in sensor_data.items():
        if state == 'true' and sensor in sensor_outputs:
            outputs = sensor_outputs[sensor]
            send_outputs(outputs)
        elif state == "inactive":
            print(sensor, "is inactive")

def start_server(port, xml_file):
    sensor_outputs = read_sensor_outputs(xml_file)

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
            handle_sensor_data(sensor_data, sensor_outputs)

        client_socket.close()

if __name__ == "__main__":
    start_server(12345, 'data.xml')  # Start the server on port 12345, reading triggers from 'sensor_triggers.xml'
