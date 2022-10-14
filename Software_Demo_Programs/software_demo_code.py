import RPi.GPIO as GPIO
from time import sleep
from enum import Enum
import pygame

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup States
class State(Enum):
    IDLE = 0
    
    #TESTS
    LED_TEST = 1
    AUDIO_TEST = 2
    MOTION_HAT_TEST = 3
    MOTION_TEACUPS_TEST = 4
    
    #DIRECTOR STATES
    CONNECT_TO_DIRECTOR = 5
    WAIT_FOR_INTRUCTION = 6
    DECODE_FILE = 7
    
# Setup Current State
current_state = State.IDLE

# Setup Interrupts
def reset_callback(channel):
    print("Resetting to Idle")
    global current_state
    current_state = State.IDLE
    
    
def led_test_callback(channel):
    global current_state
    current_state = State.LED_TEST
    
def audio_test_callback(channel):
    global current_state
    current_state = State.AUDIO_TEST

def motion_hat_callback(channel):
    global current_state
    current_state = State.MOTION_HAT_TEST
    
def motion_teacups_callback(channel):
    global current_state
    current_state = State.MOTION_TEACUPS_TEST

# Setup Pushbuttons

#Reset Button
pin_reset = 10
GPIO.setup(pin_reset, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_reset, GPIO.RISING, callback=reset_callback)

#LED Test Button
pin_led_test = 12
GPIO.setup(pin_led_test, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_led_test, GPIO.RISING, callback=led_test_callback)

# AUDIO Test Button
pin_audio_test = 16
GPIO.setup(pin_audio_test, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_audio_test, GPIO.RISING, callback=audio_test_callback)

# Motion Hat Test Button
pin_hat_test = 40
GPIO.setup(pin_hat_test, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_hat_test, GPIO.RISING, callback=motion_hat_callback)

# Motion Teacups Test Button
pin_motion_test = 37
GPIO.setup(pin_motion_test, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pin_motion_test, GPIO.RISING, callback=motion_teacups_callback)

# Setup External Components:
led_out = GPIO.LOW
led_output_port = 18
GPIO.setup(led_output_port, GPIO.OUT)

hat_pin = 22
GPIO.setup(hat_pin, GPIO.OUT)
servo_hat = GPIO.PWM(hat_pin, 50)
servo_hat.start(2.5)

cups_pin = 11
GPIO.setup(cups_pin, GPIO.OUT)
servo_cups = GPIO.PWM(cups_pin, 50)
servo_cups.start(2.5)

# Servo Functions
def move_servo(p):
    p.ChangeDutyCycle(5)
    sleep(0.5)
    p.ChangeDutyCycle(7.5)
    sleep(0.5)
    p.ChangeDutyCycle(10)
    sleep(0.5)
    p.ChangeDutyCycle(12.5)
    sleep(0.5)
    p.ChangeDutyCycle(10)
    sleep(0.5)
    p.ChangeDutyCycle(7.5)
    sleep(0.5)
    p.ChangeDutyCycle(5)
    sleep(0.5)
    p.ChangeDutyCycle(2.5)
    sleep(0.5)


while True:
    if current_state == State.IDLE:
        led_out = GPIO.LOW
        GPIO.output(led_output_port, led_out);
        servo_hat.ChangeDutyCycle(0)
        servo_cups.ChangeDutyCycle(0)

        sleep(0.1)
    elif current_state == State.LED_TEST:
        # Set LED High:
        print("Starting LED Test...")
        led_out = GPIO.HIGH;
        GPIO.output(led_output_port, led_out);
        sleep(6)
        led_out = GPIO.LOW;
        GPIO.output(led_output_port, led_out);
        current_state = State.IDLE
        print("Ending LED Test...")
        
    elif current_state == State.AUDIO_TEST:
        print("Starting Audio Test...")

        # Audio Setup
        pygame.mixer.init()
        pygame.mixer.music.load("name.wav")
        pygame.mixer.music.play()
        sleep(12.0)
        pygame.mixer.music.pause()
        current_state = State.IDLE

        print("Ending Audio Test...")
        
    elif current_state == State.MOTION_HAT_TEST:
        print("Starting Hat Test...")
        while current_state == State.MOTION_HAT_TEST:
            move_servo(servo_hat)
        print("Ending Hat Test...")

    elif current_state == State.MOTION_TEACUPS_TEST:
        print("Starting Teacups Test...")
        while current_state == State.MOTION_TEACUPS_TEST:
            move_servo(servo_cups)
        print("Ending Teacups Test...")


    sleep(0.5)