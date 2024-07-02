import network
import socket
from machine import Pin, PWM
import time

# Define motor pins
motor1_forward = Pin(16, Pin.OUT)
motor1_backward = Pin(17, Pin.OUT)
motor2_forward = Pin(18, Pin.OUT)
motor2_backward = Pin(19, Pin.OUT)

# Define LED pins
led_forward = Pin(10, Pin.OUT)
led_backward = Pin(11, Pin.OUT)
led_left = Pin(12, Pin.OUT)
led_right = Pin(13, Pin.OUT)

# Setup PWM for motor speed control
pwm_motor1 = PWM(motor1_forward)
pwm_motor2 = PWM(motor2_forward)
pwm_motor1.freq(1000)
pwm_motor2.freq(1000)

def stop():
    motor1_forward.off()
    motor1_backward.off()
    motor2_forward.off()
    motor2_backward.off()
    led_forward.off()
    led_backward.off()
    led_left.off()
    led_right.off()

def move_forward(speed):
    stop()
    pwm_motor1.duty_u16(int(speed))
    pwm_motor2.duty_u16(int(speed))
    led_forward.on()

def move_backward(speed):
    stop()
    motor1_backward.on()
    motor2_backward.on()
    led_backward.on()

def turn_left(speed):
    stop()
    motor1_backward.on()
    pwm_motor2.duty_u16(int(speed))
    led_left.on()

def turn_right(speed):
    stop()
    pwm_motor1.duty_u16(int(speed))
    motor2_backward.on()
    led_right.on()

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
        query_params = request_path.split('?')
        path = query_params[0]
        speed = 716  # Default speed
        if len(query_params) > 1:
            params = query_params[1].split('&')
            for param in params:
                if param.startswith('speed='):
                    speed = int(param.split('=')[1])

        if '/forward' in path:
            move_forward(speed)
        elif '/backward' in path:
            move_backward(speed)
        elif '/left' in path:
            turn_left(speed)
        elif '/right' in path:
            turn_right(speed)
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
