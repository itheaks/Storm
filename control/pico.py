import network
import socket
from machine import Pin, PWM
import time

# Define motor pins
motor1_forward = Pin(18, Pin.OUT)
motor1_backward = Pin(17, Pin.OUT)
motor2_forward = Pin(19, Pin.OUT)
motor2_backward = Pin(20, Pin.OUT)

# Define motor enable pins
motor1_enable = PWM(Pin(16), freq=1000)  # Motor 1 speed control
motor2_enable = PWM(Pin(21), freq=1000)  # Motor 2 speed control

# Define LED pins
led_forward = Pin(11, Pin.OUT)
led_backward = Pin(12, Pin.OUT)
led_left = Pin(13, Pin.OUT)
led_right = Pin(14, Pin.OUT)
led_default = Pin(15, Pin.OUT)

def set_speed(speed):
    duty_cycle = int((speed / 100) * 65535)  # PWM duty cycle as a 16-bit value
    motor1_enable.duty_u16(duty_cycle)
    motor2_enable.duty_u16(duty_cycle)

def stop():
    motor1_forward.off()
    motor1_backward.off()
    motor2_forward.off()
    motor2_backward.off()
    led_forward.off()
    led_backward.off()
    led_left.off()
    led_right.off()
    led_default.on()

def move_forward():
    stop()
    motor1_forward.on()
    motor2_forward.on()
    led_forward.on()
    led_default.off()

def move_backward():
    stop()
    motor1_backward.on()
    motor2_backward.on()
    led_backward.on()
    led_default.off()

def turn_left():
    stop()
    motor1_backward.on()
    motor2_forward.on()
    led_left.on()
    led_default.off()

def turn_right():
    stop()
    motor1_forward.on()
    motor2_backward.on()
    led_right.on()
    led_default.off()

# Connect to Wi-Fi
ssid = 'Project'
password = '12345678'

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    for _ in range(10):  # Retry up to 10 times
        if station.isconnected():
            print('Connection successful')
            print(station.ifconfig())
            return station
        print('Connecting to Wi-Fi...')
        time.sleep(1)

    raise RuntimeError('Failed to connect to Wi-Fi')

try:
    station = connect_wifi(ssid, password)
except RuntimeError as e:
    print(e)
    raise SystemExit('Exiting due to Wi-Fi connection failure')

# Set up a web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024).decode()
        request_path = request.split(' ')[1]
        path = request_path.split('?')[0]
        params = request_path.split('?')[1] if '?' in request_path else ''
        query_params = dict(x.split('=') for x in params.split('&')) if params else {}

        speed = int(query_params.get('speed', 50))  # Default speed to 50
        set_speed(speed)

        if '/forward' in path:
            move_forward()
        elif '/backward' in path:
            move_backward()
        elif '/left' in path:
            turn_left()
        elif '/right' in path:
            turn_right()
        elif '/stop' in path:
            stop()
        else:
            print('Unknown command:', request_path)

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send('<html><body>OK</body></html>')
    except Exception as e:
        print('Error:', e)
    finally:
        cl.close()

