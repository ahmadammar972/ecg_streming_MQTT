// MQTT connection parameters
const host = 'localhost'; // Replace with your broker's hostname or IP address
const topic = 'ecg_data';

// Create a client instance
const client = new Paho.MQTT.Client(host, '', '');

// Callback function for successful connection
const onConnect = () => {
    console.log('Connected to MQTT broker');
    // Subscribe to the topic
    client.subscribe(topic);
};

// Callback function for receiving messages
const onMessageArrived = (message) => {
    const payload = message.payloadString;
    // Parse the received data (replace with your ECG data parsing logic)
    const ecgData = parseECGData(payload);

    // Update the Plotly graph with the parsed ECG data
    updatePlotlyGraph(ecgData);
};

// Connect to the MQTT broker
client.connect({ onSuccess: onConnect });

// Function to parse received ECG data (replace with your specific parsing logic)
function parseECGData(data) {
    // Example parsing (replace with your actual format)
    const values = data.split(',');
    const timestamps = [];
    const amplitudes = [];
    for (let i = 0; i < values.length; i += 2) {
        timestamps.push(parseFloat(values[i]));
        amplitudes.push(parseFloat(values[i + 1]));
    }
    return { timestamps, amplitudes };
}

// Function to update the Plotly graph (replace with customization)
function updatePlotlyGraph(data) {
    const layout = {
        title: 'ECG Data',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Amplitude' },
        // Add other layout options as needed
    };

    const trace = {
        x: data.timestamps,
        y: data.amplitudes,
        mode: 'lines', // Line chart for ECG data
        // Add other trace options for visual appearance
    };

    Plotly.newPlot('ecg-visualization', [trace], layout);
}

// Error handling (optional)
client.on('error', (error) => {
    console.error('MQTT Error:', error);
});
