from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ESP32_IP = 'http://192.168.145.85/'  # Replace with the actual IP address of your ESP32

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    direction = request.form.get('direction')
    speed = request.form.get('speed', '50')  # Default speed to 50 if not provided
    try:
        response = requests.get(f"{ESP32_IP}/{direction}?speed={speed}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return str(e), 500
    return '', 204

@app.route('/servo1', methods=['POST'])
def servo1():
    angle = request.form.get('angle', '90')  # Default angle to 90 if not provided
    try:
        response = requests.get(f"{ESP32_IP}/servo1?angle={angle}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return str(e), 500
    return '', 204

@app.route('/servo2', methods=['POST'])
def servo2():
    angle = request.form.get('angle', '90')  # Default angle to 90 if not provided
    try:
        response = requests.get(f"{ESP32_IP}/servo2?angle={angle}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return str(e), 500
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
