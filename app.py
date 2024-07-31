from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# MQTT broker parameters
broker = '199.212.33.168'  # Replace with your MQTT broker's IP address or hostname
port = 1883  # Default MQTT port
topic = 'ecg_data'  # MQTT topic to subscribe to

# Database connection parameters for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecg_data.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the ECG model
class ECG(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# Create the database tables
with app.app_context():
    db.create_all()

# Store received messages globally (in production, consider using a database or persistent storage)
messages = {'id':[],'value':[]}

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
        value = payload.split(',')
        messages['value'].append(float(value[1]))
        messages['id'].append(float(value[0]))
        save_to_db(value)
    except ValueError as e:
        print(f"Error parsing value from payload: {e}")

# Save ECG data to the database
def save_to_db(value):
    try:
        with app.app_context():
            new_record = ECG(value=value)
            db.session.add(new_record)
            db.session.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")

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
    app.run(host='0.0.0.0', port=5000)

