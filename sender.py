import time
import pandas as pd
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

# MQTT settings
MQTT_BROKER = '199.212.33.168'
MQTT_PORT = 1883
MQTT_TOPIC = 'ecg_data'

# Create a MQTT client
mqtt_client = mqtt.Client()

# Connect to MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start MQTT loop
mqtt_client.loop_start()

# Define the PQRST data for 5 heartbeats
ecg_pqrst_data = [
    # Heartbeat 1
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 2
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 3
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 4
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 5
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0 
]
"""
# Plot the PQRST complex data
plt.figure(figsize=(12, 5))
plt.plot(ecg_pqrst_data, label='PQRST Complex Signal')
plt.xlabel('Time (arbitrary units)')
plt.ylabel('Voltage (arbitrary units)')
plt.title('ECG Signal (PQRST Complex) for 5 Heartbeats')
plt.legend()
plt.grid(True)
plt.show()
"""
# Publish ECG data
while True:
    for ecg_value in ecg_pqrst_data:
        # Publish ECG data to MQTT topic
        mqtt_client.publish(MQTT_TOPIC, f'data:{ecg_value}')
    
        print(f"Published: data:{ecg_value}")
    
        # Publish data every 0.01 second (100 Hz sampling rate)
        time.sleep(0.01)

# Disconnect MQTT client after streaming is complete
# Note: The following line will not be reached due to the infinite loop above
# mqtt_client.loop_stop()
# mqtt_client.disconnect()
