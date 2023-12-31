from machine import Pin
import time
import network
import blynklib
import blynktimer
from servo import Servo

# Setup for Pins for Motion sensor and servo
motionSensor = Pin(14, Pin.IN, Pin.PULL_UP)
my_servo = Servo(pin_id=16)

# Authorization-value for Blynk
BLYNK_AUTH = ""
#variable for blynktimer
timer = blynktimer.Timer()

#internet credentials
ssid = ''
password = ''

# connect the network    
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)
   
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
    
 
"Connection to Blynk"
# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
 

# Principal function for when motion is detected
# Timer triggers funtion eveery second to check if motion is detected
@timer.register(interval=1, run_once=False)
def motionSensorListener():
        if motionSensor.value() == 1:
            my_servo.write(90)
            time.sleep(5)  # Wait for 5 seconds
            my_servo.write(140)
            blynk.log_event("photo_notification","photo was taken")
            

# Principal run loop for blynk functions
while True:
    blynk.run()
    timer.run()
