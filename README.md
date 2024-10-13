# Fault Detection System on State Machines

This project demonstrates a fault detection mechanism on a state machine using a server-client architecture, where sensor states are monitored and evaluated. The system reads sensor configurations from an XML file and processes real-time sensor inputs, sending out corresponding outputs and warnings when certain conditions are met.

## Features
- **Sensor Input Handling**: Processes input data from sensors and evaluates their states (e.g., `active`, `inactive`, `true`).
- **State Machine Management**: Triggers appropriate outputs based on the sensor state and predefined transitions.
- **Output Listener**: Listens for outputs triggered by the sensors and logs or handles the events.
- **Fault Detection**: Detects input failures and generates warnings if sensor health degrades or becomes inactive.
- **Multithreading**: Utilizes multithreading to handle sensor input processing, output monitoring, and fault degradation simultaneously.

## Architecture

The project consists of two main components:

1. **Sensor Server**: Listens for sensor state updates from clients, processes the inputs, and triggers the corresponding outputs.
2. **Client Simulation**: Simulates sensor state generation and sends them to the server. This includes logic for degrading sensor output over time.

### Main Classes

- **SensorServer**:
    - Handles incoming sensor states from clients.
    - Parses the sensor configuration from an XML file to determine state transitions.
    - Sends output data or warnings when specific conditions are triggered.
    
- **Client Simulation**:
    - Generates random sensor states and sends them to the server.
    - Simulates output degradation and sends warnings if output health drops below 40%.
    
- **Listener and Output Handling**:
    - A listener that accepts output data from the server, handling various actions such as triggering alarms, sprinklers, etc.
    - Degradation of outputs over time to simulate faults or wear and tear of components.

## File Structure

/project-root  
├── data.xml              # XML file containing sensor configurations and triggers  
├── server.py             # Contains the SensorServer class, which processes sensor inputs  
├── client.py             # Simulates the client that generates and sends sensor states to the server  
├── README.md             # Project documentation


### Example `data.xml` Structure

```xml
<sensors>
    <sensor>
        <name>sensor_1</name>
        <triggers>
            <trigger>output1</trigger>
            <trigger>output2</trigger>
        </triggers>
    </sensor>
    <sensor>
        <name>sensor_2</name>
        <triggers>
            <trigger>alarm</trigger>
        </triggers>
    </sensor>
</sensors>
```

