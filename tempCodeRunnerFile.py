import socket
import time
import random

def generate_sensor_states(num_sensors = 5):
    sensor_states = {}
    for i in range(num_sensors):
        sensor_states[f"sensor_{i+1}"] = random.choice(['active', 'inactive', 'true'])
    return sensor_states

def send_sensor_states(sensor_states):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 12345)

    try:
        client_socket.connect(server_address)

        for sensor, state in sensor_states.items():
            data = f"{sensor}:{state}"
            client_socket.sendall(data.encode())

        client_socket.close()
        print("Sensor states sent successfully:", sensor_states)
    except Exception as e:
        print("An error occurred while sending sensor states:", str(e))

if __name__ == "__main__":
    while True:
        sensor_states = generate_sensor_states()
        send_sensor_states(sensor_states)
        time.sleep(1)