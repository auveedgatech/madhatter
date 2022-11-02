import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True: 
    if GPIO.input(10) == GPIO.HIGH:
        print('Team leader wants alice gone so that the wonderland is about him.')
        
    sleep(0.15)