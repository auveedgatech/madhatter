import RPi.GPIO as GPIO
from time import sleep
from enum import Enum
import os, sys
import serial
import string
import pygame
import threading

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
    PERFORM_ALL = 7
    
# Setup Current State
current_state = State.IDLE

# Setup Interrupts
def reset_callback(channel):
    print("Resetting to Idle")
    global current_state
    current_state = State.IDLE
    
    
def led_test_callback(channel):
    global current_state
    if current_state == State.IDLE:
        current_state = State.LED_TEST
    
def audio_test_callback(channel):
    global current_state
    if current_state == State.IDLE:
        current_state = State.AUDIO_TEST

def motion_hat_callback(channel):
    global current_state
    if current_state == State.IDLE:
        current_state = State.MOTION_HAT_TEST
    
def motion_teacups_callback(channel):
    global current_state
    if current_state == State.IDLE:
        current_state = State.MOTION_TEACUPS_TEST

def enable_director_code(channel):
    global current_state
    if current_state == State.IDLE:
        current_state = State.CONNECT_TO_DIRECTOR

# Audio Setup
ser = serial.Serial('/dev/ttyACM0', 9600)
def parse_int_serial(str):
    return int(str.strip(string.ascii_letters))

#Sends audio to headphone jack
pygame.mixer.init()


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

# Director Button:
director_pin = 38
GPIO.setup(director_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(director_pin, GPIO.RISING, callback=enable_director_code)

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
def move_hat(p):
    if current_state == State.IDLE: return
    p.ChangeDutyCycle(2.5)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(4)
    if current_state == State.IDLE: return
    p.ChangeDutyCycle(12.5)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(4)
    
def move_teacups(p):
    if current_state == State.IDLE: return
    p.ChangeDutyCycle(2.5)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(4)
    if current_state == State.IDLE: return
    p.ChangeDutyCycle(7.5)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(4)
    if current_state == State.IDLE: return
    p.ChangeDutyCycle(12.5)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(4)
    if current_state == State.IDLE: return
    p.ChangeDutyCycle(7.5)
    sleep(1)
    p.ChangeDutyCycle(0)
    sleep(4)

# Network Functions
import sys
import socket
import selectors
import traceback
import multiprocessing
import time
import keyboard 

from Protocol import libserver
from Protocol import libclient

from Utils.robotUtils import create_request, listen_for_director, start_connection, initiate_connection

ROBOT_NAME = "Robot0"
HOST = "172.20.10.14"
PORT = 65432 

LISTEN_PORT = 65433

def register_with_director():
    try:
        global current_state
        print('Register with director...')
        registration_request = create_request(ROBOT_NAME, "Register", LISTEN_PORT)
        initiate_connection(HOST, PORT, registration_request, libclient)
        print('Finished registration, booting up server to listen...')
        current_state = State.WAIT_FOR_INTRUCTION
    except:
        print("Failed to connect, return to IDLE")
        current_state = State.IDLE

#State Functions:
def led_on():
    led_out = GPIO.HIGH;
    GPIO.output(led_output_port, led_out);        

def led_off():
    led_out = GPIO.LOW
    GPIO.output(led_output_port, led_out);

def audio_thread():
    global current_state
    # Audio Test
    while True:
        line = ser.readline()
        if current_state == State.AUDIO_TEST or current_state == State.PERFORM_ALL:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load("name.wav")
                pygame.mixer.music.play()

            if len(line) == 0:
                print("Serial Setup Failed")

            volume = parse_int_serial(line.decode("utf-8"))
            print(volume)
            pygame.mixer.music.set_volume(volume/100)
        sleep(0.1)
        
def motion_hat_thread():
    global current_state
    while True:
        if current_state == State.MOTION_HAT_TEST or current_state == State.PERFORM_ALL:
            move_hat(servo_hat)
        sleep(0.1)
        
def motion_cups_thread():
    global current_state
    while True:
        if current_state == State.MOTION_TEACUPS_TEST or current_state == State.PERFORM_ALL:
            move_teacups(servo_cups)
        sleep(0.1)

def perform_all_thread():
    t1 = threading.Thread(target=led_on)
    t1.start()
    
#Main code
# Make a thread for each state and start accordingly
t_audio = threading.Thread(target=audio_thread)
t_audio.start()

t_hat = threading.Thread(target=motion_hat_thread)
t_hat.start()

t_cups = threading.Thread(target=motion_cups_thread)
t_cups.start()

while True:
    
    if current_state == State.IDLE:
        # Idle State
        is_perfoming = False
        
        
        #LED Cleanup
        led_off()
        
        # Servo Cleanup
        servo_hat.ChangeDutyCycle(0)
        servo_cups.ChangeDutyCycle(0)
        
        # Audio Cleanup
        pygame.mixer.music.stop()
        

    elif current_state == State.LED_TEST:
        # Set LED High:
        led_on()        
    elif current_state == State.CONNECT_TO_DIRECTOR:
        #register_with_director()
        current_state = State.PERFORM_ALL
    elif current_state == State.WAIT_FOR_INTRUCTION:
        print("Awaiting for Instruction")
    elif current_state == State.PERFORM_ALL:
        led_on()

    sleep(0.1)