import socket
import time
import random

def generate_sensor_states(num_sensors=5):
    sensor_states = {}
    for i in range(num_sensors):
        sensor_states[f"sensor_{i+1}"] = random.choice(['active', 'inactive', 'true'])
    return sensor_states

def send_sensor_states(sensor_states, port=12345, alternative_port=13345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', port)

    try:
        client_socket.connect(server_address)

        # Construct the message string
        message = ",".join([f"{sensor}-{state}" for sensor, state in sensor_states.items()])

        # Send the message
        client_socket.sendall(message.encode())

        client_socket.close()
        print("Sensor states sent successfully to port:", port)
    except Exception as e:
        print(f"An error occurred while sending sensor states to port {port}: {str(e)}")
        # If error occurs, try connecting to alternative port
        if port != alternative_port:
            send_sensor_states(sensor_states, alternative_port)

if __name__ == "__main__":
    # Delay the execution by 20 seconds
    time.sleep(50)

    while True:
        sensor_states = generate_sensor_states()
        send_sensor_states(sensor_states)
        time.sleep(1)
