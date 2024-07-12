from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# MQTT broker parameters
broker = 'localhost'  # Replace with your MQTT broker's IP address or hostname
port = 1883  # Default MQTT port
topic = 'ecg_data'  # MQTT topic to subscribe to

# Store received messages globally (in production, consider using a database or persistent storage)
messages = []

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    # Subscribe to the topic upon successful connection
    client.subscribe(topic)
    print(f'Subscribed to topic {topic}')

# Callback function when a message is received from the broker
def on_message(client, userdata, message):
    global messages
    payload = message.payload.decode()
    #print(f'Received message on topic {message.topic}: {payload}')
    
    # Assuming the payload is in the format "data:xxx"
    # Extract the numeric value and convert to float
    try:
        value = float(payload.split(':')[1])
        messages.append(value)
    except ValueError as e:
        print(f"Error parsing value from payload: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker, port, keepalive=60)

# Start the network loop in a non-blocking way
client.loop_start()

# Flask route to render HTML template with Plotly graph
@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/messages')
def get_messages():
    global messages
    return jsonify(messages)

@app.route('/graph')
def graph_page():
    return render_template('graph.html')

@app.route('/analysis')
def analysis_page():
    return render_template('analysis.html')

@app.route('/history')
def history_page():
    return render_template('history.html')

if __name__ == '__main__':
    app.run()
