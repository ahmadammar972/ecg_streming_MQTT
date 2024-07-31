from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from scipy.signal import butter, lfilter, iirnotch
from datetime import datetime

app = Flask(__name__)

# MQTT broker parameters
broker = '199.212.33.168'  # Replace with your MQTT broker's IP address or hostname
port = 1883  # Default MQTT port
topic = 'ecg_data'  # MQTT topic to subscribe to

# Database connection parameters for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ecg_user:IOT_ECG@localhost/ecg_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Patient model
class Patient(db.Model):
    PatientID = db.Column(db.Integer, primary_key=True, default=0)
    FirstName = db.Column(db.String(255))
    LastName = db.Column(db.String(255))
    DateOfBirth = db.Column(db.Date)
    Gender = db.Column(db.String(50))
    MedicalHistory = db.Column(db.Text)

# Define the ECGData model
class ECGData(db.Model):
    ECGDataID = db.Column(db.Integer, primary_key=True, default=0)
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'), default=0)
    Timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    Data = db.Column(db.Text)

# Define the CardECGData model
class CardECGData(db.Model):
    CardECGDataID = db.Column(db.Integer, primary_key=True, default=0)
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'), default=0)
    Timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    CleanedData = db.Column(db.Text)

# Define the PatientECGData model
class PatientECGData(db.Model):
    PatientECGDataID = db.Column(db.Integer, primary_key=True, default=0)
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'), default=0)
    Timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    DataWithRecommendations = db.Column(db.Text)

# Create the database tables
with app.app_context():
    db.create_all()

# High-pass filter parameters
fs = 1000  # Sampling frequency in Hz
highpass_cutoff = 0.5  # High-pass filter cutoff frequency in Hz
b_high, a_high = butter(1, highpass_cutoff / (0.5 * fs), btype='high')

# Notch filter parameters for 50Hz or 60Hz noise
notch_freq = 50  # Change to 60 if your power line frequency is 60Hz
quality_factor = 30.0
b_notch, a_notch = iirnotch(notch_freq / (0.5 * fs), quality_factor)

# Buffer for storing recent ECG values
buffer_size = 100  # Number of samples to keep in the buffer
ecg_buffer = []

# Store received messages globally
messages = {'id': [], 'value': []}

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    # Subscribe to the topic upon successful connection
    client.subscribe(topic)
    print(f'Subscribed to topic {topic}')

# Callback function when a message is received from the broker
def on_message(client, userdata, message):
    global messages, ecg_buffer
    payload = message.payload.decode()
    try:
        value = payload.split(',')
        ecg_id = float(value[0])
        ecg_value = float(value[1])
        
        # Update the buffer
        ecg_buffer.append(ecg_value)
        if len(ecg_buffer) > buffer_size:
            ecg_buffer.pop(0)
        
        # Apply high-pass filter if buffer has enough data
        if len(ecg_buffer) >= buffer_size:
            # Apply high-pass filter
            filtered_values = lfilter(b_high, a_high, ecg_buffer)
            # Apply notch filter
            filtered_values = lfilter(b_notch, a_notch, filtered_values)
            filtered_value = filtered_values[-1]  # Get the most recent filtered value
            
            messages['value'].append(filtered_value)
            messages['id'].append(ecg_id)
            save_to_db(filtered_value)
    except ValueError as e:
        print(f"Error parsing value from payload: {e}")

# Save ECG data to the database
def save_to_db(value):
    try:
        with app.app_context():
            new_record = ECGData(value=value)
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

@app.route('/cardECGView')
def card_ecg_view():
    # Fetch all available PatientIDs
    patients = Patient.query.all()
    patient_ids = [patient.PatientID for patient in patients]
    return render_template('card_ecg_view.html', patient_ids=patient_ids)

@app.route('/getECGData', methods=['POST'])
def get_ecg_data():
    patient_id = request.form['patient_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    # Query the database for the specified data
    ecg_data = CardECGData.query.filter(
        CardECGData.PatientID == patient_id,
        CardECGData.Timestamp >= start_date,
        CardECGData.Timestamp <= end_date
    ).all()

    # Convert data to a format suitable for visualization
    data = {
        'timestamps': [record.Timestamp for record in ecg_data],
        'values': [record.CleanedData for record in ecg_data]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

