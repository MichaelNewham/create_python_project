# 1. Flask Application (backend/app.py)
# Replace Django with lightweight Flask as recommended by AI

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_login import LoginManager
import sqlite3
import json

app = Flask(__name__, 
    template_folder='../frontend/templates',
    static_folder='../frontend/static')
app.config['SECRET_KEY'] = 'your-secret-key-here'

socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager(app)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  temperature REAL,
                  humidity REAL,
                  pressure REAL,
                  wind_speed REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather/latest')
def get_latest_weather():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1')
    data = c.fetchone()
    conn.close()
    
    if data:
        return jsonify({
            'timestamp': data[1],
            'temperature': data[2],
            'humidity': data[3],
            'pressure': data[4],
            'wind_speed': data[5]
        })
    return jsonify({})

@socketio.on('weather_update')
def handle_weather_update(data):
    # Store in database
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('INSERT INTO weather_data (temperature, humidity, pressure, wind_speed) VALUES (?, ?, ?, ?)',
              (data['temperature'], data['humidity'], data['pressure'], data['wind_speed']))
    conn.commit()
    conn.close()
    
    # Broadcast to all clients
    socketio.emit('weather_data', data, broadcast=True)

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)


# 2. Frontend HTML Template (frontend/templates/index.html)
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Weather Station</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>ESP32 Weather Station</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Temperature</h3>
                <p class="stat-value" id="temperature">--°C</p>
            </div>
            <div class="stat-card">
                <h3>Humidity</h3>
                <p class="stat-value" id="humidity">--%</p>
            </div>
            <div class="stat-card">
                <h3>Pressure</h3>
                <p class="stat-value" id="pressure">-- hPa</p>
            </div>
            <div class="stat-card">
                <h3>Wind Speed</h3>
                <p class="stat-value" id="wind_speed">-- km/h</p>
            </div>
        </div>
        
        <div class="chart-container">
            <canvas id="weatherChart"></canvas>
        </div>
        
        <div class="camera-section">
            <h2>Live Camera Feed</h2>
            <img id="camera-stream" src="/video_feed" alt="Camera Feed">
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
"""


# 3. Frontend JavaScript (frontend/static/js/app.js)
"""
const socket = io();
const maxDataPoints = 20;

// Initialize Chart.js
const ctx = document.getElementById('weatherChart').getContext('2d');
const weatherChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature (°C)',
            data: [],
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1
        }, {
            label: 'Humidity (%)',
            data: [],
            borderColor: 'rgb(54, 162, 235)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// WebSocket event handlers
socket.on('weather_data', (data) => {
    // Update current values
    document.getElementById('temperature').textContent = data.temperature + '°C';
    document.getElementById('humidity').textContent = data.humidity + '%';
    document.getElementById('pressure').textContent = data.pressure + ' hPa';
    document.getElementById('wind_speed').textContent = data.wind_speed + ' km/h';
    
    // Update chart
    const time = new Date().toLocaleTimeString();
    weatherChart.data.labels.push(time);
    weatherChart.data.datasets[0].data.push(data.temperature);
    weatherChart.data.datasets[1].data.push(data.humidity);
    
    // Keep only last N data points
    if (weatherChart.data.labels.length > maxDataPoints) {
        weatherChart.data.labels.shift();
        weatherChart.data.datasets.forEach(dataset => dataset.data.shift());
    }
    
    weatherChart.update();
});
"""


# 4. ESP32 Camera Streaming Route (backend/camera_stream.py)
import cv2
import threading
import time

class CameraStream:
    def __init__(self, esp32_ip="192.168.1.100"):
        self.esp32_url = f"http://{esp32_ip}/capture"
        self.frame = None
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()
    
    def update(self):
        while True:
            try:
                cap = cv2.VideoCapture(self.esp32_url)
                ret, frame = cap.read()
                if ret:
                    self.frame = frame
                cap.release()
                time.sleep(0.1)  # 10 FPS
            except Exception as e:
                print(f"Camera error: {e}")
                time.sleep(1)
    
    def get_frame(self):
        if self.frame is not None:
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
        return None

# Add to Flask app
camera = CameraStream()

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = camera.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
    
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# 5. ESP32 Arduino Sketch (firmware/src/main.cpp)
"""
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <esp_camera.h>
#include <DHT.h>

// Pin definitions
#define DHT_PIN 13
#define DHT_TYPE DHT22

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "YOUR_SERVER_IP";

DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient client(espClient);
WebServer server(80);

// Camera pins for ESP32-CAM
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() {
    Serial.begin(115200);
    
    // Initialize DHT sensor
    dht.begin();
    
    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi connected");
    
    // Initialize camera
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    // ... (rest of camera config)
    
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed with error 0x%x", err);
    }
    
    // Setup MQTT
    client.setServer(mqtt_server, 1883);
    
    // Setup web server routes
    server.on("/capture", handleCapture);
    server.begin();
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    
    // Read sensor data every 5 seconds
    static unsigned long lastRead = 0;
    if (millis() - lastRead > 5000) {
        float temperature = dht.readTemperature();
        float humidity = dht.readHumidity();
        
        if (!isnan(temperature) && !isnan(humidity)) {
            StaticJsonDocument<200> doc;
            doc["temperature"] = temperature;
            doc["humidity"] = humidity;
            doc["pressure"] = 1013.25; // Placeholder
            doc["wind_speed"] = random(0, 20);
            
            char buffer[512];
            serializeJson(doc, buffer);
            client.publish("weather/data", buffer);
        }
        lastRead = millis();
    }
    
    server.handleClient();
}

void handleCapture() {
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
        server.send(500, "text/plain", "Camera capture failed");
        return;
    }
    
    server.sendHeader("Content-Type", "image/jpeg");
    server.send_P(200, "image/jpeg", (const char *)fb->buf, fb->len);
    esp_camera_fb_return(fb);
}

void reconnect() {
    while (!client.connected()) {
        if (client.connect("ESP32Client")) {
            Serial.println("MQTT connected");
        } else {
            delay(5000);
        }
    }
}
"""


# 6. Deployment Script (scripts/deploy_to_pi.sh)
"""
#!/bin/bash

# Deploy to Raspberry Pi Script
PI_HOST="pi@raspberrypi.local"
PROJECT_DIR="/home/pi/esp32-weather-app"

echo "Deploying to Raspberry Pi..."

# Sync project files
rsync -avz --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
    --exclude='firmware/.*' --exclude='*.pyc' \
    ./ $PI_HOST:$PROJECT_DIR/

# Install dependencies on Pi
ssh $PI_HOST << 'EOF'
cd /home/pi/esp32-weather-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
EOF

# Create systemd service
ssh $PI_HOST << 'EOF'
sudo tee /etc/systemd/system/weather-app.service > /dev/null << 'SERVICE'
[Unit]
Description=ESP32 Weather App
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/esp32-weather-app/backend
Environment="PATH=/home/pi/esp32-weather-app/.venv/bin"
ExecStart=/home/pi/esp32-weather-app/.venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable weather-app.service
sudo systemctl restart weather-app.service
EOF

echo "Deployment complete!"
"""


# 7. Updated pyproject.toml with correct dependencies
[tool.poetry.dependencies]
python = "^3.11"
flask = "^3.0.0"
flask-socketio = "^5.3.0"
flask-login = "^0.6.0"
opencv-python = "^4.9.0"
python-socketio = "^5.11.0"
websocket-client = "^1.7.0"


# 8. Create requirements.txt for Raspberry Pi deployment
flask==3.0.0
flask-socketio==5.3.0
flask-login==0.6.0
opencv-python-headless==4.9.0.80
python-socketio==5.11.0
eventlet==0.35.1