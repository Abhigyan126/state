import socket
import time
import random

def generate_sensor_states(num_sensors=5):
    sensor_states = {}
    for i in range(num_sensors):
        sensor_states[f"sensor_{i+1}"] = random.choice(['active', 'inactive', 'true'])
    return sensor_states

def send_sensor_states(sensor_states):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 12345)

    try:
        client_socket.connect(server_address)

        # Construct the message string
        message = ",".join([f"{sensor}-{state}" for sensor, state in sensor_states.items()])

        # Send the message
        client_socket.sendall(message.encode())

        client_socket.close()
        print("Sensor states sent successfully:", sensor_states)
    except Exception as e:
        print("An error occurred while sending sensor states:", str(e))

if __name__ == "__main__":
    while True:
        sensor_states = generate_sensor_states()
        send_sensor_states(sensor_states)
        time.sleep(1)
