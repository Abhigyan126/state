import socket
import xml.etree.ElementTree as ET
import threading

class SensorServer:
    def __init__(self, port, xml_file):
        self.port = port
        self.xml_file = xml_file
        self.sensor_outputs = self.read_sensor_outputs(xml_file)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(1)  # Listen for incoming connections
        self.output_data = {}  # Store received output data

    def read_sensor_outputs(self, xml_file):
        sensor_outputs = {}
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for sensor in root.findall('sensor'):
            name = sensor.find('name').text
            outputs = [trigger.text for trigger in sensor.find('triggers')]
            sensor_outputs[name] = outputs
        return sensor_outputs

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        if data:
            sensor_data = {}
            sensor_states = data.split(",")
            for state in sensor_states:
                sensor, state = state.split("-")
                sensor_data[sensor] = state
            self.handle_sensor_data(sensor_data)

        client_socket.close()

    def handle_sensor_data(self, sensor_data):
        for sensor, state in sensor_data.items():
            if state == 'true' and sensor in self.sensor_outputs:
                outputs = self.sensor_outputs[sensor]
                self.send_outputs(outputs)
            elif state == "inactive":
                print("Input failure:", sensor)

    def send_outputs(self, outputs):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12346)
        try:
            client_socket.connect(server_address)
            client_socket.sendall(','.join(outputs).encode())
            print("Outputs sent successfully:", outputs)
        except Exception as e:
            print("Logic Error:", str(e))
        finally:
            client_socket.close()


    def start_output_listener(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 12347))
        server_socket.listen(1)  # Listen for incoming connections

        print("Output listener listening on 0.0.0.0:12347")

        while True:
            client_socket, client_address = server_socket.accept()
            print("Connection from:", client_address)

            # Receive data from the client
            data = client_socket.recv(1024).decode()

            if data:
                # Handle the output data
                self.handle_output_data(data)

            client_socket.close()

    def handle_output_data(self, output_data):
        output_name = output_data.strip()
        self.output_data[output_name] = 1
        print("Error occurred at:", output_name)

    def start(self):
        output_listener_thread = threading.Thread(target=self.start_output_listener)
        output_listener_thread.start()

        while True:
            try:
                client_socket, _ = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
            except Exception as e:
                print("Input Failure: No connection to sensor")

if __name__ == "__main__":
    sensor_server = SensorServer(12345, 'data.xml')
    sensor_server.start()
