import machine
import utime
from machine import Pin, PWM
import network
from time import sleep
from picozero import pico_temp_sensor, pico_led

servo1 = PWM(Pin(19))
servo2 = PWM(Pin(26))

servo1.freq(50)
servo2.freq(50)

def set_angle(servo, angle):
    duty = int((angle / 18) + 2.5)
    servo.duty_u16(duty)
    sleep(0.3)

# Set initial position to 90 degrees
set_angle(servo1, 90)
set_angle(servo2, 90)

ssid = "your_wifi_ssid"
password = "your_wifi_password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep(1)

print('Connected to WiFi')
print(wlan.ifconfig())

# Now create a basic web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)

print('Listening on', addr)

while True:
    client, addr = server.accept()
    print('Client connected from', addr)
    request = client.recv(1024).decode()
    print('Request:', request)
    
    request_path = request.split(' ')[1]
    
    if 'slider1' in request_path and 'slider2' in request_path:
        slider1 = request_path.split('slider1=')[1].split('&')[0]
        slider2 = request_path.split('slider2=')[1]
        
        angle1 = int(slider1)
        angle2 = int(slider2)
        
        set_angle(servo1, angle1)
        set_angle(servo2, angle2)
        
    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    response += open('index.html').read()
    
    client.send(response)
    client.close()